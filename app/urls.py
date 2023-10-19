from django.urls import path
from app.views import ProviderDetailView, ProviderView

app_name = "app"

# providers, articles, currencies

urlpatterns = [
    # path("articles/", ArticleView.as_view(), name="articles"),
    path("providers/", ProviderView.as_view(), name="providers"),
    path("providers/<str:id>/", ProviderDetailView.as_view(), name="provider-detail"),
]
