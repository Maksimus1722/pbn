import re
from django_filters.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
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
                "pbn/main.html",
                context=data,
            )
        data = base_function_404(host, request)
        if data["valid"]:
            return render(request, "errs/404.html", status=404, context=data)
        return HttpResponseNotFound()


class OtherPage(View):
    """Отображение других страниц и параллельно проверка мембран"""

    def get(self, request, *args, **kwargs):
        host = re.sub(r":.*", "", self.request.get_host())
        page_slug = self.kwargs["slug"]
        connect = ConnectDB(host)
        data = connect.get_info_other_page(page_slug)
        if data["valid"]:
            return render(request, "pbn/other_page.html", context=data)
        data = connect.get_membrans_link(page_slug)
        if data["valid"]:
            user_agent = self.request.META.get("HTTP_USER_AGENT", "Неизвестно")
            if re.search(r"google|yandex", user_agent, re.I):
                return redirect(data["link_money_site"], permanent=True)
            else:
                return redirect(self.request._current_scheme_host, permanent=True)
        data = base_function_404(host, request)
        if data["valid"]:
            return render(request, "errs/404.html", status=404, context=data)
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
            return render(request, "errs/404.html", status=404, context=data)
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
            return render(request, "errs/404.html", status=404, context=data)
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
        return render(request, "errs/404.html", status=404, context=data)
    return HttpResponseNotFound()
