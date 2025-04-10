import sqlalchemy as sa

def get_list_redirects():
    connect_db = "mysql+pymysql://max_shark:fdfde0fdf$@176.99.9.17:3306/pbn_crm"
    try:
        engine = sa.create_engine(connect_db)
        with engine.connect() as con:
            meta = sa.MetaData()
            meta.reflect(engine)
            links_table = meta.tables["pbn_linksredirects"]
            domain_table = meta.tables["pbn_domains"]
            query = (
                sa.select(
                    links_table.c.start_link,
                    links_table.c.finish_link,
                    domain_table.c.domain.label("host"),
                )
                .select_from(
                    links_table.join(
                        domain_table,
                        links_table.c.domain_id == domain_table.c.id,
                    )
                )
                .order_by(sa.desc(links_table.c.id))
            )
            rs = con.execute(query).fetchall()
            dict_redirects = {}
            for row in rs:
                if dict_redirects.get(row.host):
                    dict_redirects[row.host][row.start_link] = row.finish_link
                else:
                    dict_redirects[row.host] = {}
                    dict_redirects[row.host][row.start_link] = row.finish_link
            return dict_redirects
    except Exception as err:
        return False

redirects_map = get_list_redirects()