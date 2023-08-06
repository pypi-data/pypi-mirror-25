from .version import __version__

import base64
import sys
from email.mime.base import MIMEBase

try:
    from urllib.error import HTTPError  # pragma: no cover
except ImportError: # pragma: no cover
    from urllib2 import HTTPError  # pragma: no cover

from email.utils import parseaddr

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.base import BaseEmailBackend

import sendgrid
from sendgrid.helpers.mail import (
    Attachment,
    Category,
    Content,
    Email,
    Header,
    Mail,
    Personalization,
    Substitution
)


class SendGridBackend(BaseEmailBackend):
    """
    Email backend that uses the SendGrid API to send messages
    """
    def __init__(self, api_key=None, fail_silently=False, **kwargs):
        super(SendGridBackend, self).__init__(
            fail_silently=fail_silently, **kwargs)

        self.api_key = api_key if api_key is not None else \
            getattr(settings, 'SENDGRID_API_KEY', None)

        if not self.api_key:
            raise ImproperlyConfigured(
                'SENDGRID_API_KEY must be declared in settings.py')

        # Instantiate a copy of the API client
        self.sg = sendgrid.SendGridAPIClient(apikey=self.api_key)
        self.sg.client.request_headers['User-agent'] = \
            'sgapi/{0};django'.format(__version__)


    def send_messages(self, emails):
        """
        Sends one or more EmailMessage objects through the SendGrid API and
        returns the number of messages sent
        """
        if not emails:
            return

        num_sent = 0
        for email in emails:
            request = self._build_request(email)
            try:
                self.sg.client.mail.send.post(request_body=request)
                num_sent += 1
            except HTTPError as e:
                if not self.fail_silently:
                    raise
        return num_sent


    def _build_request(self, email):
        """
        Helper that constructs the request body for an email message
        """
        mail = Mail()

        # Set the from email
        mail.from_email = self._handle_email_addr(email.from_email)

        # Set the email subject
        mail.subject = email.subject

        # Set content
        for content in self._handle_contents(email):
            mail.add_content(content)

        # Set categories
        if hasattr(email, 'categories'):
            for category in email.categories:
                mail.add_category(Category(category))

        # Set template_id
        if hasattr(email, 'template_id'):
            mail.template_id = email.template_id

        # Set headers
        for header in self._handle_headers(email.extra_headers):
            mail.add_header(header)

        if hasattr(email, 'reply_to'):
            if email.reply_to:
                mail.reply_to = self._handle_email_addr(email.reply_to)

        # Set attachments
        for attachment in self._handle_attachments(email.attachments):
            mail.add_attachment(attachment)

        # Set personalizations
        mail.add_personalization(self._handle_personalization(email.to,
            email.cc, email.bcc, email.subject, 
            email.substitutions if hasattr(email, 'substitutions') else None))

        return mail.get()


    def _handle_email_addr(self, email_addr):
        """
        Helper to format the from_email address
        """

        # Correct for some cases where django passes a single email as a tuple
        # e.g., for reply_to
        if isinstance(email_addr, (list, tuple)):
            email_addr = email_addr[0]

        name, email = parseaddr(email_addr)
        if not name:
            name = None
        return Email(email, name)


    def _handle_personalization(self, to, cc=None, bcc=None, subject=None,
        substitutions=None):
        """
        Helper to set personalizations
        """
        personalization = Personalization()

        for email in to:
            personalization.add_to(self._handle_email_addr(email))

        if cc is not None:
            for email in cc:
                personalization.add_cc(self._handle_email_addr(email))

        if bcc is not None:
            for email in bcc:
                personalization.add_bcc(self._handle_email_addr(email))

        personalization.subject = subject

        if substitutions is not None:
            for key, value in substitutions.items():
                personalization.add_substituion(Substitution(key, value))

        return personalization


    def _handle_contents(self, email):
        """
        Helper to format contents
        """
        contents = []
        if isinstance(email, EmailMultiAlternatives):
            contents.append(Content('text/plain', email.body))
            for alternative in email.alternatives:
                contents.append(Content(alternative[1], alternative[0]))
        elif email.content_subtype == 'html':
            contents.append(Content('text/plain', ' '))
            contents.append(Content('text/html', email.body))
        else:
            contents.append(Content('text/plain', email.body))
        return contents


    def _handle_headers(self, extra_headers):
        """
        Helper to format extra headers
        """
        headers = []
        forbidden = ['reply-to']
        for key, value in extra_headers.items():
            if key not in forbidden:
                headers.append(Header(key,value))
        return headers


    def _handle_attachments(self, email_attachments):
        attachments = []
        for attachment in email_attachments:
            filename, content, content_type = (None, None, None)

            if isinstance(attachment, MIMEBase):
                filename = attachment.get_filename()
                content = attachment.get_payload()
                content_type = attachment.get_content_type()
                if attachment.get_content_maintype() == 'text' \
                    and isinstance(content, str):
                    content = self._b64_encode_str(content)
                else:
                    content = self._b64_encode_bytes(content)
            elif isinstance(attachment, tuple):
                filename, content, content_type = attachment
                basetype, subtype = content_type.split('/', 1)
                if basetype == 'text' and isinstance(content, str):
                    content = self._b64_encode_str(content)
                elif isinstance(content, bytes):
                    content = self._b64_encode_bytes(content)

            assert content is not None

            attachment = Attachment()
            attachment.filename = filename
            attachment.type = content_type
            attachment.content = content
            attachments.append(attachment)

        return attachments

    def _b64_encode_str(self, content):
        assert isinstance(content, str)
        return base64.b64encode(content.encode('utf-8')).decode('utf-8')

    def _b64_encode_bytes(self, content):
        assert isinstance(content, bytes)
        return base64.b64encode(content).decode('utf-8')
