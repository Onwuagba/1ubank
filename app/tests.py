from django.test import TestCase, Client
from django.urls import reverse
import logging
from unittest.mock import patch

from django.test import TestCase
from app.models import Article, Currency, Provider
from unittest import mock
from django.test import TestCase
from rest_framework import status
from rest_framework.renderers import JSONRenderer


class ProviderTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.data = {"provider_name": "dola"}
        Provider.objects.create(**self.data)

    def test_provider_list(self):
        url = reverse("app:providers")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_provider_detail(self):
        provider_id = "0001"
        url = reverse("app:provider-detail", args=[provider_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("app.views.logger", logging.getLogger("test_logger"))
    def create_provider(self, arg0):
        url = reverse("app:providers")
        data = {"provider_name": arg0}
        return self.client.post(url, data)

    def test_provider_create(self):
        response = self.create_provider("boy")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_provider_duplicate_create(self):
        response = self.create_provider("dola")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CurrencyTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.data = {"currency_id": "USD", "currency_name": "dola"}
        Currency.objects.create(**self.data)

    def test_currency_list(self):
        url = reverse("app:currency")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_currency_detail(self):
        id = "usd"
        url = reverse("app:currency-detail", args=[id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data["data"], self.data)

    @patch("app.views.logger", logging.getLogger("test_logger"))
    def test_currency_create(self):
        url = reverse("app:currency")
        data = {"currency_id": "ngn", "currency_name": "naira"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


test_data = [
    # Happy path tests
    {
        "id": "happy1",
        "currency_id": "usd",
        "provider_no": "0001",
        "price": 1002,
        "expected_status": status.HTTP_201_CREATED,
        "expected_re_status": "success",
        "raise_exception": False,
    },
    {
        "id": "happy2",
        "currency_id": "ngn",
        "provider_no": "0001",
        "price": 1.000,
        "expected_status": status.HTTP_201_CREATED,
        "expected_re_status": "success",
        "raise_exception": False,
    },
    # Edge case tests
    {
        "id": "edge1",
        "currency_id": None,
        "provider_no": 1,
        "price": "",
        "expected_status": status.HTTP_400_BAD_REQUEST,
        "expected_re_status": "failed",
        "raise_exception": True,
    },
    {
        "id": "edge2",
        "currency_id": 1,
        "provider_no": None,
        "price": 1002,
        "expected_status": status.HTTP_400_BAD_REQUEST,
        "expected_re_status": "failed",
        "raise_exception": True,
    },
    # Error case tests
    {
        "id": "error1",
        "currency_id": "invalid",
        "provider_no": 1,
        "price": 1002,
        "expected_status": status.HTTP_400_BAD_REQUEST,
        "expected_re_status": "failed",
        "raise_exception": True,
    },
    {
        "id": "error2",
        "currency_id": 1,
        "provider_no": "invalid",
        "price": 1002,
        "expected_status": status.HTTP_400_BAD_REQUEST,
        "expected_re_status": "failed",
        "raise_exception": True,
    },
]


class ArticleIntegrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        Currency.objects.create(currency_id="USD", currency_name="dola")
        Currency.objects.create(currency_id="NGN", currency_name="naira")
        self.provider = Provider.objects.create(provider_name="dola")

    @patch("app.views.logger", logging.getLogger("test_logger"))
    def test_create_article(self):
        for data in test_data:
            article_data = {
                "currency_id": data["currency_id"],
                "provider_no": data["provider_no"],
                "price": data["price"],
            }

            response = self.client.post(
                reverse("app:article"),
                data=JSONRenderer().render(article_data),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, data["expected_status"])
            self.assertEqual(response.data["status"], data["expected_re_status"])
