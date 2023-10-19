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

    def create(self, validated_data):
        try:
            claim = Claim.objects.select_for_update().get(id=instance.pk)

            for key, value in validated_data.items():
                setattr(claim, key, value)
            claim.save()
            claim_approver, _ = ClaimApprover.objects.get_or_create(
                claim=claim, approver=user, status=validated_data.get("status")
            )
            claim_approver.save()

            logger.info(
                f"email in api claim update began for recipient: {instance.requester.email}"
            )
        except IntegrityError as exc:
            logger.error("An error occurred: %s", exc)
            if "unique constraint" in str(exc.args):
                raise serializers.ValidationError(
                    "Currency name already exists"
                ) from exc
        except Exception as ex:
            logger.error("An error occurred: %s", ex)
            transaction.set_rollback(True)
            raise serializers.ValidationError(
                "Error encountered while updating status. Please try again"
            ) from ex
        return instance


class ArticleSerializer(serializers.ModelSerializer):
    article = CurrencySerializer()
    provider = ProviderSerializer()
    date_created = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ["article_no", "article", "provider", "price", "date_created"]

    def get_date_created(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
