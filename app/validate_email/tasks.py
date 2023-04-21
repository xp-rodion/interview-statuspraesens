from config.celery import app

from common.func import get_email_addresses
from validate_email.models import EmailFile, EmailResult
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


@app.task
def validate_email_task(email_file_id):
    email_file = EmailFile.objects.get(id=email_file_id)
    emails = get_email_addresses(f'media/{email_file.__str__()}')
    for email in emails:
        try:
            validate_email(email)
            is_valid = True
        except (ValidationError, TypeError):
            is_valid = False
        EmailResult.objects.create(email=email, is_valid=is_valid, file=email_file)
