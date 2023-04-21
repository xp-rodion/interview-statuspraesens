import logging
from random import randrange
from common.func import send_message
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from tqdm import tqdm

from ... import models


class Command(BaseCommand):
    help = 'Рассылка писем'
    logger = logging.getLogger('default')

    def handle(self, *args, **options):
        qs = models.Email.objects.filter(status=models.Email.STATUS_GENERATED)
        for email in tqdm(qs):
            random_int = randrange(10)
            if random_int < 8:
                email.departure_date = now()
                send_message(email=email)