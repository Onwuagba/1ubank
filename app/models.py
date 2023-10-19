import contextlib
from django.db import IntegrityError, models
from django.db.models.query import QuerySet
from app.constant import CURRENCY_CODE
from django.db import transaction
from django.core.exceptions import ValidationError
import re
from django.db.models.functions import Upper


def validate_price(value):
    if not re.match(r"^\d+(\.\d{1,2})?$", str(value)):
        raise ValidationError("Price must be only numbers with(out) 2 decimal places.")


class CustomManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)  # soft delete

    objects = CustomManager()

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]


class Currency(BaseModel):
    currency_id = models.CharField(max_length=5, primary_key=True)
    currency_name = models.CharField(
        max_length=9,
        unique=True,
    )

    class Meta:
        verbose_name_plural = "Currencies"

        constraints = [
            models.UniqueConstraint(
                Upper("currency_name"), name="unique_currency_name_category"
            )
        ]

    def __str__(self) -> str:
        return str(self.currency_name)


class Provider(BaseModel):
    provider_no = models.CharField(primary_key=True)
    provider_name = models.CharField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            while True:
                try:
                    with transaction.atomic():
                        last_provider = Provider.objects.select_for_update().latest(
                            "created_at"
                        )
                        self.provider_no = str(
                            int(last_provider.provider_no) + 1
                        ).zfill(4)
                        break
                except Provider.DoesNotExist:
                    self.provider_no = "0001"
                    break
                except IntegrityError:
                    pass

        super(Provider, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.provider_name


class Article(BaseModel):
    article_no = models.IntegerField(primary_key=True, db_index=True)
    article = models.ForeignKey(Currency, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    # TODO: remove validator since decimalfield takes care of it
    price = models.DecimalField(
        max_digits=16, decimal_places=2, validators=[validate_price]
    )  # Here since price is independent of article. If price is tied to article, create a pivot table

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["article", "provider"], name="unique_article_provider"
            )
        ]

    def save(self, *args, **kwargs):
        if self._state.adding:
            while True:
                try:
                    with transaction.atomic():
                        last_obj = Article.objects.select_for_update().latest(
                            "created_at"
                        )
                        self.article_no = last_obj.article_no + 1
                        break
                except Article.DoesNotExist:
                    self.article_no = 101
                    break
                except IntegrityError:
                    pass
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{str(self.article_no)} - {str(self.article.currency_name)}"
