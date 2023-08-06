django-sgapi
============

A Django email backend for the SendGrid API

.. image:: https://travis-ci.org/jtstio/django-sgapi.svg?branch=master
  :target: https://travis-ci.org/jtstio/django-sgapi
.. image:: https://codecov.io/gh/jtstio/django-sgapi/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/jtstio/django-sgapi
.. image:: https://badge.fury.io/py/django-sgapi.svg
  :target: https://pypi.python.org/pypi/django-sgapi


Installation
------------

Install the backend from PyPI:

.. code:: bash

  pip install django-sgapi

Add the following to your project's **settings.py**:

.. code:: python

  EMAIL_BACKEND = "sgbackend.SendGridBackend"
  SENDGRID_API_KEY = "Your SendGrid API Key"

**Done!**


Example
-------

.. code:: python

  from django.core.mail import send_mail
  from django.core.mail import EmailMultiAlternatives

  # Send a simple message
  send_mail('Hello there!', 'Emails are the future!',
    'Jay Hale <jay@jtst.io>', ['hello@sink.sendgrid.net'])

  # Send a more complex message
  mail = EmailMultiAlternatives(
    subject='Hello there again!',
    body='Who knew you could do so many things with email?!?',
    from_email='Jay Hale <jay@jtst.io>',
    to=['hello@sink.sendgrid.net'],
  )
  mail.reply_to = 'No Reply <no-reply@sink.sendgrid.net>'
  mail.template_id = 'marketing_template_5'
  mail.substitutions = {'%organization%': 'jtstio'}
  with open('flyer.pdf', 'rb') as file:
      mail.attachments = [
          ('flyer.pdf', file.read(), 'application/pdf')
      ]
  mail.attach_alternative(
      "<p>Who knew you could do <strong>so many things</strong> with email?!?</p>",
      "text/html"
  )
  mail.send()


Attribution
-----------
`sendgrid-django-v5 <https://github.com/sklarsa/django-sendgrid-v5>`_: An
alternative implementation you should check out

`sendgrid-django <https://github.com/elbuo8/sendgrid-django>`_: Basis for this
implementation

`sendgrid-python <https://github.com/sendgrid/sendgrid-python>`_: Python
SendGrid connector


License
-------
MIT


Enjoy :)