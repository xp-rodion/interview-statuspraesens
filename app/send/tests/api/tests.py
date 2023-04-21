from django.urls import reverse
from rest_framework.test import APITestCase

from common.func import send_message
from send.models import Email


class EmailApiTestCase(APITestCase):
    DATA = {
        "receiver": "test@mail.ru",
        "receiver_copy": "test_copy@mail.ru",
        "title": "test_title",
        "body": "test_body",
    }

    def setUp(self) -> Email:
        return Email.objects.create(**self.DATA)

    def test_post(self):
        path = reverse("api:send:create_email")
        response = self.client.post(path=path, data=self.DATA)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.DATA["receiver"], response.data["receiver"])
        self.assertEqual(self.DATA["receiver_copy"], response.data["receiver_copy"])
        self.assertEqual(self.DATA["title"], response.data["title"])
        self.assertEqual(self.DATA["body"], response.data["body"])

    def test_send_message(self):
        email = self.setUp()
        send_message(email)
        self.assertEqual(email.status, email.STATUS_SUCCESS)