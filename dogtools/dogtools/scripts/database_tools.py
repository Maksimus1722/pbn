import sqlalchemy as sa, threading
import datetime


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
                    .limit(10)
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
                    .order_by(sa.desc(article_table.c.id))
                )
                rs = con.execute(query).fetchall()
                if not rs:
                    query = sa.select(
                        domain_table.c.id,
                        domain_table.c.domain,
                        domain_table.c.logo,
                        domain_table.c.favicon,
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
