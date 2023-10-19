from django.shortcuts import render

# Create your views here.
class ArticleView():
    def get(self, request):
        return render(request, "app/articles.html")