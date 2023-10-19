from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import logging
from app.custom_response import CustomAPIResponse
from app.models import Currency, Provider
from app.serializers import CurrencySerializer, ProviderSerializer
from rest_framework.exceptions import ValidationError

logger = logging.getLogger("main")


class ProviderView(CreateAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

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
    queryset = Provider.objects.all()

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
            logger.error(f"Exception in currency get: {ex}", exc_info=True)
            message = ex.args[0]

        response = CustomAPIResponse(message, status_code, re_status)
        return response.send()


class CurrencyDetailView(APIView):
    """
    Retrieve, update and delete currency
    """

    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()

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
