from django.urls import path
from app.views import ArticleView

app_name = "app"

urlpatterns = [
    path("articles/", ArticleView.as_view(), name="articles"),
]
