import sqlalchemy as sa, threading, datetime


class ConnectDB:
    def __init__(self, host):
        self.host = host
        self.dict_category = []
        self.dict_other_page = []
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
                        }
                        for row in rs
                    ],
                    "list_top_arcicle": [],
                }
            self._manage_get_category_articles(data["domain_id"])
            if self.dict_category["valid"] and self.dict_other_page["valid"]:
                data.update(
                    {
                        "valid": True,
                        "list_category": self.dict_category["list_category"],
                        "list_other_page": self.dict_other_page["list_other_page"],
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
                }
            self._manage_get_category_articles(data["domain_id"])
            if self.dict_category["valid"] and self.dict_other_page["valid"]:
                data.update(
                    {
                        "valid": True,
                        "list_category": self.dict_category["list_category"],
                        "list_other_page": self.dict_other_page["list_other_page"],
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
                        }
                        for row in rs
                    ],
                }
            self._manage_get_category_articles(data["domain_id"])
            if self.dict_category["valid"] and self.dict_other_page["valid"]:
                data.update(
                    {
                        "valid": True,
                        "list_category": self.dict_category["list_category"],
                        "list_other_page": self.dict_other_page["list_other_page"],
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
            self._manage_get_category_articles(data["domain_id"])
            if self.dict_category["valid"] and self.dict_other_page["valid"]:
                data.update(
                    {
                        "valid": True,
                        "list_category": self.dict_category["list_category"],
                        "list_other_page": self.dict_other_page["list_other_page"],
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
                }
                self._manage_get_category_articles(data["domain_id"])
                if self.dict_category["valid"] and self.dict_other_page["valid"]:
                    data.update(
                        {
                            "valid": True,
                            "list_category": self.dict_category["list_category"],
                            "list_other_page": self.dict_other_page["list_other_page"],
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

    def _manage_get_category_articles(self, domain_id: int) -> dict:
        """Получение списка категорий и списка других страниц в 2 потокока - дочерная функция"""
        thr1 = threading.Thread(
            target=self._get_all_category_host,
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
        thr1.start()
        thr2.start()
        thr1.join()
        thr2.join()

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
                        "year_start": first_rs.year_start,
                        "emal_start": first_rs.emal_start,
                        "now_year": datetime.datetime.now().year,
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
                            }
                            for row in rs
                        ],
                    }
            self._manage_get_category_articles(data["domain_id"])
            if self.dict_category["valid"] and self.dict_other_page["valid"]:
                data.update(
                    {
                        "list_category": self.dict_category["list_category"],
                        "list_other_page": self.dict_other_page["list_other_page"],
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
                }
            self._manage_get_category_articles(data["domain_id"])
            if self.dict_category["valid"] and self.dict_other_page["valid"]:
                data.update(
                    {
                        "list_category": self.dict_category["list_category"],
                        "list_other_page": self.dict_other_page["list_other_page"],
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
            self._manage_get_category_articles(data["domain_id"])
            if self.dict_category["valid"] and self.dict_other_page["valid"]:
                data.update(
                    {
                        "valid": True,
                        "list_category": self.dict_category["list_category"],
                        "list_other_page": self.dict_other_page["list_other_page"],
                    }
                )
            else:
                data = {"valid": False}
        except Exception as err:
            data = {"valid": False}
        finally:
            return data
