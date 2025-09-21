import sqlalchemy as sa, threading, datetime


class ConnectDB:
    def __init__(self, host):
        self.host = host
        self.dict_category = []
        self.dict_other_page = []
        self.list_services = []
        self.list_text_block = []
        self.list_prices = []
        self.connect_db = (
            "mysql+pymysql://max_shark:fdfde0fdf$@176.99.9.17:3306/pbn_crm"
        )

    def get_info_main_page(self) -> dict:
        """Получение инофрмации для главной страницы"""
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                domain_table = meta.tables["pbn_domains"]
                article_table = meta.tables["pbn_article"]
                category_table = meta.tables["pbn_category"]
                query = (
                    sa.select(
                        article_table.c.name,
                        article_table.c.slug,
                        article_table.c.img_preview,
                        article_table.c.created,
                        article_table.c.text_preview,
                        article_table.c.page_view,
                        article_table.c.time_read,
                        category_table.c.category_slug.label("category_slug"),
                        category_table.c.name.label("category_name"),
                        domain_table.c.id.label("domain_id"),
                        domain_table.c.domain.label("domain_domain"),
                        domain_table.c.logo.label("logo"),
                        domain_table.c.favicon.label("favicon"),
                        domain_table.c.title.label("title"),
                        domain_table.c.description.label("description"),
                        domain_table.c.keywords.label("keywords"),
                        domain_table.c.h1.label("h1"),
                        domain_table.c.main_text.label("main_text"),
                        domain_table.c.google_analytics.label("google_analytics"),
                        domain_table.c.yandex_metrika.label("yandex_metrika"),
                        domain_table.c.yandex_webmaster.label("yandex_webmaster"),
                        domain_table.c.google_webmaster.label("google_webmaster"),
                        domain_table.c.template.label("template"),
                        domain_table.c.name_site.label("name_site"),
                        domain_table.c.info_footer.label("info_footer"),
                        domain_table.c.year_start.label("year_start"),
                        domain_table.c.emal_start.label("emal_start"),
                        domain_table.c.phone.label("phone"),
                        domain_table.c.region.label("region"),
                        domain_table.c.street.label("street"),
                        domain_table.c.work_time.label("work_time"),
                        domain_table.c.telegram.label("telegram"),
                        domain_table.c.extra_text.label("extra_text"),
                        domain_table.c.extra_subtitle.label("extra_subtitle"),
                        domain_table.c.extra_picture.label("extra_picture"),
                        domain_table.c.text_policy.label("text_policy"),
                        domain_table.c.name_info.label("name_info"),
                    )
                    .select_from(
                        article_table.join(
                            category_table,
                            article_table.c.category_id == category_table.c.id,
                        ).join(
                            domain_table,
                            article_table.c.domain_id == domain_table.c.id,
                        )
                    )
                    .where(
                        domain_table.c.domain == self.host,
                        article_table.c.active == True,
                    )
                    .order_by(sa.desc(article_table.c.created))
                    .limit(24)
                )
                rs = con.execute(query).fetchall()
                if not rs:
                    data = {"valid": False}
                    return data
                first_rs = rs[0]
                data = {
                    "domain_id": first_rs.domain_id,
                    "domain_domain": first_rs.domain_domain,
                    "logo": first_rs.logo,
                    "favicon": first_rs.favicon,
                    "title": first_rs.title,
                    "description": first_rs.description,
                    "keywords": first_rs.keywords,
                    "h1": first_rs.h1,
                    "main_text": first_rs.main_text,
                    "google_analytics": first_rs.google_analytics,
                    "yandex_metrika": first_rs.yandex_metrika,
                    "yandex_webmaster": first_rs.yandex_webmaster,
                    "google_webmaster": first_rs.google_webmaster,
                    "template": first_rs.template,
                    "name_site": first_rs.name_site,
                    "info_footer": first_rs.info_footer,
                    "year_start": first_rs.year_start,
                    "emal_start": first_rs.emal_start,
                    "now_year": datetime.datetime.now().year,
                    "phone": first_rs.phone,
                    "phone_link": "+"
                    + "".join(list(filter(lambda x: x.isdigit(), first_rs.phone))),
                    "region": first_rs.region,
                    "street": first_rs.street,
                    "work_time": first_rs.work_time,
                    "telegram": first_rs.telegram,
                    "extra_text": first_rs.extra_text,
                    "extra_subtitle": first_rs.extra_subtitle,
                    "extra_picture": first_rs.extra_picture,
                    "text_policy": first_rs.text_policy,
                    "name_info": first_rs.name_info,
                    "list_articles": [
                        {
                            "name": row.name,
                            "slug": row.slug,
                            "category_slug": row.category_slug,
                            "img_preview": row.img_preview,
                            "created": row.created,
                            "text_preview": row.text_preview,
                            "page_view": row.page_view,
                            "time_read": row.time_read,
                            "category_name": row.category_name,
                        }
                        for row in rs
                    ],
                    "list_top_arcicle": [],
                }
            data["list_sliders"] = self._get_main_sliders(data["domain_id"])
            self._manage_get_otherpage_services_category(data["domain_id"]),
            if (
                self.dict_other_page["valid"]
                and self.list_services["valid"]
                and self.dict_category["valid"]
            ):
                data.update(
                    {
                        "valid": True,
                        "list_services": self.list_services["list_services"],
                        "list_other_page": self.dict_other_page["list_other_page"],
                        "list_category": self.dict_category["list_category"],
                    }
                )
                for category in data["list_category"]:
                    top_article_category = []
                    for article in data["list_articles"]:
                        if (
                            article["category_slug"] == category["slug"]
                            and len(top_article_category) < 3
                        ):
                            top_article_category.append(article)
                    data["list_top_arcicle"].append(
                        {
                            "name_category": category["name"],
                            "top_article_category": top_article_category,
                        }
                    )
            else:
                data = {"valid": False}
        except Exception as err:
            data = {"valid": False}
        finally:
            return data

    def get_info_other_page(self, slug: str) -> dict:
        """Другие страницы (не категории)"""
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                domain_table = meta.tables["pbn_domains"]
                otherpage_table = meta.tables["pbn_otherpage"]
                query = (
                    sa.select(
                        domain_table.c.logo,
                        domain_table.c.favicon,
                        domain_table.c.id,
                        domain_table.c.domain,
                        otherpage_table.c.name.label("name"),
                        otherpage_table.c.slug.label("slug"),
                        otherpage_table.c.description.label("description"),
                        otherpage_table.c.title.label("title"),
                        otherpage_table.c.h1.label("h1"),
                        otherpage_table.c.text.label("text"),
                        domain_table.c.google_analytics.label("google_analytics"),
                        domain_table.c.yandex_metrika.label("yandex_metrika"),
                        domain_table.c.yandex_webmaster.label("yandex_webmaster"),
                        domain_table.c.google_webmaster.label("google_webmaster"),
                        domain_table.c.template.label("template"),
                        domain_table.c.name_site.label("name_site"),
                        domain_table.c.info_footer.label("info_footer"),
                        domain_table.c.year_start.label("year_start"),
                        domain_table.c.emal_start.label("emal_start"),
                        domain_table.c.phone.label("phone"),
                        domain_table.c.region.label("region"),
                        domain_table.c.street.label("street"),
                        domain_table.c.work_time.label("work_time"),
                        domain_table.c.telegram.label("telegram"),
                        domain_table.c.name_info.label("name_info"),
                    )
                    .select_from(
                        otherpage_table.join(
                            domain_table,
                            otherpage_table.c.domain_id == domain_table.c.id,
                        )
                    )
                    .where(
                        domain_table.c.domain == self.host,
                        otherpage_table.c.slug == slug,
                    )
                )
                first_row = con.execute(query).fetchone()
                if not first_row:
                    data = {"valid": False}
                    return data
                data = {
                    "domain_id": first_row.id,
                    "logo": first_row.logo,
                    "favicon": first_row.favicon,
                    "domain_domain": first_row.domain,
                    "name": first_row.name,
                    "slug": first_row.slug,
                    "description": first_row.description,
                    "title": first_row.title,
                    "h1": first_row.h1,
                    "text": first_row.text,
                    "google_analytics": first_row.google_analytics,
                    "yandex_metrika": first_row.yandex_metrika,
                    "yandex_webmaster": first_row.yandex_webmaster,
                    "google_webmaster": first_row.google_webmaster,
                    "template": first_row.template,
                    "name_site": first_row.name_site,
                    "info_footer": first_row.info_footer,
                    "year_start": first_row.year_start,
                    "emal_start": first_row.emal_start,
                    "now_year": datetime.datetime.now().year,
                    "phone": first_row.phone,
                    "phone_link": "+"
                    + "".join(list(filter(lambda x: x.isdigit(), first_row.phone))),
                    "region": first_row.region,
                    "street": first_row.street,
                    "work_time": first_row.work_time,
                    "telegram": first_row.telegram,
                    "name_info": first_row.name_info,
                }
            self._manage_get_otherpage_services_category(data["domain_id"]),
            if (
                self.dict_other_page["valid"]
                and self.list_services["valid"]
                and self.dict_category["valid"]
            ):
                data.update(
                    {
                        "valid": True,
                        "list_services": self.list_services["list_services"],
                        "list_other_page": self.dict_other_page["list_other_page"],
                        "list_category": self.dict_category["list_category"],
                    }
                )
            else:
                data = {"valid": False}
        except Exception as err:
            data = {"valid": False}
        finally:
            return data

    def get_author(self, slug: str) -> dict:
        """Получаем информацию о конкретном авторе"""
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                domain_table = meta.tables["pbn_domains"]
                author_table = meta.tables["pbn_author"]
                article_table = meta.tables["pbn_article"]
                category_table = meta.tables["pbn_category"]
                query = (
                    sa.select(
                        article_table.c.name,
                        article_table.c.slug,
                        article_table.c.img_preview,
                        article_table.c.created,
                        article_table.c.time_read,
                        article_table.c.page_view,
                        article_table.c.text_preview,
                        author_table.c.name.label("author_name"),
                        author_table.c.slug.label("author_slug"),
                        author_table.c.description.label("description"),
                        author_table.c.title.label("title"),
                        author_table.c.keywords.label("keywords"),
                        author_table.c.spec.label("spec"),
                        author_table.c.preview.label("preview"),
                        author_table.c.img_preview.label("author_img_preview"),
                        author_table.c.id.label("author_id"),
                        domain_table.c.logo.label("logo"),
                        domain_table.c.favicon.label("favicon"),
                        domain_table.c.id.label("domain_id"),
                        domain_table.c.domain.label("domain"),
                        domain_table.c.google_analytics.label("google_analytics"),
                        domain_table.c.yandex_metrika.label("yandex_metrika"),
                        domain_table.c.yandex_webmaster.label("yandex_webmaster"),
                        domain_table.c.google_webmaster.label("google_webmaster"),
                        domain_table.c.template.label("template"),
                        domain_table.c.name_site.label("name_site"),
                        domain_table.c.info_footer.label("info_footer"),
                        domain_table.c.year_start.label("year_start"),
                        domain_table.c.emal_start.label("emal_start"),
                        domain_table.c.phone.label("phone"),
                        domain_table.c.region.label("region"),
                        domain_table.c.street.label("street"),
                        domain_table.c.work_time.label("work_time"),
                        domain_table.c.telegram.label("telegram"),
                        domain_table.c.name_info.label("name_info"),
                        category_table.c.category_slug.label("category_slug"),
                        category_table.c.name.label("category_name"),
                    )
                    .select_from(
                        article_table.join(
                            author_table,
                            article_table.c.author_id == author_table.c.id,
                        )
                        .join(
                            domain_table, article_table.c.domain_id == domain_table.c.id
                        )
                        .join(
                            category_table,
                            article_table.c.category_id == category_table.c.id,
                        )
                    )
                    .where(
                        author_table.c.slug == slug,
                        author_table.c.domain_id == domain_table.c.id,
                        article_table.c.active == True,
                    )
                )
                rs = con.execute(query).fetchall()
                if not rs:
                    data = {"valid": False}
                    return data
                first_rs = rs[0]
                data = {
                    "domain_id": first_rs.domain_id,
                    "logo": first_rs.logo,
                    "favicon": first_rs.favicon,
                    "domain": first_rs.domain,
                    "title": first_rs.title,
                    "google_analytics": first_rs.google_analytics,
                    "yandex_metrika": first_rs.yandex_metrika,
                    "yandex_webmaster": first_rs.yandex_webmaster,
                    "google_webmaster": first_rs.google_webmaster,
                    "template": first_rs.template,
                    "name_site": first_rs.name_site,
                    "info_footer": first_rs.info_footer,
                    "description": first_rs.description,
                    "keywords": first_rs.keywords,
                    "author_name": first_rs.author_name,
                    "spec": first_rs.spec,
                    "preview": first_rs.preview,
                    "author_img_preview": first_rs.author_img_preview,
                    "author_slug": first_rs.author_slug,
                    "year_start": first_rs.year_start,
                    "emal_start": first_rs.emal_start,
                    "now_year": datetime.datetime.now().year,
                    "phone": first_rs.phone,
                    "phone_link": "+"
                    + "".join(list(filter(lambda x: x.isdigit(), first_rs.phone))),
                    "region": first_rs.region,
                    "street": first_rs.street,
                    "work_time": first_rs.work_time,
                    "telegram": first_rs.telegram,
                    "name_info": first_rs.name_info,
                    "list_articles": [
                        {
                            "name": row.name,
                            "slug": row.slug,
                            "img_preview": row.img_preview,
                            "category_slug": row.category_slug,
                            "category_name": row.category_name,
                            "created": row.created,
                            "time_read": row.time_read,
                            "page_view": row.page_view,
                            "text_preview": row.text_preview,
                        }
                        for row in rs
                    ],
                }
            self._manage_get_otherpage_services_category(data["domain_id"]),
            if (
                self.dict_other_page["valid"]
                and self.list_services["valid"]
                and self.dict_category["valid"]
            ):
                data.update(
                    {
                        "valid": True,
                        "list_services": self.list_services["list_services"],
                        "list_other_page": self.dict_other_page["list_other_page"],
                        "list_category": self.dict_category["list_category"],
                    }
                )
            else:
                data = {"valid": False}
        except Exception as err:
            data = {"valid": False}
        finally:
            return data

    def get_all_authors(self) -> dict:
        """Получаем информацию обо всех авторах блога"""
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                domain_table = meta.tables["pbn_domains"]
                author_table = meta.tables["pbn_author"]
                query = (
                    sa.select(
                        author_table.c.name,
                        author_table.c.slug,
                        author_table.c.spec,
                        author_table.c.img_preview,
                        domain_table.c.logo.label("logo"),
                        domain_table.c.favicon.label("favicon"),
                        domain_table.c.id.label("domain_id"),
                        domain_table.c.domain.label("domain"),
                        domain_table.c.google_analytics.label("google_analytics"),
                        domain_table.c.yandex_metrika.label("yandex_metrika"),
                        domain_table.c.yandex_webmaster.label("yandex_webmaster"),
                        domain_table.c.google_webmaster.label("google_webmaster"),
                        domain_table.c.template.label("template"),
                        domain_table.c.authors_title.label("title"),
                        domain_table.c.authors_description.label("description"),
                        domain_table.c.authors_keywords.label("keywords"),
                        domain_table.c.name_site.label("name_site"),
                        domain_table.c.info_footer.label("info_footer"),
                        domain_table.c.year_start.label("year_start"),
                        domain_table.c.emal_start.label("emal_start"),
                        domain_table.c.phone.label("phone"),
                        domain_table.c.region.label("region"),
                        domain_table.c.street.label("street"),
                        domain_table.c.work_time.label("work_time"),
                        domain_table.c.telegram.label("telegram"),
                        domain_table.c.name_info.label("name_info"),
                    )
                    .select_from(
                        author_table.join(
                            domain_table,
                            author_table.c.domain_id == domain_table.c.id,
                        )
                    )
                    .where(
                        domain_table.c.domain == self.host,
                    )
                )
                rs = con.execute(query).fetchall()
                if not rs:
                    data = {"valid": False}
                    return data
                first_rs = rs[0]
                data = {
                    "domain_id": first_rs.domain_id,
                    "logo": first_rs.logo,
                    "favicon": first_rs.favicon,
                    "domain": first_rs.domain,
                    "google_analytics": first_rs.google_analytics,
                    "yandex_metrika": first_rs.yandex_metrika,
                    "yandex_webmaster": first_rs.yandex_webmaster,
                    "google_webmaster": first_rs.google_webmaster,
                    "template": first_rs.template,
                    "name_site": first_rs.name_site,
                    "info_footer": first_rs.info_footer,
                    "title": first_rs.title,
                    "description": first_rs.description,
                    "keywords": first_rs.keywords,
                    "year_start": first_rs.year_start,
                    "emal_start": first_rs.emal_start,
                    "now_year": datetime.datetime.now().year,
                    "phone": first_rs.phone,
                    "phone_link": "+"
                    + "".join(list(filter(lambda x: x.isdigit(), first_rs.phone))),
                    "region": first_rs.region,
                    "street": first_rs.street,
                    "work_time": first_rs.work_time,
                    "telegram": first_rs.telegram,
                    "name_info": first_rs.name_info,
                    "list_authors": [
                        {
                            "name": row.name,
                            "slug": row.slug,
                            "img_preview": row.img_preview,
                            "spec": row.spec,
                        }
                        for row in rs
                    ],
                }
            self._manage_get_otherpage_services_category(data["domain_id"]),
            if (
                self.dict_other_page["valid"]
                and self.list_services["valid"]
                and self.dict_category["valid"]
            ):
                data.update(
                    {
                        "valid": True,
                        "list_services": self.list_services["list_services"],
                        "list_other_page": self.dict_other_page["list_other_page"],
                        "list_category": self.dict_category["list_category"],
                    }
                )
            else:
                data = {"valid": False}
        except Exception as err:
            data = {"valid": False}
        finally:
            return data

    def get_info_404(self) -> dict:
        """Отработка 404 ошибок"""
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                domain_table = meta.tables["pbn_domains"]
                query = sa.select(
                    domain_table.c.id,
                    domain_table.c.domain,
                    domain_table.c.logo,
                    domain_table.c.favicon,
                    domain_table.c.google_analytics.label("google_analytics"),
                    domain_table.c.yandex_metrika.label("yandex_metrika"),
                    domain_table.c.yandex_webmaster.label("yandex_webmaster"),
                    domain_table.c.google_webmaster.label("google_webmaster"),
                    domain_table.c.template.label("template"),
                    domain_table.c.name_site.label("name_site"),
                    domain_table.c.info_footer.label("info_footer"),
                    domain_table.c.year_start.label("year_start"),
                    domain_table.c.emal_start.label("emal_start"),
                    domain_table.c.phone.label("phone"),
                    domain_table.c.region.label("region"),
                    domain_table.c.street.label("street"),
                    domain_table.c.work_time.label("work_time"),
                    domain_table.c.telegram.label("telegram"),
                    domain_table.c.name_info.label("name_info"),
                ).where(domain_table.c.domain == self.host)
                rs = con.execute(query).fetchone()
                data = {
                    "domain_id": rs.id,
                    "domain_domain": rs.domain,
                    "logo": rs.logo,
                    "favicon": rs.favicon,
                    "google_analytics": rs.google_analytics,
                    "yandex_metrika": rs.yandex_metrika,
                    "yandex_webmaster": rs.yandex_webmaster,
                    "google_webmaster": rs.google_webmaster,
                    "template": rs.template,
                    "name_site": rs.name_site,
                    "info_footer": rs.info_footer,
                    "year_start": rs.year_start,
                    "emal_start": rs.emal_start,
                    "now_year": datetime.datetime.now().year,
                    "phone": rs.phone,
                    "phone_link": "+"
                    + "".join(list(filter(lambda x: x.isdigit(), rs.phone))),
                    "region": rs.region,
                    "street": rs.street,
                    "work_time": rs.work_time,
                    "telegram": rs.telegram,
                    "name_info": rs.name_info,
                }
                self._manage_get_otherpage_services_category(data["domain_id"]),
            if (
                self.dict_other_page["valid"]
                and self.list_services["valid"]
                and self.dict_category["valid"]
            ):
                data.update(
                    {
                        "valid": True,
                        "list_services": self.list_services["list_services"],
                        "list_other_page": self.dict_other_page["list_other_page"],
                        "list_category": self.dict_category["list_category"],
                    }
                )
            else:
                data = {"valid": False}
        except Exception as err:
            data = {"valid": False}
        finally:
            return data

    def get_membrans_link(self, page_slug: str) -> dict:
        """Получение мембранных ссылок (перенапрваление на мани-сайт)"""
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                domain_table = meta.tables["pbn_domains"]
                membran_table = meta.tables["pbn_linksmembrans"]
                query = (
                    sa.select(
                        domain_table.c.logo,
                        domain_table.c.favicon,
                        domain_table.c.id,
                        domain_table.c.domain,
                        membran_table.c.link_money_site.label("link_money_site"),
                    )
                    .select_from(
                        membran_table.join(
                            domain_table,
                            membran_table.c.domain_id == domain_table.c.id,
                        )
                    )
                    .where(
                        domain_table.c.domain == self.host,
                        membran_table.c.slug_user == page_slug,
                    )
                )
                first_rs = con.execute(query).fetchone()
                if not first_rs:
                    data = {"valid": False}
                    return data
                data = {
                    "valid": True,
                    "domain_id": first_rs.id,
                    "logo": first_rs.logo,
                    "favicon": first_rs.favicon,
                    "domain_domain": first_rs.domain,
                    "link_money_site": first_rs.link_money_site,
                }
        except Exception as err:
            data = {"valid": False}
        finally:
            return data

    def get_search_article(self, word_search: str) -> dict:
        """Поиск статей на странице поиска"""
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                domain_table = meta.tables["pbn_domains"]
                article_table = meta.tables["pbn_article"]
                category_table = meta.tables["pbn_category"]
                query = (
                    sa.select(
                        article_table.c.id,
                        article_table.c.name,
                        article_table.c.slug,
                        article_table.c.title,
                        article_table.c.created,
                        article_table.c.time_read,
                        article_table.c.page_view,
                        article_table.c.img_preview,
                        article_table.c.text_preview,
                        category_table.c.id.label("category_id"),
                        category_table.c.category_slug.label("category_slug"),
                        category_table.c.name.label("category_name"),
                        domain_table.c.id.label("domain_id"),
                        domain_table.c.logo.label("logo"),
                        domain_table.c.favicon.label("favicon"),
                        domain_table.c.domain.label("domain_domain"),
                        domain_table.c.google_analytics.label("google_analytics"),
                        domain_table.c.yandex_metrika.label("yandex_metrika"),
                        domain_table.c.yandex_webmaster.label("yandex_webmaster"),
                        domain_table.c.template.label("template"),
                        domain_table.c.name_site.label("name_site"),
                        domain_table.c.info_footer.label("info_footer"),
                        domain_table.c.year_start.label("year_start"),
                        domain_table.c.emal_start.label("emal_start"),
                        domain_table.c.phone.label("phone"),
                        domain_table.c.region.label("region"),
                        domain_table.c.street.label("street"),
                    )
                    .select_from(
                        article_table.join(
                            domain_table,
                            article_table.c.domain_id == domain_table.c.id,
                        ).join(
                            category_table,
                            article_table.c.category_id == category_table.c.id,
                        )
                    )
                    .where(
                        domain_table.c.domain == self.host,
                        article_table.c.active == True,
                        sa.func.lower(article_table.c.name).like(
                            f"%{word_search.lower()}%"
                        ),
                    )
                    .order_by(sa.desc(article_table.c.created))
                )
                rs = con.execute(query).fetchall()
                if not rs:
                    query = sa.select(
                        domain_table.c.id,
                        domain_table.c.domain,
                        domain_table.c.logo,
                        domain_table.c.favicon,
                        domain_table.c.template,
                        domain_table.c.name_site,
                        domain_table.c.info_footer,
                        domain_table.c.year_start,
                        domain_table.c.emal_start,
                        domain_table.c.phone,
                        domain_table.c.region,
                        domain_table.c.street,
                    ).where(domain_table.c.domain == self.host)
                    rs = con.execute(query).fetchone()
                    data = {
                        "valid": True,
                        "result": False,
                        "word_search": word_search,
                        "domain_id": rs.id,
                        "qunt_article": 0,
                        "logo": rs.logo,
                        "favicon": rs.favicon,
                        "domain_domain": rs.domain,
                        "template": rs.template,
                        "name_site": rs.name_site,
                        "info_footer": rs.info_footer,
                        "year_start": rs.year_start,
                        "emal_start": rs.emal_start,
                        "now_year": datetime.datetime.now().year,
                        "region": rs.region,
                        "street": rs.street,
                    }
                else:
                    first_rs = rs[0]
                    data = {
                        "valid": True,
                        "result": True,
                        "word_search": word_search,
                        "qunt_article": len(rs),
                        "domain_id": first_rs.domain_id,
                        "domain_domain": first_rs.domain_domain,
                        "logo": first_rs.logo,
                        "favicon": first_rs.favicon,
                        "google_analytics": first_rs.google_analytics,
                        "yandex_metrika": first_rs.yandex_metrika,
                        "yandex_webmaster": first_rs.yandex_webmaster,
                        "template": first_rs.template,
                        "name_site": first_rs.name_site,
                        "info_footer": first_rs.info_footer,
                        "year_start": first_rs.year_start,
                        "emal_start": first_rs.emal_start,
                        "now_year": datetime.datetime.now().year,
                        "region": first_rs.region,
                        "street": first_rs.street,
                        "list_articles": [
                            {
                                "name": row.name,
                                "slug": row.slug,
                                "category_slug": row.category_slug,
                                "img_preview": row.img_preview,
                                "created": row.created.strftime("%d.%m.%Y"),
                                "text_preview": row.text_preview,
                                "time_read": row.time_read,
                                "page_view": row.page_view,
                                "category_name": row.category_name,
                            }
                            for row in rs
                        ],
                    }
            self._manage_get_otherpage_services_category(data["domain_id"]),
            if (
                self.dict_other_page["valid"]
                and self.list_services["valid"]
                and self.dict_category["valid"]
            ):
                data.update(
                    {
                        "valid": True,
                        "list_services": self.list_services["list_services"],
                        "list_other_page": self.dict_other_page["list_other_page"],
                        "list_category": self.dict_category["list_category"],
                    }
                )
            else:
                data = {"valid": False}
        except Exception as err:
            data = {"valid": False}
        finally:
            return data

    def get_default_search(self) -> dict:
        """Дефолтное отображение поиска при 1-ом get-запросе"""
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                domain_table = meta.tables["pbn_domains"]
                query = sa.select(
                    domain_table.c.id.label("domain_id"),
                    domain_table.c.logo.label("logo"),
                    domain_table.c.favicon.label("favicon"),
                    domain_table.c.domain.label("domain_domain"),
                    domain_table.c.google_analytics.label("google_analytics"),
                    domain_table.c.yandex_metrika.label("yandex_metrika"),
                    domain_table.c.yandex_webmaster.label("yandex_webmaster"),
                    domain_table.c.google_webmaster.label("google_webmaster"),
                    domain_table.c.template.label("template"),
                    domain_table.c.name_site.label("name_site"),
                    domain_table.c.info_footer.label("info_footer"),
                    domain_table.c.year_start.label("year_start"),
                    domain_table.c.emal_start.label("emal_start"),
                    domain_table.c.phone.label("phone"),
                    domain_table.c.region.label("region"),
                    domain_table.c.street.label("street"),
                ).where(
                    domain_table.c.domain == self.host,
                )
                first_rs = con.execute(query).fetchone()
                data = {
                    "valid": True,
                    "result": False,
                    "qunt_article": 0,
                    "domain_id": first_rs.domain_id,
                    "domain_domain": first_rs.domain_domain,
                    "logo": first_rs.logo,
                    "favicon": first_rs.favicon,
                    "google_analytics": first_rs.google_analytics,
                    "yandex_metrika": first_rs.yandex_metrika,
                    "yandex_webmaster": first_rs.yandex_webmaster,
                    "google_webmaster": first_rs.google_webmaster,
                    "template": first_rs.template,
                    "name_site": first_rs.name_site,
                    "info_footer": first_rs.info_footer,
                    "year_start": first_rs.year_start,
                    "emal_start": first_rs.emal_start,
                    "phone": first_rs.phone,
                    "phone_link": "+"
                    + "".join(list(filter(lambda x: x.isdigit(), first_rs.phone))),
                    "now_year": datetime.datetime.now().year,
                    "region": first_rs.region,
                    "street": first_rs.street,
                }
            self._manage_get_otherpage_services_category(data["domain_id"]),
            if (
                self.dict_other_page["valid"]
                and self.list_services["valid"]
                and self.dict_category["valid"]
            ):
                data.update(
                    {
                        "valid": True,
                        "list_services": self.list_services["list_services"],
                        "list_other_page": self.dict_other_page["list_other_page"],
                        "list_category": self.dict_category["list_category"],
                    }
                )
            else:
                data = {"valid": False}
        except Exception as err:
            data = {"valid": False}
        finally:
            return data

    def get_sitemap(self) -> dict:
        """Получаем список статей хоста для формирования XML"""
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                domain_table = meta.tables["pbn_domains"]
                article_table = meta.tables["pbn_article"]
                category_table = meta.tables["pbn_category"]
                query = (
                    sa.select(
                        article_table.c.slug,
                        article_table.c.last_mod,
                        category_table.c.category_slug.label("category_slug"),
                        domain_table.c.id.label("domain_id"),
                        domain_table.c.last_mod.label("domain_last_mod"),
                    )
                    .select_from(
                        article_table.join(
                            category_table,
                            article_table.c.category_id == category_table.c.id,
                        ).join(
                            domain_table,
                            article_table.c.domain_id == domain_table.c.id,
                        )
                    )
                    .where(
                        domain_table.c.domain == self.host,
                        article_table.c.active == True,
                    )
                    .order_by(sa.desc(article_table.c.id))
                )
                rs = con.execute(query).fetchall()
                if not rs:
                    data = {"valid": False}
                    return data
                first_rs = rs[0]
                data = {
                    "domain_id": first_rs.domain_id,
                    "domain_last_mod": first_rs.domain_last_mod,
                    "list_articles": [
                        {
                            "slug": row.slug,
                            "category_slug": row.category_slug,
                            "last_mod": row.last_mod,
                        }
                        for row in rs
                    ],
                }
                author_table = meta.tables["pbn_author"]
                query = (
                    sa.select(
                        author_table.c.slug,
                        author_table.c.last_mod,
                    )
                    .select_from(
                        author_table.join(
                            domain_table,
                            author_table.c.domain_id == domain_table.c.id,
                        )
                    )
                    .where(
                        domain_table.c.domain == self.host,
                    )
                    .order_by(sa.desc(author_table.c.id))
                )
                rs = con.execute(query).fetchall()
                if rs:
                    data["authors"] = True
                    data["list_authors"] = [
                        {"slug": row.slug, "last_mod": row.last_mod} for row in rs
                    ]
                else:
                    data["authors"] = False
            self._manage_get_otherpage_services_category(data["domain_id"]),
            if (
                self.dict_other_page["valid"]
                and self.list_services["valid"]
                and self.dict_category["valid"]
            ):
                data.update(
                    {
                        "valid": True,
                        "list_services": self.list_services["list_services"],
                        "list_other_page": self.dict_other_page["list_other_page"],
                        "list_category": self.dict_category["list_category"],
                    }
                )
            else:
                data = {"valid": False}
        except Exception as err:
            data = {"valid": False}
        finally:
            return data

    def get_services(self) -> dict:
        """Список всех услуг"""
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                domain_table = meta.tables["pbn_domains"]
                query = sa.select(
                    domain_table.c.id.label("domain_id"),
                    domain_table.c.domain.label("domain_domain"),
                    domain_table.c.logo.label("logo"),
                    domain_table.c.favicon.label("favicon"),
                    domain_table.c.google_analytics.label("google_analytics"),
                    domain_table.c.yandex_metrika.label("yandex_metrika"),
                    domain_table.c.yandex_webmaster.label("yandex_webmaster"),
                    domain_table.c.google_webmaster.label("google_webmaster"),
                    domain_table.c.template.label("template"),
                    domain_table.c.name_site.label("name_site"),
                    domain_table.c.info_footer.label("info_footer"),
                    domain_table.c.year_start.label("year_start"),
                    domain_table.c.emal_start.label("emal_start"),
                    domain_table.c.phone.label("phone"),
                    domain_table.c.region.label("region"),
                    domain_table.c.street.label("street"),
                    domain_table.c.work_time.label("work_time"),
                    domain_table.c.telegram.label("telegram"),
                    domain_table.c.service_title.label("service_title"),
                    domain_table.c.service_description.label("service_description"),
                    domain_table.c.service_text.label("service_text"),
                    domain_table.c.name_info.label("name_info"),
                ).where(
                    domain_table.c.domain == self.host,
                )
                rs = con.execute(query).fetchall()
                if not rs:
                    data = {"valid": False}
                    return data
                first_rs = rs[0]
                data = {
                    "domain_id": first_rs.domain_id,
                    "domain_domain": first_rs.domain_domain,
                    "logo": first_rs.logo,
                    "favicon": first_rs.favicon,
                    "google_analytics": first_rs.google_analytics,
                    "yandex_metrika": first_rs.yandex_metrika,
                    "yandex_webmaster": first_rs.yandex_webmaster,
                    "google_webmaster": first_rs.google_webmaster,
                    "template": first_rs.template,
                    "name_site": first_rs.name_site,
                    "info_footer": first_rs.info_footer,
                    "year_start": first_rs.year_start,
                    "emal_start": first_rs.emal_start,
                    "now_year": datetime.datetime.now().year,
                    "phone": first_rs.phone,
                    "phone_link": "+"
                    + "".join(list(filter(lambda x: x.isdigit(), first_rs.phone))),
                    "region": first_rs.region,
                    "street": first_rs.street,
                    "work_time": first_rs.work_time,
                    "telegram": first_rs.telegram,
                    "title": first_rs.service_title,
                    "description": first_rs.service_description,
                    "service_text": first_rs.service_text,
                    "name_info": first_rs.name_info,
                }
            self._manage_get_otherpage_services_category(data["domain_id"]),
            if (
                self.dict_other_page["valid"]
                and self.list_services["valid"]
                and self.dict_category["valid"]
            ):
                data.update(
                    {
                        "valid": True,
                        "list_services": self.list_services["list_services"],
                        "list_other_page": self.dict_other_page["list_other_page"],
                        "list_category": self.dict_category["list_category"],
                    }
                )
            else:
                data = {"valid": False}
        except Exception as err:
            data = {"valid": False}
        finally:
            return data

    def get_one_servise(self, slug: str) -> dict:
        """Конкретная страница услуги"""
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                domain_table = meta.tables["pbn_domains"]
                service_table = meta.tables["pbn_service"]
                query = (
                    sa.select(
                        domain_table.c.logo.label("logo"),
                        domain_table.c.favicon.label("favicon"),
                        domain_table.c.id.label("domain_id"),
                        domain_table.c.domain.label("domain"),
                        domain_table.c.google_analytics.label("google_analytics"),
                        domain_table.c.yandex_metrika.label("yandex_metrika"),
                        domain_table.c.yandex_webmaster.label("yandex_webmaster"),
                        domain_table.c.google_webmaster.label("google_webmaster"),
                        domain_table.c.template.label("template"),
                        domain_table.c.name_site.label("name_site"),
                        domain_table.c.info_footer.label("info_footer"),
                        domain_table.c.year_start.label("year_start"),
                        domain_table.c.emal_start.label("emal_start"),
                        domain_table.c.phone.label("phone"),
                        domain_table.c.region.label("region"),
                        domain_table.c.street.label("street"),
                        domain_table.c.work_time.label("work_time"),
                        domain_table.c.telegram.label("telegram"),
                        domain_table.c.name_info.label("name_info"),
                        service_table.c.id,
                        service_table.c.name,
                        service_table.c.slug,
                        service_table.c.title,
                        service_table.c.description,
                        service_table.c.keywords,
                        service_table.c.name_table_price,
                        service_table.c.value_table_price,
                    )
                    .select_from(
                        service_table.join(
                            domain_table,
                            service_table.c.domain_id == domain_table.c.id,
                        )
                    )
                    .where(
                        service_table.c.slug == slug,
                        service_table.c.domain_id == domain_table.c.id,
                    )
                )
                rs = con.execute(query).fetchall()
                if not rs:
                    data = {"valid": False}
                    return data
                first_rs = rs[0]
                data = {
                    "domain_id": first_rs.domain_id,
                    "logo": first_rs.logo,
                    "favicon": first_rs.favicon,
                    "domain": first_rs.domain,
                    "google_analytics": first_rs.google_analytics,
                    "yandex_metrika": first_rs.yandex_metrika,
                    "yandex_webmaster": first_rs.yandex_webmaster,
                    "google_webmaster": first_rs.google_webmaster,
                    "template": first_rs.template,
                    "name_site": first_rs.name_site,
                    "info_footer": first_rs.info_footer,
                    "year_start": first_rs.year_start,
                    "emal_start": first_rs.emal_start,
                    "now_year": datetime.datetime.now().year,
                    "phone": first_rs.phone,
                    "phone_link": "+"
                    + "".join(list(filter(lambda x: x.isdigit(), first_rs.phone))),
                    "region": first_rs.region,
                    "street": first_rs.street,
                    "work_time": first_rs.work_time,
                    "telegram": first_rs.telegram,
                    "name_info": first_rs.name_info,
                    "service_id": first_rs.id,
                    "service_name": first_rs.name,
                    "title": first_rs.title,
                    "description": first_rs.description,
                    "keywords": first_rs.keywords,
                    "service_slug": first_rs.slug,
                    "name_table_price": first_rs.name_table_price,
                    "value_table_price": first_rs.value_table_price,
                }
            self._manage_get_price_text_service(data["service_id"])
            if self.list_text_block["valid"] and self.list_prices["valid"]:
                data.update(
                    {
                        "valid": True,
                        "list_text_block": self.list_text_block["list_text_block"],
                        "list_prices": self.list_prices["list_prices"],
                        "count_price": self.list_prices["count_price"],
                        "max_price": self.list_prices["max_price"],
                        "min_price": self.list_prices["min_price"],
                    }
                )
                self._manage_get_otherpage_services_category(data["domain_id"]),
                if (
                    self.dict_other_page["valid"]
                    and self.list_services["valid"]
                    and self.dict_category["valid"]
                ):
                    data.update(
                        {
                            "valid": True,
                            "list_services": self.list_services["list_services"],
                            "list_other_page": self.dict_other_page["list_other_page"],
                            "list_category": self.dict_category["list_category"],
                        }
                    )
                else:
                    data = {"valid": False}
            else:
                data = {"valid": False}
        except Exception as err:
            data = {"valid": False}
        finally:
            return data

    def _get_main_sliders(self, domain_id):
        engine = sa.create_engine(self.connect_db)
        with engine.connect() as con:
            meta = sa.MetaData()
            meta.reflect(engine)
            slider_table = meta.tables["pbn_mainslider"]
            query = (
                sa.select(
                    slider_table.c.name,
                    slider_table.c.sort,
                    slider_table.c.text,
                    slider_table.c.preview_picture,
                    slider_table.c.link,
                )
                .select_from(slider_table)
                .where(
                    slider_table.c.domain_id == domain_id,
                )
                .order_by(sa.asc(slider_table.c.sort))
            )
            rs = con.execute(query).fetchall()
            list_sliders = [
                {
                    "name": row.name,
                    "text": row.text,
                    "preview_picture": row.preview_picture,
                    "link": row.link,
                }
                for row in rs
            ]
            return list_sliders

    def _get_price_service(self, service_id):
        engine = sa.create_engine(self.connect_db)
        with engine.connect() as con:
            meta = sa.MetaData()
            meta.reflect(engine)
            price_table = meta.tables["pbn_price"]
            price_constructortextservice = meta.tables["pbn_constructortextservice"]
            query = (
                sa.select(
                    price_table.c.name_price.label("name"),
                    price_table.c.price.label("price_name"),
                    price_table.c.price_service_id.label("service_id"),
                    price_constructortextservice.c.type_block,
                    price_constructortextservice.c.sort,
                    price_constructortextservice.c.place_price,
                    price_constructortextservice.c.picture,
                    price_constructortextservice.c.subtitle,
                    price_constructortextservice.c.text,
                    price_constructortextservice.c.service_id,
                )
                .select_from(
                    price_table.join(
                        price_constructortextservice,
                        price_table.c.service_id
                        == price_constructortextservice.c.service_id,
                    )
                )
                .where(
                    price_table.c.service_id == service_id,
                )
            )
            rs = con.execute(query).fetchall()
            list_prices = [
                {
                    "name": row.name,
                    "price_name": row.price_name,
                }
                for row in rs
            ]
            return list_prices

    def _manage_get_otherpage_services_category(self, domain_id: int) -> dict:
        """Получение списка категорий, списка услуг и списка других страниц в 3 потокока - дочерная функция"""
        thr1 = threading.Thread(
            target=self._get_all_service,
            args=[
                domain_id,
            ],
        )
        thr2 = threading.Thread(
            target=self._get_all_other_page_host,
            args=[
                domain_id,
            ],
        )
        thr3 = threading.Thread(
            target=self._get_all_category_host,
            args=[
                domain_id,
            ],
        )
        thr1.start()
        thr2.start()
        thr3.start()
        thr1.join()
        thr2.join()
        thr3.join()

    def _get_all_category_host(self, domain_id: int) -> dict:
        """Получение всех категорий хоста"""
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                list_table = meta.tables["pbn_category"]
                list_query = (
                    sa.select(
                        list_table.c.name,
                        list_table.c.category_slug,
                        list_table.c.last_mod,
                        list_table.c.img_preview,
                    )
                    .where(list_table.c.domain_id == domain_id)
                    .order_by(sa.asc(list_table.c.sort))
                )
                rs = con.execute(list_query)
                list_pages = [
                    {
                        "name": row.name,
                        "slug": row.category_slug,
                        "last_mod": row.last_mod,
                        "img_preview": row.img_preview,
                    }
                    for row in rs
                ]
            self.dict_category = {"valid": True, "list_category": list_pages}
        except:
            self.dict_category = {"valid": False}

    def _get_all_other_page_host(self, domain_id: int) -> dict:
        """Получение всех других категорий хоста"""
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                list_table = meta.tables["pbn_otherpage"]
                list_query = (
                    sa.select(
                        list_table.c.name,
                        list_table.c.slug,
                        list_table.c.last_mod,
                    )
                    .where(list_table.c.domain_id == domain_id)
                    .order_by(sa.asc(list_table.c.sort))
                )
                rs = con.execute(list_query)
                list_pages = [
                    {
                        "name": row.name,
                        "slug": row.slug,
                        "last_mod": row.last_mod,
                    }
                    for row in rs
                ]
            self.dict_other_page = {"valid": True, "list_other_page": list_pages}
        except:
            self.dict_other_page = {"valid": False}

    def _get_all_service(self, domain_id):
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                service_table = meta.tables["pbn_service"]
                query = (
                    sa.select(
                        service_table.c.name,
                        service_table.c.sort,
                        service_table.c.preview_picture,
                        service_table.c.slug,
                    )
                    .select_from(service_table)
                    .where(
                        service_table.c.domain_id == domain_id,
                    )
                    .order_by(sa.asc(service_table.c.sort))
                )
                rs = con.execute(query).fetchall()
                list_services = [
                    {
                        "name": row.name,
                        "preview_picture": row.preview_picture,
                        "slug": row.slug,
                    }
                    for row in rs
                ]
            self.list_services = {"valid": True, "list_services": list_services}
        except:
            self.list_services = {"valid": False}

    def _manage_get_price_text_service(self, service_id: int) -> dict:
        """Управляющая функция для 2-ух потоков: получение текстовых блоков и таблицы цен"""
        thr1 = threading.Thread(
            target=self._get_prices,
            args=[
                service_id,
            ],
        )
        thr2 = threading.Thread(
            target=self._get_text_block,
            args=[
                service_id,
            ],
        )
        thr1.start()
        thr2.start()
        thr1.join()
        thr2.join()

    def _get_prices(self, service_id: int) -> dict:
        """Получение всех цен для конкретной услуги"""
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                price_table = meta.tables["pbn_price"]
                query = (
                    sa.select(
                        price_table.c.price_name,
                        price_table.c.name,
                        price_table.c.service_id,
                    )
                    .select_from(price_table)
                    .where(
                        price_table.c.service_id == service_id,
                    )
                )
                rs = con.execute(query).fetchall()
                list_prices = [
                    {
                        "name": row.name,
                        "price_name": row.price_name,
                    }
                    for row in rs
                ]
            list_max_min_price = [el["price_name"] for el in list_prices]
            self.list_prices = {
                "valid": True,
                "list_prices": list_prices,
                "count_price": len(list_prices),
                "max_price": max(list_max_min_price),
                "min_price": min(list_max_min_price),
            }
        except:
            self.list_prices = {"valid": False}

    def _get_text_block(self, service_id):
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                price_constructortextservice = meta.tables["pbn_constructortextservice"]
                query = (
                    sa.select(
                        price_constructortextservice.c.type_block,
                        price_constructortextservice.c.sort,
                        price_constructortextservice.c.place_price,
                        price_constructortextservice.c.picture,
                        price_constructortextservice.c.subtitle,
                        price_constructortextservice.c.text,
                        price_constructortextservice.c.service_id,
                    )
                    .select_from(price_constructortextservice)
                    .where(
                        price_constructortextservice.c.service_id == service_id,
                    )
                    .order_by(sa.asc(price_constructortextservice.c.sort))
                )
                rs = con.execute(query).fetchall()
                list_text_block = [
                    {
                        "type_block": row.type_block,
                        "place_price": row.place_price,
                        "picture": row.picture,
                        "subtitle": row.subtitle,
                        "text": row.text,
                    }
                    for row in rs
                ]
            self.list_text_block = {"valid": True, "list_text_block": list_text_block}
        except:
            self.list_text_block = {"valid": False}
