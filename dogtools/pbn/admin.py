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
    MainSlider,
    Service,
    Price,
    ConstructorTextService,
    Actions,
    Galery,
    Questions,
    BenifitsCompany,
    Cases,
    Review,
    HowWork,
    DescriptionService,
)


admin.site.site_header = "Админ-панель для управления сайтами"
admin.site.index_title = "Рабочая панель"


class MembransLinksInline(admin.TabularInline):
    model = LinksMembrans
    extra = 1


class RedirectLinksInline(admin.TabularInline):
    model = LinksRedirects
    extra = 1


class MainSliderInline(admin.StackedInline):
    model = MainSlider
    extra = 1


class PriceInline(admin.TabularInline):
    model = Price
    extra = 0
    fields = ["name", "price_name"]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        fields_to_widen = [
            "name",
        ]
        for field_name in fields_to_widen:
            form.base_fields[field_name].widget.attrs.update(
                {
                    "style": "width: 60%;",
                }
            )
        return form


class ConstructorTextService(admin.StackedInline):
    model = ConstructorTextService
    extra = 0


class ActionsDomains(admin.StackedInline):
    model = Actions
    extra = 0


class GaleryDomains(admin.StackedInline):
    model = Galery
    extra = 0


class QuestionService(admin.StackedInline):
    model = Questions
    extra = 0


class BenifitsCompanyDomains(admin.StackedInline):
    model = BenifitsCompany
    extra = 0


class CasesDomains(admin.StackedInline):
    model = Cases
    extra = 0


class ReviewDomain(admin.StackedInline):
    model = Review
    extra = 0


class HowworkDomain(admin.StackedInline):
    model = HowWork
    extra = 0


class DescriptionServiceService(admin.StackedInline):
    model = DescriptionService
    extra = 0


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
                )
            },
        ),
        (
            "Счетчики и вебмастера",
            {
                "fields": (
                    "yandex_webmaster",
                    "google_webmaster",
                    "yandex_metrika",
                    "google_analytics",
                )
            },
        ),
        (
            "Заполнение главной страницы",
            {
                "fields": (
                    "title",
                    "description",
                    "keywords",
                    "h1",
                    "main_text",
                    "extra_subtitle",
                    "extra_text",
                    "extra_picture",
                )
            },
        ),
        (
            "Дополнительная информация в сквозных блоках",
            {
                "fields": (
                    "name_site",
                    "info_footer",
                    "year_start",
                    "text_policy",
                )
            },
        ),
        (
            "Контактная информация (для всех коммерческих шаблонов)",
            {
                "fields": (
                    "emal_start",
                    "work_time",
                    "region",
                    "street",
                    "phone",
                    "telegram",
                )
            },
        ),
        (
            "Данные главной страницы блога (используется во всех шаблонах)",
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
            "Данные страницы авторов (используется в шаблонах: «Блог-2», «Блог-3», «Услуги-1»)",
            {
                "fields": (
                    "authors_title",
                    "authors_description",
                    "authors_keywords",
                )
            },
        ),
        (
            "Данные страницы услуги (используется в коммерческих шаблонах)",
            {
                "fields": (
                    "service_title",
                    "service_description",
                    "service_text",
                )
            },
        ),
        (
            "Названия инфо-раздела на коммереческих шаблонах",
            {"fields": ("name_info",)},
        ),
    )
    inlines = [
        MainSliderInline,
        RedirectLinksInline,
        MembransLinksInline,
        ActionsDomains,
        GaleryDomains,
        BenifitsCompanyDomains,
        CasesDomains,
        ReviewDomain,
        HowworkDomain,
    ]
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
            "name_site",
            "info_footer",
            "authors_title",
            "authors_description",
            "authors_keywords",
            "service_title",
            "service_description",
            "extra_subtitle",
        ]
        for field_name in fields_to_widen:
            form.base_fields[field_name].widget.attrs.update(
                {
                    "style": "width: 60%;",
                }
            )
        fields_to_small = ["emal_start"]
        for field_name in fields_to_small:
            form.base_fields[field_name].widget.attrs.update(
                {
                    "style": "width: 10%;",
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
    list_filter = [
        "domain",
    ]
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
                    "expirense",
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


class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "sort", "domain", "slug"]
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
                    "sort",
                    "name",
                    "domain",
                    "slug",
                    "preview_picture",
                    "text_preview",
                    "icon_preview",
                    "one_text",
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
        (
            "Заголовки столбцов цен",
            {
                "fields": (
                    "name_table_price",
                    "value_table_price",
                )
            },
        ),
        (
            "Акция",
            {
                "fields": (
                    "action_name",
                    "action_text",
                    "action_value",
                )
            },
        ),
    )
    inlines = [
        PriceInline,
        ConstructorTextService,
        QuestionService,
        DescriptionServiceService,
    ]

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


# Register your models here.
admin.site.register(Domains, DomainsAdmin)
admin.site.register(Article, ArticlesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(OtherPage, OtherPageAdmin)
admin.site.register(Author, authorAdmin)
admin.site.register(Service, ServiceAdmin)
