import datetime
from django.db import models
from pytils.translit import slugify
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MinLengthValidator, FileExtensionValidator


CHOICES_TEMPLATES = [
    ("first", "Блог-1"),
    ("second", "Блог-2"),
    ("blog_third", "Блог-3"),
]

CHOICES_YEAR_START = [
    ("2013", "2013"),
    ("2014", "2014"),
    ("2015", "2015"),
    ("2016", "2016"),
    ("2017", "2017"),
    ("2018", "2018"),
    ("2019", "2019"),
    ("2020", "2021"),
    ("2022", "2022"),
    ("2023", "2023"),
    ("2024", "2024"),
]


# Create your models here.
class Domains(models.Model):
    domain = models.CharField(
        max_length=100,
        verbose_name="Домен",
        help_text="формат site.ru",
        unique=True,
    )
    title = models.CharField(
        max_length=250, default="", verbose_name="Title главной страницы"
    )
    description = models.CharField(
        max_length=500,
        default="",
        verbose_name="Meta-description главной страницы",
    )
    keywords = models.CharField(
        max_length=500, default="", verbose_name="Meta-keywords главной страницы"
    )
    h1 = models.CharField(
        max_length=250, default="", verbose_name="Заголовок главной страницы"
    )
    main_text = RichTextUploadingField(
        verbose_name="Текст на главной",
        validators=[MinLengthValidator(300)],
        help_text="Не менее 300 символов",
    )
    logo = models.ImageField(
        upload_to="static/pbn/img",
        null=True,
        verbose_name="Логотип сайта",
        help_text="Форматы: png, jpg, jpeg",
        validators=[
            FileExtensionValidator(
                allowed_extensions=(
                    "png",
                    "jpg",
                    "jpeg",
                )
            )
        ],
    )
    favicon = models.ImageField(
        upload_to="static/pbn/favicons",
        null=True,
        verbose_name="favicon",
        help_text="фавикон в формате .ico",
        validators=[FileExtensionValidator(allowed_extensions=("ico",))],
    )
    blog_title = models.CharField(
        max_length=250, default="", verbose_name="Title страницы блога"
    )
    blog_description = models.CharField(
        max_length=500, default="", verbose_name="Description страницы блога"
    )
    blog_keywords = models.CharField(
        max_length=250, default="", verbose_name="Meta-keywords страницы блога"
    )
    blog_name = models.CharField(
        max_length=250, default="", verbose_name="H1 страницы блога"
    )
    last_mod = models.DateTimeField(
        auto_now=True,
        verbose_name="Последнее обновление",
    )
    google_analytics = models.CharField(
        max_length=100,
        default="",
        blank=True,
        verbose_name="Счетчик Google Analytics",
        help_text="Например: G-8C1FN89PWR",
    )
    yandex_metrika = models.CharField(
        max_length=100,
        default="",
        blank=True,
        verbose_name="Счетчик Yandex metrika",
        help_text="Например: 94153371",
    )
    yandex_webmaster = models.CharField(
        max_length=150,
        default="",
        blank=True,
        verbose_name="Номер Яндекс.Вебмастера",
        help_text="Например: ffbe325dc3c6cf09",
    )
    template = models.CharField(
        choices=CHOICES_TEMPLATES,
        max_length=150,
        default="first",
        verbose_name="Выбор шаблона",
    )
    authors_title = models.CharField(
        max_length=300,
        default="",
        blank=True,
        verbose_name="Title страницы авторов",
        help_text="Заполнять, если такая страница есть в шаблоне",
    )
    authors_description = models.CharField(
        max_length=300,
        default="",
        blank=True,
        verbose_name="Description страницы авторов",
        help_text="Заполнять, если такая страница есть в шаблоне",
    )
    authors_keywords = models.CharField(
        max_length=300,
        default="",
        blank=True,
        verbose_name="Keywords страницы авторов",
        help_text="Заполнять, если такая страница есть в шаблоне",
    )
    info_footer = models.CharField(
        max_length=300,
        default="",
        blank=True,
        verbose_name="Текст о сайте в футере",
        help_text="Шаблоны: «Блог-2», «Блог-3»",
    )
    name_site = models.CharField(
        max_length=100,
        default="",
        blank=True,
        verbose_name="Название сайта в шапке",
        help_text="Шаблоны: «Блог-3»",
    )
    year_start = models.CharField(
        max_length=50,
        choices=CHOICES_YEAR_START,
        default="2015",
        verbose_name="Год запуска проекта",
    )
    emal_start = models.CharField(
        max_length=50,
        default="info",
        verbose_name="Имя ящика",
        help_text="Для всех шаблонов. Например: info или help (домен подтянется сам)",
    )
    phone = models.CharField(
        max_length=50,
        default="",
        verbose_name="Телефон",
        blank=True,
        help_text="Для шаблонов:«Блог-3» и всех коммерческих. В удобочитаемом виде: +7-(495)-233-23-23",
    )

    class Meta:
        verbose_name = "Домен"
        verbose_name_plural = "Домены"

    def __str__(self):
        return f"{self.domain}"


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    title = models.CharField(max_length=250, default="", verbose_name="Title")
    description = models.CharField(
        max_length=500,
        default="",
        verbose_name="Meta-description",
    )
    h1 = models.CharField(max_length=250, default="", verbose_name="Заголовок H1")
    domain = models.ForeignKey(
        Domains,
        on_delete=models.PROTECT,
        verbose_name="Домен",
    )
    keywords = models.CharField(
        max_length=250, default="", verbose_name="Meta-keywords"
    )
    category_slug = models.SlugField(
        max_length=100,
        null=False,
        db_index=True,
        verbose_name="URL",
        help_text="При создании поставьте любой символ. Поле заполнится автоматически.",
    )
    sort = models.IntegerField(
        default=100,
        verbose_name="Сортировка",
        help_text="Чем ближе к нулю,тем выше",
    )
    last_mod = models.DateTimeField(
        auto_now=True,
        verbose_name="Последнее обновление",
    )
    img_preview = models.ImageField(
        upload_to="static/pbn/img",
        verbose_name="Картинка-превью",
        help_text="Для некоторых шаблонов",
        validators=[
            FileExtensionValidator(
                allowed_extensions=(
                    "png",
                    "jpg",
                    "jpeg",
                )
            )
        ],
        blank=True,
        default="",
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.category_slug = slugify(self.name)[:100]
        super(Category, self).save(*args, **kwargs)

    def get_url(self):
        return reverse("category", args=[self.slug])

    def __str__(self):
        return f"{self.domain} | {self.name}"

    class Meta:
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"


class Author(models.Model):
    name = models.CharField(max_length=250, verbose_name="Имя автора")
    spec = models.CharField(
        max_length=300,
        verbose_name="Специализация автора",
        help_text="Не более 300 символов",
    )
    preview = RichTextUploadingField(
        verbose_name="Информация об авторе",
    )
    title = models.CharField(max_length=250, verbose_name="Title")
    description = models.CharField(max_length=500, verbose_name="Meta-description")
    keywords = models.CharField(
        max_length=500, default="", verbose_name="Meta-keywords"
    )
    slug = models.SlugField(
        max_length=100,
        null=False,
        db_index=True,
        verbose_name="URL",
        help_text="При создании поставьте любой символ. Поле заполнится автоматически.",
    )
    img_preview = models.ImageField(
        upload_to="static/pbn/img",
        null=True,
        verbose_name="Фото автора",
        validators=[
            FileExtensionValidator(
                allowed_extensions=(
                    "png",
                    "jpg",
                    "jpeg",
                )
            )
        ],
    )
    domain = models.ForeignKey(
        Domains,
        on_delete=models.PROTECT,
        verbose_name="Домен",
        default="",
    )
    last_mod = models.DateTimeField(
        auto_now=True,
        verbose_name="Последнее обновление",
    )

    class Meta:
        verbose_name = "Автора"
        verbose_name_plural = "Авторы"
        ordering = ("name",)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)[:100]
        super(Author, self).save(*args, **kwargs)

    def get_url(self):
        return reverse("author", args=[self.slug])

    def __str__(self):
        return f"{self.name} - {self.domain}"


class Article(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")
    domain = models.ForeignKey(
        Domains,
        on_delete=models.PROTECT,
        verbose_name="Домен",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="Категория",
        default="",
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        verbose_name="Автор",
        default=None,
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=250, verbose_name="Title")
    description = models.CharField(max_length=500, verbose_name="Meta-description")
    keywords = models.CharField(
        max_length=500, default="", verbose_name="Meta-keywords"
    )
    slug = models.SlugField(
        max_length=100,
        null=False,
        db_index=True,
        verbose_name="URL",
        help_text="При создании поставьте любой символ. Поле заполнится автоматически.",
    )
    img_preview = models.ImageField(
        upload_to="static/pbn/img",
        null=True,
        verbose_name="Картинка-превью",
        validators=[
            FileExtensionValidator(
                allowed_extensions=(
                    "png",
                    "jpg",
                    "jpeg",
                )
            )
        ],
    )
    text_preview = RichTextUploadingField(
        max_length=300,
        verbose_name="Текст-превью",
        default="",
        help_text="Не более 300 символов вместе с пробелами. Только текст и ссылки.",
    )
    created = models.DateField(
        default=datetime.datetime.now(), verbose_name="Дата создания"
    )
    text = RichTextUploadingField(
        verbose_name="Текст статьи",
        validators=[MinLengthValidator(300)],
        help_text="Не менее 300 символов",
    )
    active = models.BooleanField(default=True, verbose_name="Активность")
    last_mod = models.DateTimeField(
        auto_now=True,
        verbose_name="Последнее обновление",
    )
    page_view = models.IntegerField(default=0, verbose_name="Просмотры")
    time_read = models.IntegerField(default=1, verbose_name="Минут на прочтение")
    table_content = RichTextUploadingField(
        verbose_name="Содержание статьи",
        help_text="Маркированный список подзаголовков с якорями (необязательно)",
        default="",
        blank=True,
    )

    class Meta:
        verbose_name = "Статью"
        verbose_name_plural = "Статьи"

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)[:100]
        super(Article, self).save(*args, **kwargs)

    def get_url(self):
        return reverse("arcticle", args=[self.slug])

    def __str__(self):
        return f"{self.name}"


class OtherPage(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")
    domain = models.ForeignKey(
        Domains,
        on_delete=models.PROTECT,
        verbose_name="Домен",
    )
    slug = models.SlugField(
        max_length=100,
        null=False,
        db_index=True,
        verbose_name="URL",
        help_text="При создании поставьте любой символ. Поле заполнится автоматически.",
    )
    title = models.CharField(max_length=250, default="", verbose_name="Title")
    description = models.CharField(
        max_length=500,
        default="",
        verbose_name="Meta-description",
    )
    keywords = models.CharField(
        max_length=250, default="", verbose_name="Meta-keywords"
    )
    h1 = models.CharField(max_length=250, default="", verbose_name="Заголовок H1")
    text = RichTextUploadingField(verbose_name="Содержание", default="")
    sort = models.IntegerField(
        default=100,
        verbose_name="Сортировка",
        help_text="Чем ближе к нулю,тем выше",
    )
    last_mod = models.DateTimeField(
        auto_now=True,
        verbose_name="Последнее обновление",
    )

    class Meta:
        verbose_name = "Страницу"
        verbose_name_plural = "Другие страницы"

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)[:100]
        super(OtherPage, self).save(*args, **kwargs)

    def get_url(self):
        return reverse("page", args=[self.slug])

    def __str__(self):
        return f"{self.name}"


class LinksMembrans(models.Model):
    domain = models.ForeignKey(
        Domains,
        on_delete=models.PROTECT,
        verbose_name="Домен",
    )
    slug_user = models.CharField(
        max_length=100,
        verbose_name="URL-прокладки",
        help_text="Символный код ссылки-прокладки. Только латиница в нижним регистре и тире. Например: my-new-link",
        default="",
    )
    link_money_site = models.CharField(
        max_length=100,
        verbose_name="URL Money Site",
        help_text="URL финальной страницы на Money Site",
        default="",
    )

    class Meta:
        verbose_name = "Набор"
        verbose_name_plural = "Ссылки-прокладки"

    def __str__(self):
        return f"{self.slug_user}"


class LinksRedirects(models.Model):
    domain = models.ForeignKey(
        Domains,
        on_delete=models.PROTECT,
        verbose_name="Домен",
    )
    start_link = models.CharField(
        max_length=100,
        verbose_name="Откуда редирект",
        help_text="Начинается строго со знака /. Например /page.html или /page",
        default="",
    )
    finish_link = models.CharField(
        max_length=100,
        verbose_name="Куда редирект",
        help_text="Начинается строго со знака /. Например /page.html. Если редирект на главную, просто пишем - /.",
        default="",
    )

    class Meta:
        verbose_name = "Набор"
        verbose_name_plural = "Ссылки-редиректы"

    def __str__(self):
        return f"{self.start_link}"
