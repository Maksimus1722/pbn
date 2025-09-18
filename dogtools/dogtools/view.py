import re
from django_filters.views import View
from django.http import HttpResponsePermanentRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse
from .scripts.database_tools import ConnectDB
from .scripts.list_hosts import redirects_map


## Мета-данные страницы ошибки
title = "Несуществующая страница"
description = "По данному адресу страница не существует. Попробуйте ввести другой адрес"
keywords = "страница ошибки"


class MainPage(View):
    """Отображение главное страницы"""

    def get(self, request, *args, **kwargs):
        host = re.sub(r":.*", "", self.request.get_host())
        data = ConnectDB(host)
        data = data.get_info_main_page()
        if data["valid"]:
            return render(
                request,
                f"pbn/{data['template']}/main.html",
                context=data,
            )
        data = base_function_404(host, request)
        if data["valid"]:
            return render(
                request,
                f"pbn/{data['template']}/errs/404.html",
                status=404,
                context=data,
            )
        return HttpResponseNotFound()


class OtherPage(View):
    """Отображение других страниц и параллельно проверка мембран"""

    def get(self, request, *args, **kwargs):
        host = re.sub(r":.*", "", self.request.get_host())
        page_slug = self.kwargs["slug"]
        connect = ConnectDB(host)
        data = connect.get_info_other_page(page_slug)
        if data["valid"]:
            return render(
                request, f"pbn/{data['template']}/other_page.html", context=data
            )
        data = connect.get_membrans_link(page_slug)
        if data["valid"]:
            user_agent = self.request.META.get("HTTP_USER_AGENT", "Неизвестно")
            if re.search(r"google|yandex", user_agent, re.I):
                return redirect(data["link_money_site"], permanent=True)
            else:
                return redirect(self.request._current_scheme_host, permanent=True)
        data = base_function_404(host, request)
        if data["valid"]:
            return render(
                request,
                f"pbn/{data['template']}/errs/404.html",
                status=404,
                context=data,
            )
        return HttpResponseNotFound()


class Author(View):
    def get(self, request, *args, **kwargs):
        host = re.sub(r":.*", "", self.request.get_host())
        page_slug = self.kwargs["slug"]
        connect = ConnectDB(host)
        data = connect.get_author(page_slug)
        if data["valid"]:
            return render(request, f"pbn/{data['template']}/author.html", context=data)
        data = base_function_404(host, request)
        if data["valid"]:
            return render(
                request,
                f"pbn/{data['template']}/errs/404.html",
                status=404,
                context=data,
            )
        return HttpResponseNotFound()


class ListAuthors(View):
    def get(self, request, *args, **kwargs):
        host = re.sub(r":.*", "", self.request.get_host())
        connect = ConnectDB(host)
        data = connect.get_all_authors()
        if data["valid"]:
            return render(request, f"pbn/{data['template']}/authors.html", context=data)
        data = base_function_404(host, request)
        if data["valid"]:
            return render(
                request,
                f"pbn/{data['template']}/errs/404.html",
                status=404,
                context=data,
            )
        return HttpResponseNotFound()


class Robots(View):
    """Получение robots.txt"""

    def get(self, request, *args, **kwargs):
        return render(
            request,
            "robots/robots.txt",
            content_type="text/plain",
        )


class Sitemap(View):
    """Формирование sitemap.xml"""

    def get(self, request, *args, **kwargs):
        host = re.sub(r":.*", "", self.request.get_host())
        data = ConnectDB(host)
        data = data.get_sitemap()
        if data["valid"]:
            return render(
                request,
                "sitemap/sitemap.xml",
                context=data,
                content_type="application/xml",
            )
        data = base_function_404(host, request)
        if data["valid"]:
            return render(
                request,
                f"pbn/{data['template']}/errs/404.html",
                status=404,
                context=data,
            )
        return HttpResponseNotFound()


class GeneralRedirect(View):
    """Отработка списка редиректов из админки"""

    def get(self, request, *args, **kwargs):
        host = re.sub(r":.*", "", self.request.get_host())
        path = request.path
        url_redirect = redirects_map[host].get(path)
        if url_redirect:
            return redirect(url_redirect, permanent=True)
        data = base_function_404(host, request)
        if data["valid"]:
            return render(
                request,
                f"pbn/{data['template']}/errs/404.html",
                status=404,
                context=data,
            )
        return HttpResponseNotFound()


class SearchResults(View):
    def get(self, request, *args, **kwargs):
        text_search = request.GET.get("text_search")
        if text_search:
            url = reverse("search") + f"?text={text_search}"
            return HttpResponsePermanentRedirect(url)
        else:
            host = re.sub(r":.*", "", self.request.get_host())
            text = request.GET.get("text") if request.GET.get("text") else ""
            connect = ConnectDB(host)
            data = connect.get_search_article(text)
            data["text_search"] = text
        if data["valid"]:
            data.update(
                {
                    "title": f"Результаты поиска на сайте {host}",
                    "description": f"Поиск на сайте {host} по ключевым фразам",
                }
            )
            return render(request, f"pbn/{data['template']}/search.html", context=data)
        else:
            data = base_function_404(host, request)
            if data["valid"]:
                return render(
                    request,
                    f"pbn/{data['template']}/errs/404.html",
                    status=404,
                    context=data,
                )
        return HttpResponseNotFound()


class Services(View):
    def get(self, request, *args, **kwargs):
        host = re.sub(r":.*", "", self.request.get_host())
        connect = ConnectDB(host)
        data = connect.get_services()
        if data["valid"]:
            return render(
                request, f"pbn/{data['template']}/services.html", context=data
            )
        data = base_function_404(host, request)
        if data["valid"]:
            return render(
                request,
                f"pbn/{data['template']}/errs/404.html",
                status=404,
                context=data,
            )
        return HttpResponseNotFound()


class OneService(View):
    def get(self, request, *args, **kwargs):
        host = re.sub(r":.*", "", self.request.get_host())
        page_slug = self.kwargs["slug"]
        connect = ConnectDB(host)
        data = connect.get_one_servise(page_slug)
        if data["valid"]:
            return render(request, f"pbn/{data['template']}/author.html", context=data)
        data = base_function_404(host, request)
        if data["valid"]:
            return render(
                request,
                f"pbn/{data['template']}/errs/404.html",
                status=404,
                context=data,
            )
        return HttpResponseNotFound()


def base_function_404(host, request) -> dict:
    """Получени кастомной 404 ошибки"""
    data = ConnectDB(host)
    data = data.get_info_404()
    data.update(
        {
            "title": title,
            "description": description,
            "keywords": keywords,
            "url": request._current_scheme_host + request.path,
        }
    )
    return data


# Просто нужна стандартная функция 404, если ничего не отработало
def handler404(request, exception):
    host = re.sub(r":.*", "", request.get_host())
    data = base_function_404(host, request)
    if data["valid"]:
        return render(
            request, f"pbn/{data['template']}/errs/404.html", status=404, context=data
        )
    return HttpResponseNotFound()
