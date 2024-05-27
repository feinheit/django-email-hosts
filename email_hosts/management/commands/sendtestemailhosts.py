import socket

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from email_hosts.backends import get_connection


class Command(BaseCommand):
    help = "Sends a test email to the email addresses specified as arguments."

    missing_args_message = "You must specify some email recipients."

    def add_arguments(self, parser):
        parser.add_argument(
            "backend",
            help="Backend to which mail should be sent.",
        )
        parser.add_argument(
            "email",
            nargs="*",
            help="One or more email addresses to send a test email to.",
        )

    def handle(self, *args, **kwargs):
        subject = f"Test email from {socket.gethostname()} on {timezone.now()}"

        send_mail(
            subject=subject,
            message="If you're reading this, it was successful.",
            from_email=None,
            recipient_list=kwargs["email"],
            connection=get_connection(kwargs["backend"]),
        )
