from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import logging
from app.custom_response import CustomAPIResponse
from app.models import Provider
from app.serializers import ProviderSerializer
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
