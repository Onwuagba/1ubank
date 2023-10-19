from django.urls import path
from app.views import CurrencyDetailView, CurrencyView, ProviderDetailView, ProviderView

app_name = "app"

# providers, articles, currencies

urlpatterns = [
    # path("articles/", ArticleView.as_view(), name="articles"),
    path("providers/", ProviderView.as_view(), name="providers"),
    path("providers/<str:id>/", ProviderDetailView.as_view(), name="provider-detail"),
    path("currency/", CurrencyView.as_view(), name="currency"),
    path("currency/<str:id>/", CurrencyDetailView.as_view(), name="currency-detail"),
]
