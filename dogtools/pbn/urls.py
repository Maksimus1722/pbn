from django.urls import path
from . import views

urlpatterns = [
    path("", views.Blog.as_view(), name="blog"),
    path("<slug:category_slug>/", views.Category.as_view(), name="category"),
    path("<slug:category_slug>/<slug:slug>/", views.Article.as_view(), name="article"),
]
