from django.test import TestCase

from common.func import get_email_addresses
from validate_email.models import EmailFile, EmailResult
from validate_email.tasks import validate_email_task


class EmailValidationTests(TestCase):
    FILE = 'file_tests/email.xlsx'

    def create_email_file(self):
        email_file = EmailFile.objects.create(file=self.FILE)
        return email_file

    def test_get_email_adresses(self):
        emails = get_email_addresses(f'media/{self.FILE}')
        self.assertEqual(emails[0], "tr@mail.ru")
        self.assertEqual(emails[1], 123123)

    def test_validate_email_task(self):
        email_file = self.create_email_file()
        validate_email_task(email_file.id)
        result = EmailResult.objects.filter(file__pk=email_file.pk)
        self.assertTrue(result[0].is_valid)
        self.assertFalse(result[1].is_valid)