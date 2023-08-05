import base64
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.base import BaseEmailBackend
from email import utils
from email.mime.base import MIMEBase
import sendgrid
from sendgrid.helpers.mail import Attachment
from sendgrid.helpers.mail import Category
from sendgrid.helpers.mail import Content
from sendgrid.helpers.mail import Email
from sendgrid.helpers.mail import Mail
from sendgrid.helpers.mail import Personalization
from sendgrid.helpers.mail import Substitution
try:
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import HTTPError

from .version import __version__

class SendGridBackend(BaseEmailBackend):
    """
    SendGrid API backend for Django
    """
    def __init__(self, fail_silently=False, **kwargs):
        super(SendGridBackend, self).__init__(fail_silently=fail_silently,
            **kwargs)

        # Store the API key from settings
        self.api_key = getattr(settings, "SENDGRID_API_KEY", None)

        # Verify an API key is present
        if not self.api_key:
            raise ImproperlyConfigured(
                'SENDGRID_API_KEY must be set in settings')

        # Instantiate the SendGrid module
        self.sg = sendgrid.SendGridAPIClient(apikey=self.api_key)
        self.version = 'sendgrid/{0};django'.format(__version__)
        self.sg.client.request_headers['User-agent'] = self.version

    def send_messages(self, emails):
        """
        Send a collection of email messages
        """
        if not emails:
            return

        num_sent = 0
        for e in emails:
            mail = self._build_sg_mail(e)
            try:
                self.sg.client.mail.send.post(request_body=mail)
                num_sent += 1
            except HTTPError as e:
                if not self.fail_silently:
                    raise

        return num_sent

    def _build_sg_mail(self, email):
        m = Mail()

        # From name & email address
        from_name, from_email = utils.parseaddr(email.from_email)
        if not from_name:
            from_name = None
        m.from_email = Email(from_email, from_name)

        # Message subject
        m.subject = str(email.subject) # Ensure subject is translated

        # Message personalization
        p = Personalization()
        for e in email.to:
            p.add_to(Email(e))
        for e in email.cc:
            p.add_cc(Email(e))
        for e in email.bcc:
            p.add_bcc(Email(e))
        p.subject = str(email.subject)

        # Message body
        m.add_content(Content('text/plain', email.body))
        if isinstance(email, EmailMultiAlternatives):
            for a in email.alternatives:
                if a[1] == 'text/html':
                    m.add_content(Content(a[1], a[0]))
        elif email.content_subtype == 'html':
            m.contents = []
            m.add_content(Content('text/plain', ' ')) # TODO: html to text
            m.add_content(Content('text/html', email.body))

        # SendGrid categories
        if hasattr(email, 'categories'):
            for c in email.categories:
                m.add_category(Category(c))

        # SendGrid templates
        if hasattr(email, 'template_id'):
            m.template_id = email.template_id
            if hasattr(email, 'substitutions'):
                for k, v in email.substitutions.items():
                    p.add_substitution(Substitution(k,v))

        # Other headers
        for k, v in email.extra_headers.items():
            m.add_header({k: v})

        # Attachments
        for a in email.attachments:
            if isinstance(a, MIMEBase):
                _a = Attachment()
                _a.set_filename(a.get_filename())
                _a.set_content(base64.b64encode(a.get_payload()))
                m.add_attachment(_a)
            elif instance(a, tuple):
                _a = Attachment()
                _a.set_filename(a[0])
                _a.set_content(str(base64.b64encode(a[1])))
                _a.set_type(a[2])
                m.add_attachment(_a)

        # Personalization
        m.add_personalization(p)

        # Ready to go!
        return m.get()