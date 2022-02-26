from unittest import mock

from django.core.mail import EmailMessage
from django.test import TestCase
from django.test.utils import override_settings
from speckenv_django import django_email_url

from email_hosts.backends import get_connection, parse_conf


EMAIL_HOSTS = {
    "one": "submission://USER:PASSWORD@smtp.sendgrid.com",
    "two": "submission://USER:PASSWORD@smtp.mailgun.com?_default_from_email=info@example.org",
}


class EmailHostsTest(TestCase):
    def test_parse_conf(self):
        conf = parse_conf(
            django_email_url("submission://USER:PASSWORD@smtp.sendgrid.com")
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
                "timeout": None,
            },
        )

    @override_settings(EMAIL_HOSTS=EMAIL_HOSTS)
    def test_get_connection(self):
        self.assertEqual(get_connection("one").host, "smtp.sendgrid.com")
        self.assertEqual(get_connection("two").host, "smtp.mailgun.com")

        self.assertEqual(get_connection("one").default_from_email, "")
        self.assertEqual(get_connection("two").default_from_email, "info@example.org")

    @override_settings(
        EMAIL_HOSTS={},
        # It is the default when running tests but let's be explicit anyway.
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    )
    def test_get_connection_fallback(self):
        connection = get_connection("nothing")
        self.assertEqual(
            connection.__class__.__module__,
            "django.core.mail.backends.locmem",
        )

    @override_settings(EMAIL_HOSTS=EMAIL_HOSTS)
    def test_without_default_from_email(self):
        with mock.patch("smtplib.SMTP", autospec=True) as mock_smtp:
            EmailMessage(
                "Hello",
                "World",
                to=["recipient@example.com"],
                connection=get_connection("one"),
            ).send()

            mock_smtp.assert_called()
            name, args, kwargs = [
                call for call in mock_smtp.method_calls if call[0].endswith(".sendmail")
            ][0]

            self.assertEqual(args[0], "webmaster@localhost")
            self.assertEqual(args[1], ["recipient@example.com"])

            lines = args[2].splitlines()
            self.assertIn(b"From: webmaster@localhost", lines)
            self.assertIn(b"To: recipient@example.com", lines)

    @override_settings(EMAIL_HOSTS=EMAIL_HOSTS)
    def test_with_default_from_email(self):
        with mock.patch("smtplib.SMTP", autospec=True) as mock_smtp:
            EmailMessage(
                "Hello",
                "World",
                to=["recipient@example.com"],
                connection=get_connection("two"),
            ).send()

            mock_smtp.assert_called()
            name, args, kwargs = [
                call for call in mock_smtp.method_calls if call[0].endswith(".sendmail")
            ][0]

            self.assertEqual(args[0], "info@example.org")
            self.assertEqual(args[1], ["recipient@example.com"])

            lines = args[2].splitlines()
            self.assertIn(b"From: info@example.org", lines)
            self.assertIn(b"To: recipient@example.com", lines)

    @override_settings(EMAIL_HOSTS=EMAIL_HOSTS)
    def test_with_default_from_email_and_explicit_sender(self):
        with mock.patch("smtplib.SMTP", autospec=True) as mock_smtp:
            EmailMessage(
                "Hello",
                "World",
                to=["recipient@example.com"],
                from_email="no-reply@example.com",
                connection=get_connection("two"),
            ).send()

            mock_smtp.assert_called()
            name, args, kwargs = [
                call for call in mock_smtp.method_calls if call[0].endswith(".sendmail")
            ][0]

            self.assertEqual(args[0], "no-reply@example.com")
            self.assertEqual(args[1], ["recipient@example.com"])

            lines = args[2].splitlines()
            self.assertIn(b"From: no-reply@example.com", lines)
            self.assertIn(b"To: recipient@example.com", lines)
