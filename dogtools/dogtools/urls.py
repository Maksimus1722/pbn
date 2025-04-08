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

urlpatterns = [
    path("", view.MainPage.as_view(), name="main_page"),
    path("admin/", admin.site.urls),
    path("robots.txt", view.Robots.as_view(), name="robots"),
    path("sitemap.xml", view.Sitemap.as_view(), name="sitemap"),
    # списки всех редиректов
    path("blog/test14/", view.GeneralRedirect.as_view(), name="redirect"),
    # конец списку редиректов
    path("blog/", include("pbn.urls")),
    path("<slug:slug>/", view.OtherPage.as_view(), name="other_page"),
    path("ckeditor/", include("ckeditor_uploader.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = view.handler404
