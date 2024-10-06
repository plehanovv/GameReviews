from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class RegisterUserTestCase(TestCase):
    def test_form_registr(self):
        path = reverse('users:register')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')