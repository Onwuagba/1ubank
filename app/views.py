from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import logging
from app.custom_response import CustomAPIResponse
from app.models import Article, Currency, Provider
from app.serializers import (
    ArticleDetailSerializer,
    ArticleSerializer,
    CurrencySerializer,
    ProviderSerializer,
)
from rest_framework.exceptions import ValidationError
from django.db import transaction

logger = logging.getLogger("main")


class ProviderView(CreateAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    http_method_names = ["get", "post"]

    def get(self, request, **kwargs):
        re_status = "failed"
        status_code = status.HTTP_400_BAD_REQUEST

        try:
            if qs := self.get_queryset():
                serializer = self.serializer_class(qs, many=True)
                message = serializer.data
                re_status = "success"
                status_code = status.HTTP_200_OK
            else:
                message = "No provider added yet"
        except Exception as ex:
            logger.error(f"Exception in provider get: {ex}")
            message = ex.args[0]

        response = CustomAPIResponse(message, status_code, re_status)
        return response.send()

    def post(self, request, *args, **kwargs):
        re_status = "failed"
        status_code = status.HTTP_400_BAD_REQUEST

        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            message = "Provider created successfully"
            re_status = "success"
            status_code = status.HTTP_201_CREATED
        except Exception as ex:
            logger.error(f"Exception in provider get: {ex}", exc_info=True)
            message = ex.args[0]

        response = CustomAPIResponse(message, status_code, re_status)
        return response.send()


class ProviderDetailView(APIView):
    """
    Retrieve, update and delete provider instance
    """

    serializer_class = ProviderSerializer
    http_method_names = ["get", "patch", "delete"]

    def get_object(self, provider_no):
        try:
            return Provider.objects.get(provider_no=provider_no)
        except Provider.DoesNotExist as e:
            raise ValidationError("Invalid provider id") from e

    def get(self, request, **kwargs):
        provider_no = kwargs.get("id")
        re_status = "failed"
        status_code = status.HTTP_400_BAD_REQUEST

        try:
            obj = self.get_object(provider_no)
            serializer = self.serializer_class(obj)
            message = serializer.data
            re_status = "success"
            status_code = status.HTTP_200_OK
        except Exception as ex:
            logger.error(f"Exception in provider detail get: {ex}")
            message = ex.args[0]

        response = CustomAPIResponse(message, status_code, re_status)
        return response.send()

    def patch(self, request, **kwargs):
        provider_no = kwargs.get("id")
        re_status = "failed"
        status_code = status.HTTP_400_BAD_REQUEST

        try:
            obj = self.get_object(provider_no)
            serializer = self.serializer_class(
                obj,
                data=request.data,
                partial=True,
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = "Provider updated successfully"
                re_status = "success"
                status_code = status.HTTP_200_OK
        except Exception as ex:
            logger.error(f"Exception in provider detail patch  {provider_no}: {ex}")
            message = ex.args[0]

        response = CustomAPIResponse(message, status_code, re_status)
        return response.send()

    def delete(self, request, **kwargs):
        provider_no = kwargs.get("id")
        re_status = "failed"
        status_code = status.HTTP_400_BAD_REQUEST

        try:
            obj = self.get_object(provider_no)
            obj.is_deleted = True
            obj.save()
            message = "Provider has been deleted successfully"
            re_status = "success"
            status_code = status.HTTP_200_OK
        except Exception as ex:
            logger.error(f"provider detail delete with id  {provider_no}: {ex}")
            message = ex.args[0]

        response = CustomAPIResponse(message, status_code, re_status)
        return response.send()


class CurrencyView(CreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    http_method_names = ["get", "post"]

    def get(self, request, **kwargs):
        re_status = "failed"
        status_code = status.HTTP_400_BAD_REQUEST

        try:
            if qs := self.get_queryset():
                serializer = self.serializer_class(qs, many=True)
                message = serializer.data
                re_status = "success"
                status_code = status.HTTP_200_OK
            else:
                message = "No currency added yet"
        except Exception as ex:
            logger.error(f"Exception in currency get: {ex}")
            message = ex.args[0]

        response = CustomAPIResponse(message, status_code, re_status)
        return response.send()

    def post(self, request, *args, **kwargs):
        re_status = "failed"
        status_code = status.HTTP_400_BAD_REQUEST

        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            message = "Currency created successfully"
            re_status = "success"
            status_code = status.HTTP_201_CREATED
        except Exception as ex:
            logger.error(f"Exception in currency post: {ex}", exc_info=True)
            message = ex.args[0]

        response = CustomAPIResponse(message, status_code, re_status)
        return response.send()


class CurrencyDetailView(APIView):
    """
    Retrieve, update and delete currency
    """

    serializer_class = CurrencySerializer
    http_method_names = ["get", "patch", "delete"]

    def get_object(self, currency_id):
        try:
            return Currency.objects.get(currency_id__iexact=currency_id)
        except Currency.DoesNotExist as e:
            raise ValidationError("Invalid currency id") from e

    def get(self, request, **kwargs):
        currency_id = kwargs.get("id")
        re_status = "failed"
        status_code = status.HTTP_400_BAD_REQUEST

        try:
            obj = self.get_object(currency_id)
            serializer = self.serializer_class(obj)
            message = serializer.data
            re_status = "success"
            status_code = status.HTTP_200_OK
        except Exception as ex:
            logger.error(f"Exception in currency detail get: {ex}")
            message = ex.args[0]

        response = CustomAPIResponse(message, status_code, re_status)
        return response.send()

    def patch(self, request, **kwargs):
        currency_id = kwargs.get("id")
        re_status = "failed"
        status_code = status.HTTP_400_BAD_REQUEST

        try:
            obj = self.get_object(currency_id)
            serializer = self.serializer_class(
                obj,
                data=request.data,
                partial=True,
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = "Currency updated successfully"
                re_status = "success"
                status_code = status.HTTP_200_OK
        except Exception as ex:
            logger.error(f"Exception in currency detail patch  {currency_id}: {ex}")
            message = ex.args[0]

        response = CustomAPIResponse(message, status_code, re_status)
        return response.send()

    def delete(self, request, **kwargs):
        currency_id = kwargs.get("id")
        re_status = "failed"
        status_code = status.HTTP_400_BAD_REQUEST

        try:
            obj = self.get_object(currency_id)
            obj.is_deleted = True
            obj.save()
            message = "Currency deleted successfully"
            re_status = "success"
            status_code = status.HTTP_200_OK
        except Exception as ex:
            logger.error(f"currency detail delete with id  {currency_id}: {ex}")
            message = ex.args[0]

        response = CustomAPIResponse(message, status_code, re_status)
        return response.send()


class ArticleView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    http_method_names = ["get", "post"]

    def get(self, request, *args):
        re_status = "failed"
        status_code = status.HTTP_400_BAD_REQUEST

        try:
            queryset = self.filter_queryset(self.get_queryset())
            if page := self.paginate_queryset(queryset):
                serializer = self.serializer_class(page, many=True)
                query_response = self.get_paginated_response(serializer.data)
                message = query_response.data
                re_status = "success"
                status_code = status.HTTP_200_OK
            else:
                message = "No article found"
        except Exception as ex:
            logger.error(f"Exception in article get: {ex}")
            message = ex.args[0]

        response = CustomAPIResponse(message, status_code, re_status)
        return response.send()

    # def post(self, request, *args, **kwargs):
    #     re_status = "failed"
    #     status_code = status.HTTP_400_BAD_REQUEST
    #     error = {}

    #     with transaction.atomic():
    #         try:
    #             currency_data = request.data.get("article")
    #             provider_data = request.data.get("provider")
    #             article_data = request.data

    #             currency_serializer = CurrencySerializer(data=currency_data)
    #             provider_serializer = ProviderSerializer(data=provider_data)
    #             article_serializer = ArticleSerializer(data=article_data)

    #             is_valid = all(
    #                 [
    #                     currency_serializer.is_valid(),
    #                     provider_serializer.is_valid(),
    #                     article_serializer.is_valid(),
    #                 ]
    #             )

    #             if is_valid:
    #                 currency = currency_serializer.save()
    #                 provider = provider_serializer.save()
    #                 if not currency and not provider:
    #                     error
    #                 article_serializer.save(article=currency, provider=provider)
    #                 message = "Article created successfully"
    #                 re_status = "success"
    #                 status_code = status.HTTP_201_CREATED

    #             message = {
    #                 "currency": currency_serializer.errors,
    #                 "provider": provider_serializer.errors,
    #                 "article": article_serializer.errors,
    #             }
    #         except Exception as ex:
    #             transaction.set_rollback(True)
    #             logger.error(f"Exception in article post: {ex}", exc_info=True)
    #             message = ex.args[0]

    #     response = CustomAPIResponse(message, status_code, re_status)
    #     return response.send()

    def check_currency(self, currency):
        try:
            return Currency.objects.get(currency_id__iexact=currency)
        except Currency.DoesNotExist as ex:
            raise ValidationError("Invalid currency id") from ex

    def check_provider(self, provider):
        try:
            return Provider.objects.get(provider_no=provider)
        except Provider.DoesNotExist as ex:
            raise ValidationError("Invalid provider id") from ex

    def post(self, request, *args, **kwargs):
        re_status = "failed"
        status_code = status.HTTP_400_BAD_REQUEST

        try:
            currency = self.check_currency(request.data.get("currency_id"))
            provider = self.check_provider(request.data.get("provider_no"))
            article_serializer = self.serializer_class(
                data={**request.data, "article": currency.pk, "provider": provider.pk}
            )
            article_serializer.is_valid(raise_exception=True)
            self.perform_create(article_serializer)
            message = "Article created successfully"
            re_status = "success"
            status_code = status.HTTP_201_CREATED
        except Exception as ex:
            logger.error(f"Exception in article post: {ex}", exc_info=True)
            message = ex.args[0]

        response = CustomAPIResponse(message, status_code, re_status)
        return response.send()


class ArticleDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleDetailSerializer
    http_method_names = ["get", "patch", "delete"]

    def get_object(self, article_no):
        try:
            return Article.objects.get(article_no=article_no)
        except Article.DoesNotExist as e:
            raise ValidationError("Invalid article number") from e

    def get(self, request, **kwargs):
        article_no = kwargs.get("art_num")
        re_status = "failed"
        status_code = status.HTTP_400_BAD_REQUEST

        try:
            obj = self.get_object(article_no)
            serializer = self.serializer_class(obj)
            message = serializer.data
            re_status = "success"
            status_code = status.HTTP_200_OK
        except Exception as ex:
            logger.error(f"Exception in article detail get: {ex}")
            message = ex.args[0]

        response = CustomAPIResponse(message, status_code, re_status)
        return response.send()

    def check_currency(self, currency):
        try:
            return Currency.objects.get(currency_id__iexact=currency)
        except Currency.DoesNotExist as ex:
            raise ValidationError("Invalid currency id") from ex

    def check_provider(self, provider):
        try:
            return Provider.objects.get(provider_no=provider)
        except Provider.DoesNotExist as ex:
            raise ValidationError("Invalid provider id") from ex

    def patch(self, request, *args, **kwargs):
        article_no = kwargs.get("art_num")
        re_status = "failed"
        status_code = status.HTTP_400_BAD_REQUEST

        try:
            currency_id = request.data.get("article_id")
            provider_no = request.data.get("provider_id")

            obj = self.get_object(article_no)
            data = {**request.data}

            if currency_id:
                currency = self.check_currency(currency_id)
                data["article"] = currency.pk
            if provider_no:
                provider = self.check_provider(provider_no)
                data["provider"] = provider.pk

            serializer = self.serializer_class(obj, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            message = "Article updated successfully"
            re_status = "success"
            status_code = status.HTTP_200_OK

        except Exception as ex:
            logger.error(f"Exception in article patch: {ex}", exc_info=True)
            message = ex.args[0]

        response = CustomAPIResponse(message, status_code, re_status)
        return response.send()

    def delete(self, request, **kwargs):
        article_no = kwargs.get("art_num")
        re_status = "failed"
        status_code = status.HTTP_400_BAD_REQUEST

        try:
            obj = self.get_object(article_no)
            obj.is_deleted = True
            obj.save()
            message = "Article deleted successfully"
            re_status = "success"
            status_code = status.HTTP_200_OK
        except Exception as ex:
            logger.error(f"article detail delete with id  {article_no}: {ex}")
            message = ex.args[0]

        response = CustomAPIResponse(message, status_code, re_status)
        return response.send()
