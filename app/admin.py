from django.contrib import admin
from app.models import Article, Currency, Provider


class DefaultAdmin(admin.ModelAdmin):
    ordering = ("-updated_at",)


@admin.register(Article)
class ArticleAdmin(DefaultAdmin):
    list_display = (
        "article_no",
        "article",
        "provider",
        "price",
        "created_at",
        "updated_at",
    )
    search_fields = [
        "article__currency_id",
        "provider__provider_no",
        "article_no",
    ]
    readonly_fields = ("article_no",)


class CurrencyAdmin(DefaultAdmin):
    list_display = ("currency_id", "currency_name", "created_at", "updated_at")
    search_fields = [
        "currency_name",
        "currency_id",
    ]


class ProviderAdmin(DefaultAdmin):
    list_display = ("provider_no", "provider_name", "created_at", "updated_at")
    search_fields = [
        "provider_name",
        "provider_no",
    ]
    readonly_fields = ("provider_no",)


admin.site.register(Provider, ProviderAdmin)
admin.site.register(Currency, CurrencyAdmin)
