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


"""
Работа с двумя очередями, но с одной таской.
вызывать во вьюхе, с помощью кода ниже.

You can also override this using the routing_key argument to Task.apply_async(), or send_task():

from feeds.tasks import import_feed

import_feed.apply_async(args=['uuid почты'],
                        queue='mail_queue', здесь мы задаем явно в какую очередь кинуть
                        routing_key='feed.import' мб не нужен, почитать.)
                        
вызывать данную очередь -> celery -A путь до файла с настройками -Q таска
                   
прочитать про очереди и поточность

при парсе excel и txt, просто каждый раз вызывать валидировать наш mail и отправлять в нужную очередь
"""