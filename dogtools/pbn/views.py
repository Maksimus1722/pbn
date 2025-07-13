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
    """Отображение страницы блога"""

    def get(self, request, *args, **kwargs):
        host = re.sub(r":.*", "", self.request.get_host())
        connect = ConnectDB(host)
        data = connect.get_all_arcticle_for_blog()
        if data["valid"]:
            return render(
                request,
                f"pbn/{data['template']}/blog.html",
                context=data,
            )
        data = connect.get_info_404()
        if data["valid"]:
            data.update(
                {
                    "title": title,
                    "description": description,
                    "keywords": keywords,
                    "url": self.request._current_scheme_host + self.request.path,
                }
            )
            return render(
                request,
                f"pbn/{data['template']}/errs/404.html",
                status=404,
                context=data,
            )
        return HttpResponseNotFound()


class Category(View):
    """Отображение рубрики блога"""

    def get(self, request, *args, **kwargs):
        host = re.sub(r":.*", "", self.request.get_host())
        connect = ConnectDB(host)
        data = connect.get_article_category(self.kwargs["category_slug"])
        if data["valid"]:
            return render(
                request,
                f"pbn/{data['template']}/category.html",
                context=data,
            )
        data = connect.get_info_404()
        if data["valid"]:
            data.update(
                {
                    "title": title,
                    "description": description,
                    "keywords": keywords,
                    "url": self.request._current_scheme_host + self.request.path,
                }
            )
            return render(
                request,
                f"pbn/{data['template']}/errs/404.html",
                status=404,
                context=data,
            )
        return HttpResponseNotFound()


class Article(View):
    """Отображение конкретной статьи"""

    def get(self, request, *args, **kwargs):
        host = re.sub(r":.*", "", self.request.get_host())
        connect = ConnectDB(host)
        data = connect.get_article(
            article_slug=self.kwargs["slug"], category_slug=self.kwargs["category_slug"]
        )
        if data["valid"]:
            connect.add_count_view_article(data["id_article"], data["page_view"])
            data["list_top_articles"] = connect.get_top_articles(data["domain_id"])
            if data["list_top_articles"]:
                return render(
                    request,
                    f"pbn/{data['template']}/article.html",
                    context=data,
                )
        data = connect.get_info_404()
        if data["valid"]:
            data.update(
                {
                    "title": title,
                    "description": description,
                    "keywords": keywords,
                    "url": self.request._current_scheme_host + self.request.path,
                }
            )
            return render(
                request,
                f"pbn/{data['template']}/errs/404.html",
                status=404,
                context=data,
            )
        return HttpResponseNotFound()
