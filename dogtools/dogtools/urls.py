"""
URL configuration for tools project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import view
from .scripts.list_hosts import redirects_map


urlpatterns = (
    [
        path(url[1:], view.GeneralRedirect.as_view(), name="redirect")
        for host in redirects_map
        for url in redirects_map[host]
    ]
    + [
        path("", view.MainPage.as_view(), name="main_page"),
        path("admin/", admin.site.urls),
        path("robots.txt", view.Robots.as_view(), name="robots"),
        path("sitemap.xml", view.Sitemap.as_view(), name="sitemap"),
        path("search/", view.SearchResults.as_view(), name="search"),
        path("blog/", include("pbn.urls")),
        path("authors/", view.ListAuthors.as_view(), name="list_authors"),
        path("authors/<slug:slug>/", view.Author.as_view(), name="author"),
        path("ckeditor/", include("ckeditor_uploader.urls")),
        path("<slug:slug>/", view.OtherPage.as_view(), name="other_page"),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

handler404 = view.handler404
