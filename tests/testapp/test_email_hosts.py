from unittest import mock

import dj_email_url
from django.core.mail import EmailMessage
from django.test import TestCase
from django.test.utils import override_settings

from email_hosts.backends import parse_conf, use_backend


class EmailHostsTest(TestCase):
    def test_parse_conf(self):
        conf = parse_conf(
            dj_email_url.parse("submission://USER:PASSWORD@smtp.sendgrid.com")
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
            },
        )

    @override_settings(
        EMAIL_HOSTS={
            "en": "submission://USER:PASSWORD@smtp.sendgrid.com",
            "de": "submission://USER:PASSWORD@smtp.mailgun.com",
        },
    )
    def test_use_backend(self):
        self.assertEqual(use_backend("en").host, "smtp.sendgrid.com")
        self.assertEqual(use_backend("de").host, "smtp.mailgun.com")

        with mock.patch("smtplib.SMTP", autospec=True) as mock_smtp:
            EmailMessage(
                "Hello",
                "World",
                to=["recipient@example.com"],
                connection=use_backend("en"),
            ).send()

            mock_smtp.assert_called()
            name, args, kwargs = [
                call for call in mock_smtp.method_calls if call[0].endswith(".sendmail")
            ][0]
            # print(sendmail)
            print(name, args, kwargs)

            self.assertEqual(args[0], "webmaster@localhost")
            self.assertEqual(args[1], ["recipient@example.com"])

            lines = args[2].splitlines()
            self.assertIn(b"From: webmaster@localhost", lines)
            self.assertIn(b"To: recipient@example.com", lines)

            # context = mock_smtp.return_value.__enter__.return_value
            # print(context, context.__dict__)
            # context.ehlo.assert_called()
            # context.starttls.assert_called()
            # context.login.assert_called()
            # context.send_message.assert_called_with(msg)
