from django.urls import path
from app.views import (
    ArticleDetailView,
    ArticleView,
    CurrencyDetailView,
    CurrencyView,
    ProviderDetailView,
    ProviderView,
)

app_name = "app"

# providers, articles, currencies

urlpatterns = [
    path("providers/", ProviderView.as_view(), name="providers"),
    path("providers/<str:id>/", ProviderDetailView.as_view(), name="provider-detail"),
    path("currency/", CurrencyView.as_view(), name="currency"),
    path("currency/<str:id>/", CurrencyDetailView.as_view(), name="currency-detail"),
    path("articles/", ArticleView.as_view(), name="article"),
    path("articles/<int:art_num>/", ArticleDetailView.as_view(), name="article-detail"),
]
