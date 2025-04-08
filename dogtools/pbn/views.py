from django_filters.views import View
from django.shortcuts import render
from django.http import HttpResponseNotFound
import re
from .scripts.database_pbn import ConnectDB

# Create your views here.
## Мета-данные страницы ошибки
title = "Несуществующая страница"
description = "По данному адресу страница не существует. Попробуйте ввести другой адрес"
keywords = "страница ошибки"


class Blog(View):
    def get(self, request, *args, **kwargs):
        host = re.sub(r":.*", "", self.request.get_host())
        data = ConnectDB(host)
        data = data.get_all_arcticle_for_blog()
        if data["valid"]:
            return render(
                request,
                "pbn/blog.html",
                context=data,
            )
        else:
            data = ConnectDB(host)
            data = data.get_info_404()
            if data["valid"]:
                data.update(
                    {
                        "title": title,
                        "description": description,
                        "keywords": keywords,
                        "url": self.request._current_scheme_host + self.request.path,
                    }
                )
                return render(request, "errs/404.html", status=404, context=data)
            else:
                return HttpResponseNotFound()


class Category(View):
    def get(self, request, *args, **kwargs):
        host = re.sub(r":.*", "", self.request.get_host())
        data = ConnectDB(host)
        data = data.get_article_category(slug=self.kwargs["category_slug"])
        if data["valid"]:
            return render(
                request,
                "pbn/category.html",
                context=data,
            )
        else:
            data = ConnectDB(host)
            data = data.get_info_404()
            if data["valid"]:
                data.update(
                    {
                        "title": title,
                        "description": description,
                        "keywords": keywords,
                        "url": self.request._current_scheme_host + self.request.path,
                    }
                )
                return render(request, "errs/404.html", status=404, context=data)
            else:
                return HttpResponseNotFound()


class Article(View):
    def get(self, request, *args, **kwargs):
        host = re.sub(r":.*", "", self.request.get_host())
        data = ConnectDB(host)
        data = data.get_article(
            article_slug=self.kwargs["slug"], category_slug=self.kwargs["category_slug"]
        )
        if data["valid"]:
            return render(
                request,
                "pbn/article.html",
                context=data,
            )
        else:
            data = ConnectDB(host)
            data = data.get_info_404()
            if data["valid"]:
                data.update(
                    {
                        "title": title,
                        "description": description,
                        "keywords": keywords,
                        "url": self.request._current_scheme_host + self.request.path,
                    }
                )
                return render(request, "errs/404.html", status=404, context=data)
            else:
                return HttpResponseNotFound()
