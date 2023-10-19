from rest_framework import serializers
import logging
from app.models import Article, Currency, Provider
from django.db import IntegrityError, transaction

logger = logging.getLogger("main")


class ProviderSerializer(serializers.ModelSerializer):
    provider_no = serializers.CharField(read_only=True)

    class Meta:
        model = Provider
        exclude = ["created_at", "updated_at", "is_deleted"]

    def validate(self, data):
        if not data:
            raise serializers.ValidationError("Provider name cannot be empty")
        return data

    def create(self, validated_data):
        try:
            return Provider.objects.create(**validated_data)
        except IntegrityError as ex:
            if "unique constraint" in str(ex.args):
                raise serializers.ValidationError(
                    "Provider with this name already exists"
                ) from ex
        except Exception as ef:
            logger.error("An error occurred: %s", ef, exc_info=True)
            raise serializers.ValidationError("Oops! Something went wrong") from ef

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                provider = Provider.objects.select_for_update().get(
                    provider_no=instance.pk
                )
                for key, value in validated_data.items():
                    if hasattr(provider, key):  # prevent Error
                        setattr(provider, key, value)
                    else:
                        raise serializers.ValidationError(f"Invalid field: {key}")
                provider.save()
        except IntegrityError as ex:
            if "unique constraint" in str(ex.args):
                raise serializers.ValidationError(
                    "Provider with this name already exists"
                ) from ex
        except serializers.ValidationError as ve:
            message = ve.detail.get("error", [])
            raise serializers.ValidationError(message) from ve
        except Exception as ef:
            logger.error("An error occurred: %s", ef, exc_info=True)
            raise serializers.ValidationError("Oops! Something went wrong") from ef

        return instance


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        exclude = ["created_at", "updated_at", "is_deleted"]

    def validate(self, data):
        if not data.get("currency_name"):
            raise serializers.ValidationError("Currency name cannot be empty")
        return data

    def create(self, validated_data):
        try:
            return Currency.objects.create(**validated_data)
        except IntegrityError as ex:
            if "unique constraint" in str(ex.args):
                raise serializers.ValidationError(
                    "Currency with this data already exists"
                ) from ex
        except Exception as ef:
            logger.error("An error occurred: %s", ef, exc_info=True)
            raise serializers.ValidationError("Oops! Something went wrong") from ef

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                currency = Currency.objects.select_for_update().get(pk=instance.pk)
                for key, value in validated_data.items():
                    if hasattr(currency, key):
                        setattr(currency, key, value)
                currency.save()
        except IntegrityError as ex:
            if "unique constraint" in str(ex.args):
                raise serializers.ValidationError(
                    "Currency with this data already exists"
                ) from ex
        except Exception as ef:
            logger.error("An error occurred: %s", ef, exc_info=True)
            raise serializers.ValidationError("Oops! Something went wrong") from ef

        return instance
