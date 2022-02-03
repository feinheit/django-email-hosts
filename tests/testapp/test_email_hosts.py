import dj_email_url
from django.test import TestCase

from email_hosts.backends import parse_conf


class EmailHostsTest(TestCase):
    def test_parse_conf(self):
        conf = parse_conf(
            **dj_email_url.parse("submission://USER:PASSWORD@smtp.sendgrid.com")
        )
        self.assertEqual(
            conf,
            {
                "host": "smtp.sendgrid.com",
                "port": 587,
                "username": "USER",
                "password": "PASSWORD",
                "use_tls": True,
                "use_ssl": False,
                "ssl_keyfile": None,
                "ssl_certfile": None,
            },
        )
