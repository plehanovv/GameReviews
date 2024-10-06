from http import HTTPStatus
from django.test import TestCase
import unittest
from django.urls import reverse


class GetPagesTestCases(TestCase):
    def setUp(self):
        "Инициализация перед выполнением теста"

    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'review_app/index.html')

    def test_redirectpage(self):
        path = reverse('add_review')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)

        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def tearDown(self):
        "Действия после выполнение теста"

