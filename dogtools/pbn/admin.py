from django.contrib import admin
from .models import Domains, Article, Category, OtherPage, MembransLinks


admin.site.site_header = "Админ-панель для управления сайтами"
admin.site.index_title = "Рабочая панель"


class MembransLinksInline(admin.TabularInline):
    model = MembransLinks
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
            {"fields": ("last_mod", "domain", "logo", "favicon", "h1", "main_text")},
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
    )
    inlines = [MembransLinksInline]
    readonly_fields = ("last_mod",)


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
                    "last_mod",
                    "active",
                    "created",
                    "name",
                    "domain",
                    "category",
                    "slug",
                )
            },
        ),
        ("Мета-данные", {"fields": ("title", "description", "keywords")}),
        ("Содержимое", {"fields": ("img_preview", "text_preview", "text")}),
    )
    readonly_fields = ("last_mod",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "sort", "domain", "category_slug"]
    list_editable = ["sort"]
    list_per_page = 20
    search_fields = [
        "name__istartswith",
    ]
    ordering = ["name", "sort"]
    list_filter = [
        "domain",
    ]
    fieldsets = (
        (
            "Основное",
            {"fields": ("last_mod", "sort", "name", "domain", "category_slug")},
        ),
        ("Мета-данные", {"fields": ("title", "description", "keywords", "h1")}),
    )
    readonly_fields = ("last_mod",)


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


# Register your models here.
admin.site.register(Domains, DomainsAdmin)
admin.site.register(Article, ArticlesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(OtherPage, OtherPageAdmin)
