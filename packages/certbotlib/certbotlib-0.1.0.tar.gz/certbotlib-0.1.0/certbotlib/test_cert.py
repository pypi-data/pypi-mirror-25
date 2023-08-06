from certbotlib import Certbot
from awslib import Acm
import logging
logger = logging.getLogger('certbotlib')

logging.basicConfig(level=logging.INFO)
directory = '/Users/oriolfb/Desktop/certbotlib'

lets_encrypt_certs = []
acm = Acm(region='eu-central-1')
certificates = acm.get_expiring_certs_by_days(40)

for certificate in certificates:
    if 'Encrypt' in certificate.issuer:
        lets_encrypt_certs.append(certificate)

certbot = Certbot(email='devops@payconiq.com',
                  logs_dir=directory,
                  work_dir=directory,
                  config_dir=directory,
                  # domain=lets_encrypt_certs[0].domain_name,
                  domain='test4.payconiq.io',
                  region='eu-central-1',
                  profile='oriol-prod')
