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
    ("blog_fourth", "Блог-4"),
    ("service_1", "Услуги-1"),
    ("service_2", "Услуги-2"),
    ("service_3", "Услуги-3"),
]

CHOICES_YEAR_START = [
    ("2013", "2013"),
    ("2014", "2014"),
    ("2015", "2015"),
    ("2016", "2016"),
    ("2017", "2017"),
    ("2018", "2018"),
    ("2019", "2019"),
    ("2020", "2020"),
    ("2021", "2021"),
    ("2022", "2022"),
    ("2023", "2023"),
    ("2024", "2024"),
]


TYPE_BLOCK = [
    ("text", "Текст"),
    ("picture_right", "Текст + картинка справа"),
    ("picture_left", "Текст + картинка слева"),
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
    google_webmaster = models.CharField(
        max_length=150,
        default="",
        blank=True,
        verbose_name="Номер Google Search Console",
        help_text="Например: WQIWvovWZPf97NwMWKDEBnYOKZevVnd3YC0H6Sl5vNs",
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
        help_text="Для всех шаблонов",
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
    telegram = models.CharField(
        max_length=100,
        default="",
        verbose_name="Телеграм",
        blank=True,
        help_text="Для всех коммерческих шаблонов. Формат: my_name",
    )
    region = models.CharField(
        max_length=50,
        default="",
        verbose_name="Город расположения",
        blank=True,
        help_text="Используется для микроразметки. Например: Москва",
    )
    street = models.CharField(
        max_length=50,
        default="",
        verbose_name="Адрес (без города)",
        blank=True,
        help_text="Используется для микроразметки. Например: Полежаевская дом 1",
    )
    work_time = models.CharField(
        max_length=50,
        default="",
        blank=True,
        verbose_name="График работы",
        help_text="Используется для всех коммерческих шаблонов",
    )
    extra_text = RichTextUploadingField(
        default="",
        blank=True,
        verbose_name="Дополнительный текст на главной",
        help_text="Используется для шаблонов: услуги-1",
    )
    extra_subtitle = models.CharField(
        max_length=100,
        default="",
        blank=True,
        verbose_name="Подзаголовок 2-ого текста главной",
        help_text="Используется для шаблонов: услуги-1",
    )
    extra_picture = models.ImageField(
        upload_to="static/pbn/img",
        null=True,
        blank=True,
        verbose_name="Дополнительное изображение на главной",
        help_text="Используется для шаблонов: услуги-1 (пропорции 3x2)",
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
    text_policy = RichTextUploadingField(
        default="",
        blank=True,
        verbose_name="Текст страницы - Политика конфиденциальности",
        help_text="Используется для всех коммерческих шаблонов",
    )

    service_title = models.CharField(
        max_length=200,
        default="",
        blank=True,
        verbose_name="Title для страницы: все услуги",
        help_text="Используется для коммерческих шаблонов",
    )
    service_description = models.CharField(
        max_length=300,
        default="",
        blank=True,
        verbose_name="Desription для страницы: все услуги",
        help_text="Используется для коммерческих шаблонов",
    )
    service_text = RichTextUploadingField(
        default="",
        blank=True,
        verbose_name="Текст страницы - все услуги",
        help_text="Используется для всех коммерческих шаблонов",
    )
    name_info = models.CharField(
        max_length=100,
        default="",
        blank=True,
        verbose_name="Название инфо-раздела в коммерческих шаблонах",
        help_text="Используется для коммерческих шаблонов (новости, статьи, публикации и т.д.)",
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
    expirense = models.IntegerField(
        default=1, verbose_name="Опыт автора", help_text="Для шаблонов: коммерческий-2"
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


class Service(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name="Название услуги",
        help_text="Он же пойдет в H1 и в ссылку в меню",
    )
    sort = models.IntegerField(
        default=100,
        verbose_name="Сортировка",
        help_text="Чем ближе к нулю,тем выше",
    )
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
    preview_picture = models.ImageField(
        upload_to="static/pbn/img",
        null=True,
        verbose_name="Картинка-превью",
        help_text="размер 600x300",
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
    name_table_price = models.CharField(
        max_length=300,
        default="",
        blank=True,
        verbose_name="Название столбца с услугами",
        help_text="Например: Наименование",
    )
    value_table_price = models.CharField(
        max_length=300,
        default="",
        blank=True,
        verbose_name="Наименование столбца с ценами на услуги",
        help_text="Например: Стоимость руб за м2",
    )
    action_name = models.CharField(
        max_length=300,
        default="",
        blank=True,
        verbose_name="Заголовок акции для услуги",
        help_text="Шаблоны: коммерческий-2,3",
    )
    action_text = RichTextUploadingField(
        verbose_name="Текст-акции",
        default="",
        help_text="Шаблоны: коммерческий-2,3",
        blank=True,
    )
    action_value = models.IntegerField(
        default=10,
        verbose_name="Величина скидки",
        help_text="Шаблоны: коммерческий-2,3",
    )
    icon_preview = models.CharField(
        max_length=100,
        default="",
        blank=True,
        verbose_name="Символ UTF-8",
        help_text="Шаблоны: коммерческий-3 (например  🎉)",
    )

    text_preview = models.CharField(
        max_length=500,
        default="",
        blank=True,
        verbose_name="Превью-текст для услуги",
        help_text="Шаблоны: коммерческий-3",
    )

    one_text = RichTextUploadingField(
        verbose_name="Единственный текстовый блок",
        default="",
        help_text="Шаблоны: коммерческий-3",
        blank=True,
    )

    class Meta:
        verbose_name = "Услугу"
        verbose_name_plural = "Услуги"

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)[:100]
        super(Service, self).save(*args, **kwargs)

    def get_url(self):
        return reverse("service", args=[self.slug])

    def __str__(self):
        return f"{self.domain} | {self.name}"


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


class Price(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        verbose_name="Услуга",
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название позиции",
        help_text="Например: резка стали",
        default="",
    )

    price_name = models.IntegerField(
        verbose_name="Цена",
        help_text="200",
        default="",
    )

    class Meta:
        verbose_name = "Набор цен"
        verbose_name_plural = "Позиция - цена"

    def __str__(self):
        return f"{self.name}"


class MainSlider(models.Model):
    domain = models.ForeignKey(
        Domains,
        on_delete=models.PROTECT,
        verbose_name="Домен",
    )
    sort = models.IntegerField(
        default=100,
        verbose_name="Сортировка",
        help_text="Чем ближе к нулю,тем выше",
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название слайда",
        help_text="Например: Супер-технология по фильтрации воды",
        default="",
    )
    text = models.CharField(
        max_length=300,
        verbose_name="Текстовый анонс",
        help_text="Например: Дарим 30% скидку до конца месяца на фильтры для воды",
        default="",
    )
    preview_picture = models.ImageField(
        upload_to="static/pbn/img",
        null=True,
        verbose_name="Картинка-слайда",
        help_text="размер 1350x900",
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
    link = models.CharField(
        max_length=100,
        verbose_name="Прозвольная ссылка",
        help_text="Например: /service/name1",
        default="",
    )

    class Meta:
        verbose_name = "Слайдер"
        verbose_name_plural = "Слайдер (коммерческий шаблон 1)"

    def __str__(self):
        return f"{self.name}"


class ConstructorTextService(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        verbose_name="Услуга",
    )
    type_block = models.CharField(
        max_length=100,
        choices=TYPE_BLOCK,
        default="text",
        verbose_name="Тип блока",
    )
    sort = models.IntegerField(
        default=10,
        verbose_name="Сортировка",
        help_text="Чем ближе к нулю,тем выше",
    )
    place_price = models.BooleanField(
        default=True, verbose_name="Расположить до блока цен"
    )
    picture = models.ImageField(
        upload_to="static/pbn/img",
        null=True,
        blank=True,
        verbose_name="Картинка-блока",
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
    subtitle = models.CharField(
        max_length=300,
        default="",
        blank=True,
        verbose_name="Подзаголовок H2-блока",
    )
    text = RichTextUploadingField(verbose_name="Текст", default="", blank=True)

    class Meta:
        verbose_name = "Блок"
        verbose_name_plural = "Блок"

    def __str__(self):
        return f"{self.subtitle}"


class Actions(models.Model):
    domain = models.ForeignKey(
        Domains,
        on_delete=models.PROTECT,
        verbose_name="Домен",
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Заголовок Акции",
        help_text="Например: Выгода до 20% на ручную мойку",
        default="",
    )
    picture = models.ImageField(
        upload_to="static/pbn/img",
        null=True,
        verbose_name="Картинка-",
        help_text="размер 1312x736",
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
    sort = models.IntegerField(
        default=100,
        verbose_name="Сортировка",
        help_text="Чем ближе к нулю,тем выше",
    )

    class Meta:
        verbose_name = "вариант акции"
        verbose_name_plural = "Акция (шаблоны: коммерческий-2)"

    def __str__(self):
        return f"{self.name}"


class Galery(models.Model):
    domain = models.ForeignKey(
        Domains,
        on_delete=models.PROTECT,
        verbose_name="Домен",
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Название картинки",
        help_text="Не отображается на сайте",
        default="",
    )
    picture = models.ImageField(
        upload_to="static/pbn/img",
        null=True,
        verbose_name="Картинка-",
        help_text="размер 1312x736",
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
    sort = models.IntegerField(
        default=100,
        verbose_name="Сортировка",
        help_text="Чем ближе к нулю,тем выше",
    )

    class Meta:
        verbose_name = "вариант картинки"
        verbose_name_plural = "Картинки галерии (шаблоны: коммерческий-2)"

    def __str__(self):
        return f"{self.name}"


class Questions(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        verbose_name="Услуга",
    )
    question = models.CharField(
        max_length=300,
        verbose_name="Вопрос",
        help_text="Например: как починить автомобиль?",
        default="",
    )
    answer = RichTextUploadingField(verbose_name="Ответ", default="", blank=True)
    sort = models.IntegerField(
        default=100,
        verbose_name="Сортировка",
        help_text="Чем ближе к нулю,тем выше",
    )

    class Meta:
        verbose_name = "Вопрос-ответ"
        verbose_name_plural = "Вопрос - ответ"

    def __str__(self):
        return f"{self.question}"


class BenifitsCompany(models.Model):
    domain = models.ForeignKey(
        Domains,
        on_delete=models.PROTECT,
        verbose_name="Домен",
    )
    sort = models.IntegerField(
        default=100,
        verbose_name="Сортировка",
        help_text="Чем ближе к нулю,тем выше",
    )
    name = models.CharField(
        max_length=300,
        verbose_name="Название",
        help_text="Например: Экспертиза",
        default="",
    )
    text = models.CharField(
        max_length=150,
        verbose_name="Описание преимущества",
        default="",
        blank=True,
        help_text="Например: 10 лет опыта в сфере строительства (не более 150 символов)",
    )

    icon = models.CharField(
        max_length=100,
        verbose_name="Символов UTF-8",
        help_text="Например:  🎉",
        default="",
    )

    class Meta:
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества (коммерческие шаблоны: 3)"

    def __str__(self):
        return f"{self.name}"


class Cases(models.Model):
    domain = models.ForeignKey(
        Domains,
        on_delete=models.PROTECT,
        verbose_name="Домен",
    )
    sort = models.IntegerField(
        default=100,
        verbose_name="Сортировка",
        help_text="Чем ближе к нулю,тем выше",
    )
    name = models.CharField(
        max_length=300,
        verbose_name="Название",
        help_text="Например: Оптимизация бизнес процессов",
        default="",
    )
    text = models.CharField(
        max_length=150,
        verbose_name="Описание кейса",
        default="",
        blank=True,
        help_text="Например: Реализовали комплексный проект по автоматизации розничной сети из 50+ магазинов с интеграцией всех систем.",
    )
    category_case = models.CharField(
        max_length=150,
        verbose_name="Категория кейса",
        default="",
        blank=True,
        help_text="Например: Трансформация",
    )
    image = models.ImageField(
        upload_to="static/pbn/img",
        null=True,
        verbose_name="Картинка кейса",
        help_text="размер 440x320",
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

    class Meta:
        verbose_name = "Кейсы"
        verbose_name_plural = "Кейс (коммерческие шаблоны: 3)"

    def __str__(self):
        return f"{self.name}"


class Review(models.Model):
    domain = models.ForeignKey(
        Domains,
        on_delete=models.PROTECT,
        verbose_name="Домен",
    )
    sort = models.IntegerField(
        default=100,
        verbose_name="Сортировка",
        help_text="Чем ближе к нулю,тем выше",
    )
    author = models.CharField(
        max_length=300,
        verbose_name="Автор",
        help_text="Например: Иван Иванов",
        default="",
    )
    post = models.CharField(
        max_length=150,
        verbose_name="Должность",
        default="",
        blank=True,
        help_text="Например: Операционный директор СЕО-Импульс.",
    )
    text = RichTextUploadingField(verbose_name="Текст отзыва", default="", blank=True)
    image = models.ImageField(
        upload_to="static/pbn/img",
        null=True,
        verbose_name="Фото автора",
        help_text="размер 56x56",
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

    class Meta:
        verbose_name = "Отзывы"
        verbose_name_plural = "Отзыв (коммерческие шаблоны: 3)"

    def __str__(self):
        return f"{self.author}"


class HowWork(models.Model):
    domain = models.ForeignKey(
        Domains,
        on_delete=models.PROTECT,
        verbose_name="Домен",
    )
    sort = models.IntegerField(
        default=100,
        verbose_name="Сортировка",
        help_text="Чем ближе к нулю,тем выше",
    )
    name = models.CharField(
        max_length=300,
        verbose_name="Названи этапа",
        help_text="Например: Анализ",
        default="",
    )
    text = models.CharField(
        max_length=150,
        verbose_name="Описание этапа",
        default="",
        blank=True,
        help_text="Например: Изучаем ваш бизнес, цели и текущую ситуацию",
    )

    class Meta:
        verbose_name = "Шаг"
        verbose_name_plural = "Шаги (коммерческие шаблоны: 3)"

    def __str__(self):
        return f"{self.name}"


class DescriptionService(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        verbose_name="Услуга",
    )
    sort = models.IntegerField(
        default=100,
        verbose_name="Сортировка",
        help_text="Чем ближе к нулю,тем выше",
    )
    name = models.CharField(
        max_length=300,
        verbose_name="Тезис",
        help_text="Например: Стратегический анализ",
        default="",
    )
    text = RichTextUploadingField(
        verbose_name="Описание тезиса",
        default="",
        help_text="Например: Комплексные программы обучения для повышения квалификации сотрудников и развития команды.",
        blank=True,
    )
    icon = models.CharField(
        max_length=100,
        verbose_name="Символов UTF-8",
        help_text="Например:  🎉",
        default="",
    )

    class Meta:
        verbose_name = "Тезис"
        verbose_name_plural = "Тезисы (коммерческие шаблоны: 3)"

    def __str__(self):
        return f"{self.name}"
