from __future__ import absolute_import, unicode_literals

import uuid

from django.conf import settings
from django.core.mail import send_mail

from config.celery import app
from . import models


@app.task
def send_email(email_uid: uuid):
    email = models.Email.objects.get(uid=email_uid)
    send_mail(
        subject=email.title,
        message=email.body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email.receiver],
        fail_silently=False)