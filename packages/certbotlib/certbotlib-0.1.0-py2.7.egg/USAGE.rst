=====
Usage
=====

Prepare your environment:

This assumes your binary is at `/usr/local/bin/certbot`
In order to install it please refer to  https://certbot.eff.org/


Instantiate your Certbot and variables

.. code-block:: python

    from certbotlib import Certbot
    import logging

    logging.basicConfig(level=logging.INFO)
    directory = '/Users/payconiq/certbotlib'
    domain = 'mydomain.payconiq.io'



In order to create a certificate for a domain `mydomain.payconiq.io` and create
a record on the account `devops-prod` where the DNS records are kept but
the certificate should be uploaded to your `default` account:


.. code-block:: python

    certbot = Certbot(email='devops@payconiq.com',
                  logs_dir=directory,
                  work_dir=directory,
                  config_dir=directory,
                  domain=domain,
                  region='eu-central-1',
                  profile='devops-prod')

Now let's say you only want to create certificates for the ones that will expire
in 1 week and so re-import them.
You'll need `awslib` library to help you out. Have a go:
http://python.docs.payconiq.io/awslib/

.. code-block:: python

    from awslib import Acm
    acm = Acm(region='eu-central-1')

    certificates = [certificate for certificate
                    in acm.get_expiring_certs_by_days(40)
                    if 'Encrypt' in certificate.issuer]

    for certificate in certificates:
        certbot = Certbot(email='devops@payconiq.com',
                          logs_dir=directory,
                          work_dir=directory,
                          config_dir=directory,
                          domain=certificate.domain_name,
                          region='eu-central-1',
                          profile='devops-prod')

