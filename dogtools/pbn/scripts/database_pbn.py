import sqlalchemy as sa, threading, datetime


class ConnectDB:
    def __init__(self, host):
        self.host = host
        self.dict_category = []
        self.dict_other_page = []
        self.connect_db = (
            "mysql+pymysql://max_shark:fdfde0fdf$@176.99.9.17:3306/pbn_crm"
        )

    def get_all_arcticle_for_blog(self) -> dict:
        """Список всех статей хоста для вывода в блог"""
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
                        domain_table.c.logo.label("logo"),
                        domain_table.c.favicon.label("favicon"),
                        domain_table.c.domain.label("domain_domain"),
                        domain_table.c.blog_title.label("blog_title"),
                        domain_table.c.blog_description.label("blog_description"),
                        domain_table.c.blog_name.label("blog_name"),
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
                    "domain_domain": first_rs.domain_domain,
                    "title": first_rs.blog_title,
                    "description": first_rs.blog_description,
                    "h1": first_rs.blog_name,
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
            print(err)
            data = {"valid": False}
        finally:
            return data

    def get_article_category(self, slug: str) -> dict:
        """Список активных статей рубрики в рамках хоста"""
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                article_table = meta.tables["pbn_article"]
                category_table = meta.tables["pbn_category"]
                domain_table = meta.tables["pbn_domains"]
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
                        category_table.c.title.label("title"),
                        category_table.c.description.label("description"),
                        category_table.c.h1.label("h1"),
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
                        category_table.c.category_slug == slug,
                        domain_table.c.domain == self.host,
                        article_table.c.active == True,
                    )
                    .order_by(sa.desc(article_table.c.created))
                )
                rs = con.execute(query).fetchall()
                if not rs:
                    data = {"valid": False}
                    return data
                first_rs = rs[0]
                data = {
                    "qunt_article": len(rs),
                    "domain_id": first_rs.domain_id,
                    "domain_domain": first_rs.domain_domain,
                    "category_slug": first_rs.category_slug,
                    "title": first_rs.title,
                    "description": first_rs.description,
                    "h1": first_rs.h1,
                    "category_name": first_rs.category_name,
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
                    "list_articles": [
                        {
                            "name": row.name,
                            "slug": row.slug,
                            "category_slug": row.category_slug,
                            "img_preview": row.img_preview,
                            "created": row.created,
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

    def add_count_view_article(self, id_article: int, now_page_view: int) -> bool:
        """Добавляем к текущей статье +1 просмотр на каждый get-запрос.
        Получаем id-статьи и текущее количество просмоторов. Обратно просто TRUE/False.
        """
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.begin() as conn:
                meta = sa.MetaData()
                meta.reflect(engine)
                article_table = meta.tables["pbn_article"]
                update = (
                    sa.update(article_table)
                    .where(article_table.c.id == id_article)
                    .values(page_view=now_page_view + 1)
                )
                conn.execute(update)
            return True
        except Exception:
            return False

    def get_article(self, article_slug="", category_slug="") -> dict:
        """Получение информации о конкретной статьи на хосте по слагу статьи и слагу категорий"""
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
                        article_table.c.description,
                        article_table.c.text,
                        article_table.c.created,
                        article_table.c.time_read,
                        article_table.c.page_view,
                        article_table.c.table_content,
                        article_table.c.author_id,
                        category_table.c.id.label("category_id"),
                        category_table.c.name.label("category_name"),
                        category_table.c.category_slug.label("category_slug"),
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
                        article_table.c.slug == article_slug,
                        category_table.c.category_slug == category_slug,
                        domain_table.c.domain == self.host,
                        article_table.c.active == True,
                    )
                    .order_by(sa.desc(article_table.c.created))
                )
                rs = con.execute(query).fetchone()
                if not rs:
                    data = {"valid": False}
                    return data
                data = {
                    "id_article": rs.id,
                    "created": rs.created,
                    "slug": rs.slug,
                    "name": rs.name,
                    "title": rs.title,
                    "description": rs.description,
                    "text": rs.text,
                    "time_read": rs.time_read,
                    "page_view": rs.page_view,
                    "table_content": rs.table_content,
                    "category_name": rs.category_name,
                    "category_slug": rs.category_slug,
                    "domain_id": rs.domain_id,
                    "domain_domain": rs.domain_domain,
                    "logo": rs.logo,
                    "favicon": rs.favicon,
                    "id_category": rs.category_id,
                    "google_analytics": rs.google_analytics,
                    "yandex_metrika": rs.yandex_metrika,
                    "yandex_webmaster": rs.yandex_webmaster,
                    "google_webmaster": rs.google_webmaster,
                    "template": rs.template,
                    "name_site": rs.name_site,
                    "info_footer": rs.info_footer,
                    "author_id": rs.author_id,
                    "year_start": rs.year_start,
                    "emal_start": rs.emal_start,
                    "now_year": datetime.datetime.now().year,
                    "phone": rs.phone,
                    "phone_link": "+"
                    + "".join(list(filter(lambda x: x.isdigit(), rs.phone))),
                }
                article_query = (
                    sa.select(article_table)
                    .where(
                        sa.and_(
                            article_table.c.category_id == data["id_category"],
                            article_table.c.id < data["id_article"],
                            article_table.c.active == True,
                        )
                    )
                    .order_by(sa.desc(article_table.c.created))
                )
                rs = con.execute(article_query)
                if rs.rowcount < 1:
                    article_query = (
                        sa.select(article_table)
                        .where(
                            sa.and_(
                                article_table.c.category_id == data["id_category"],
                                article_table.c.id > data["id_article"],
                                article_table.c.active == True,
                            )
                        )
                        .order_by(sa.desc(article_table.c.created))
                    )
                    rs = con.execute(article_query)
                rs = rs.fetchmany(3)
                data["simular_articles"] = [
                    {
                        "name": row.name,
                        "slug": row.slug,
                        "category_slug": category_slug,
                        "img_preview": row.img_preview,
                        "created": row.created,
                        "description": row.description,
                    }
                    for row in rs
                ]
            if data["author_id"]:
                data["data_author"] = self._get_author_for_article(data["author_id"])
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

    def get_top_articles(self, domain_id: int, top=7) -> list:
        """Получаем топ-n статей по кол-ву просмотров у хоста и выдаем отсоритированный список"""
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                article_table = meta.tables["pbn_article"]
                category_table = meta.tables["pbn_category"]
                query = (
                    sa.select(
                        article_table.c.name,
                        article_table.c.slug,
                        article_table.c.page_view,
                        category_table.c.category_slug.label("category_slug"),
                    )
                    .select_from(
                        article_table.join(
                            category_table,
                            article_table.c.category_id == category_table.c.id,
                        )
                    )
                    .where(
                        article_table.c.domain_id == domain_id,
                        article_table.c.active == True,
                    )
                    .order_by(sa.desc(article_table.c.page_view))
                    .limit(top)
                )
                rs = con.execute(query).fetchall()
                if not rs:
                    data = {"valid": False}
                    return data
                list_top_articles = [
                    {
                        "name": row.name,
                        "slug": row.slug,
                        "category_slug": row.category_slug,
                        "page_view": row.page_view,
                    }
                    for row in rs
                ]
            return list_top_articles
        except Exception as err:
            return False

    def get_info_404(self):
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
                    domain_table.c.year_start.label("emal_start"),
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

    def _get_author_for_article(self, author_id: int) -> dict:
        """Дополнительная функция для получения информации об авторе статьи, если задана инфа об авторе"""
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                author_table = meta.tables["pbn_author"]
                query = sa.select(
                    author_table.c.name,
                    author_table.c.spec,
                    author_table.c.slug,
                    author_table.c.img_preview,
                ).where(author_table.c.id == author_id)
                rs = con.execute(query).fetchone()
                if not rs:
                    return {"valid": False}
                data = {
                    "name": rs.name,
                    "spec": rs.spec,
                    "slug": rs.slug,
                    "img_preview": rs.img_preview,
                    "valid": True,
                }
                return data
        except Exception as err:
            data = {"valid": False}
        finally:
            return data

    def _manage_get_category_articles(self, domain_id):
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

    def _get_all_category_host(self, domain_id):
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                list_table = meta.tables["pbn_category"]
                list_query = (
                    sa.select(list_table)
                    .where(list_table.c.domain_id == domain_id)
                    .order_by(sa.asc(list_table.c.sort))
                )
                rs = con.execute(list_query)
                list_pages = [
                    {
                        "name": row.name,
                        "slug": row.category_slug,
                        "img_preview": row.img_preview,
                    }
                    for row in rs
                ]
            self.dict_category = {"valid": True, "list_category": list_pages}
        except:
            self.dict_category = {"valid": False}

    def _get_all_other_page_host(self, domain_id):
        try:
            engine = sa.create_engine(self.connect_db)
            with engine.connect() as con:
                meta = sa.MetaData()
                meta.reflect(engine)
                list_table = meta.tables["pbn_otherpage"]
                list_query = (
                    sa.select(list_table)
                    .where(list_table.c.domain_id == domain_id)
                    .order_by(sa.asc(list_table.c.sort))
                )
                rs = con.execute(list_query)
                list_pages = [
                    {
                        "name": row.name,
                        "slug": row.slug,
                    }
                    for row in rs
                ]
            self.dict_other_page = {"valid": True, "list_other_page": list_pages}
        except:
            self.dict_other_page = {"valid": False}
