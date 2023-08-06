#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-
# File: certbotlib.py
"""
Main module file

Put your classes here
"""

import logging
import subprocess
import os
from time import sleep
from awslib import Route53, Acm


__author__ = '''Oriol Fabregas <oriol.fabregas@payconiq.com>'''
__docformat__ = 'plaintext'
__date__ = '''11-09-2017'''

# This is the main prefix used for logging
LOGGER_BASENAME = '''certbotlib'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class Certbot(object): # noqa
    """
    Main interface object.

    Executes certbot on your OS with the given parameters and performs the
    requests to Route53 to create the TXT record and validate back to Cerbot.

    If validation is succeeded, Cerbot will issue the certificates and upload
    them in Amazon Certificate Manager. If the certificate for the given domain
    already exists, it will replace the certificates instead of creating a new
    ARN (this is usually what you want).

    For obvious reasons, certbot needs access to public DNS zones. At Payconiq,
    our DNS is held by Production account but one might need certificates on
    Acceptance as well. In this case, the library accepts a profile to
    indicate in which account your DNS records are. How to choose a profile is
    documented directly on AWS

    +info: http://boto3.readthedocs.io/en/latest/guide/configuration.html#shared-credentials-file
    """

    def __init__(self,  # noqa
                 email,
                 logs_dir,
                 work_dir,
                 config_dir,
                 domain,
                 region,
                 profile):
        """
        Initialises object with given parameters

        Certbot creates sub directories automatically but one has to override
        the default directory otherwise it will attempt to create them on
        directories where regular users don't have access.

        This assumes your binary is at /usr/local/bin/certbot

        :param email: string
        :param logs_dir: string
        :param work_dir: string
        :param config_dir: string
        :param domain: string
        :param region: string
        :param profile: string
        """
        self.logger = logging.getLogger('{base}.{suffix}'.format(
            base=LOGGER_BASENAME, suffix=self.__class__.__name__))
        self.route = Route53(profile_name=profile)
        self.acm = Acm(region=region)
        self._domain = domain
        self._config_dir = config_dir
        self.cmd = ['/usr/local/bin/certbot',
                    '-m', email,
                    '--text',
                    '--logs-dir', logs_dir,
                    '--work-dir', work_dir,
                    '--config-dir', config_dir,
                    '--agree-tos',
                    '-d', domain,
                    '--manual',
                    '--manual-public-ip-logging-ok',
                    '--no-eff-email',
                    '--preferred-challenges',
                    'dns',
                    'certonly']
        self.key = None
        self.acme = None
        self.certs_dir = None
        self._region = region
        self._parse()

    def _parse(self):
        """
        Execute certbot binary and runs business logic

        1. Runs certbot binary with parameters
        2. Parses output and gets KEY and ACME record
        3. Creates DNS record on Route53 and waits 20 seconds (propagation)
        4. Issues a new line (enter) to certbot to verify the record
        5. Issues the certificates
        6. Uploads them to ACM

        :return: boolean
        """
        self.logger.info("Running certbot")
        self.logger.debug("Full command: {}".format(self.cmd))
        process = subprocess.Popen(self.cmd,
                                   shell=False,
                                   bufsize=0,
                                   stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   stdout=subprocess.PIPE)
        discard = ['--------------', 'Please', 'Before']
        while True:
            line = process.stdout.readline()
            line = line.replace('\n', '')
            if not any([disc in line for disc in discard]) and line:
                if '_acme-challenge' in line:
                    try:
                        self.acme = line.split()[0]
                    except IndexError:
                        self.logger.error("Can't get ACME domain")
                else:
                    self.key = line
            if self.key and self.acme:
                self.create_aws_dns()
                self.logger.info('Waiting for changes to propagate')
                sleep(20)
                self.logger.info("Verifying record with Certbot")
                result = process.communicate(input='\n')
                self._parse_after_input([r for r in result])
                cert, key, chain = self.check_certificate_path()
                self.upload_certificates(cert=cert, key=key, chain=chain)
                break
        return True

    def check_certificate_path(self):
        """
        Validates if certificates exist on filesystem

        :return: tuple with cert, key and chain
        """
        try:
            cert = open('{dir}/cert.pem'.format(dir=self.certs_dir), 'rb')
            key = open('{dir}/privkey.pem'.format(dir=self.certs_dir), 'rb')
            chain = open('{dir}/fullchain.pem'.format(dir=self.certs_dir), 'rb')
        except IOError:
            raise OSError("Couldn't find the certificates folder")
        return cert, key, chain

    def _parse_after_input(self, result):
        """
        Gets the standard output of the command after issuing a new line

        This output usually indicates if the certificates have been created and
        if so, it will show where have been saved

        :param result: tuple
        :return: boolean
        """
        for line in result[0].split('\n'):
            self.logger.debug(line)
            if self._domain in line:
                self.certs_dir = os.path.dirname(line.strip())
                self.logger.info("Certificates created."
                                 "Path: {}".format(self.certs_dir))
            else:
                self.logger.error("Couldn't get the certificates")
        return True

    def create_aws_dns(self):
        """
        Creates DNS record to Route53 public zone

        :return: boolean
        """
        result = False
        self.logger.debug("Got key {}\n"
                          "With Acme {}".format(self.key, self.acme))
        self.logger.info("Updating/Creating DNS record in AWS")
        change_batch = {'Changes': [{'Action': 'UPSERT',
                                     'ResourceRecordSet':
                                         {'Name': self.acme,
                                          'Type': 'TXT',
                                          'TTL': 300,
                                          'ResourceRecords':
                                              [{'Value': '"{txt_value}"'.format(txt_value=self.key)}]}}]}
        response = self.route.change_domain_by_zone(zone=self.__get_public_zone()[0].zone_id,
                                                    domain_details=change_batch)
        self.logger.debug(response)
        if response.get('ChangeInfo'):
            self.logger.info("Domain created/updated")
            result = True
        return result

    def __get_public_zone(self):
        """
        Gets the public zone(s) for a given account

        :return: List of Zone object
        """
        zone = [zone for zone in self.route.get_zones()
                if not zone.is_private and zone.name[:-1] in self._domain]
        return zone

    def upload_certificates(self, cert, key, chain):
        """
        Uploads/replaces to ACM for a given account

        :param cert: path to certificate
        :param key: path to key
        :param chain: path to fullchain certificate
        :return: dictionary
        """
        self.logger.info("Uploading certificates")
        certs = self.acm.get_certificates_by_status()
        kwargs = {}
        for certificate in certs:
            if self._domain == certificate.domain_name:
                self.logger.info("Certificate already exist for {} domain".format(self._domain))
                kwargs['CertificateArn'] = certificate.arn
        response = self.acm.import_certificate(certificate=cert.read(),
                                               private_key=key.read(),
                                               certificate_chain=chain.read(),
                                               **kwargs)
        self.logger.debug(response)
        if response.get('CertificateArn', {}):
            self.logger.info("Certificate updated successfully")
        return response
