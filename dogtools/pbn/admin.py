from django.contrib import admin
from django.core.cache import cache
from .models import (
    Domains,
    Article,
    Category,
    OtherPage,
    LinksMembrans,
    LinksRedirects,
    Author,
)


admin.site.site_header = "Админ-панель для управления сайтами"
admin.site.index_title = "Рабочая панель"


class MembransLinksInline(admin.TabularInline):
    model = LinksMembrans
    extra = 1


class RedirectLinksInline(admin.TabularInline):
    model = LinksRedirects
    extra = 1


class DomainsAdmin(admin.ModelAdmin):
    list_display = [
        "domain",
        "title",
        "description",
        "keywords",
    ]
    list_editable = [
        "title",
        "description",
        "keywords",
    ]
    list_per_page = 20
    search_fields = [
        "domain__istartswith",
    ]
    ordering = ["domain"]
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "last_mod",
                    "domain",
                    "logo",
                    "favicon",
                    "template",
                    "google_analytics",
                    "yandex_metrika",
                    "yandex_webmaster",
                    "h1",
                    "main_text",
                )
            },
        ),
        ("Мета-данные", {"fields": ("title", "description", "keywords")}),
        (
            "Данные главной страницы блога",
            {
                "fields": (
                    "blog_title",
                    "blog_description",
                    "blog_keywords",
                    "blog_name",
                )
            },
        ),
        (
            "Данные страницы авторов",
            {
                "fields": (
                    "authors_title",
                    "authors_description",
                    "authors_keywords",
                )
            },
        ),
    )
    inlines = [RedirectLinksInline, MembransLinksInline]
    readonly_fields = ("last_mod",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        fields_to_widen = [
            "h1",
            "title",
            "description",
            "keywords",
            "blog_title",
            "blog_description",
            "blog_keywords",
            "blog_name",
        ]
        for field_name in fields_to_widen:
            form.base_fields[field_name].widget.attrs.update(
                {
                    "style": "width: 60%;",
                }
            )
        return form


class ArticlesAdmin(admin.ModelAdmin):
    list_display = ["name", "active", "domain", "category"]
    list_editable = [
        "active",
    ]
    list_per_page = 20
    search_fields = [
        "name__istartswith",
    ]
    ordering = ["name", "active"]
    list_filter = [
        "domain",
    ]
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "active",
                    "last_mod",
                    "page_view",
                    "created",
                    "name",
                    "domain",
                    "category",
                    "author",
                    "slug",
                )
            },
        ),
        ("Мета-данные", {"fields": ("title", "description", "keywords")}),
        (
            "Содержимое",
            {
                "fields": (
                    "time_read",
                    "img_preview",
                    "text_preview",
                    "table_content",
                    "text",
                )
            },
        ),
    )
    readonly_fields = ("last_mod", "page_view")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        fields_to_widen = [
            "name",
            "title",
            "description",
            "keywords",
        ]
        for field_name in fields_to_widen:
            form.base_fields[field_name].widget.attrs.update(
                {
                    "style": "width: 60%;",
                }
            )
        return form


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "sort", "domain", "category_slug"]
    list_editable = ["sort"]
    list_per_page = 20
    search_fields = [
        "name__istartswith",
    ]
    ordering = ["domain", "name"]
    list_filter = [
        "domain",
    ]
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "last_mod",
                    "sort",
                    "name",
                    "domain",
                    "category_slug",
                    "img_preview",
                )
            },
        ),
        ("Мета-данные", {"fields": ("title", "description", "keywords", "h1")}),
    )
    readonly_fields = ("last_mod",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        fields_to_widen = [
            "h1",
            "title",
            "description",
            "keywords",
        ]
        for field_name in fields_to_widen:
            form.base_fields[field_name].widget.attrs.update(
                {
                    "style": "width: 60%;",
                }
            )
        return form


class OtherPageAdmin(admin.ModelAdmin):
    """
    fields = [
        "sort",
        "name",
        "domain",
        "slug",
        "title",
        "description",
        "keywords",
        "h1",
        "text",
    ]
    """

    list_display = ["name", "id", "sort", "domain", "slug"]
    list_editable = [
        "sort",
    ]
    list_per_page = 20
    search_fields = [
        "name__istartswith",
    ]
    ordering = ["id", "name"]
    list_filter = [
        "domain",
    ]
    fieldsets = (
        ("Основное", {"fields": ("last_mod", "sort", "name", "domain", "slug")}),
        (
            "Мета-данные",
            {
                "fields": (
                    "title",
                    "description",
                    "keywords",
                )
            },
        ),
        ("Содержимое", {"fields": ("h1", "text")}),
    )
    readonly_fields = ("last_mod",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        fields_to_widen = [
            "h1",
            "title",
            "description",
            "keywords",
        ]
        for field_name in fields_to_widen:
            form.base_fields[field_name].widget.attrs.update(
                {
                    "style": "width: 60%;",
                }
            )
        return form


class authorAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "domain", "spec"]
    list_editable = ["slug", "domain", "spec"]
    list_per_page = 20
    search_fields = [
        "name__istartswith",
    ]
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "last_mod",
                    "name",
                    "spec",
                    "preview",
                    "slug",
                    "img_preview",
                    "domain",
                )
            },
        ),
        (
            "Мета-данные",
            {
                "fields": (
                    "title",
                    "description",
                    "keywords",
                )
            },
        ),
    )
    readonly_fields = ("last_mod",)


# Register your models here.
admin.site.register(Domains, DomainsAdmin)
admin.site.register(Article, ArticlesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(OtherPage, OtherPageAdmin)
admin.site.register(Author, authorAdmin)
