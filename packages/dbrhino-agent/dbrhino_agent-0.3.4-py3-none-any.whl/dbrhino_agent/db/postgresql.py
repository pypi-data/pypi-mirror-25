import re
import logging
import psycopg2
from psycopg2.extras import quote_ident
from . import common
from .. import templates as tmpl
from ..dbrhino import GrantResult

logger = logging.getLogger(__name__)


def full_version_string(cur):
    cur.execute("select version()")
    return common.scalar_result(cur)


def get_pg_version(cur):
    match = re.search(r"PostgreSQL\s+([0-9.]+)", full_version_string(cur))
    return match.group(1) if match else None


def get_redshift_version(cur):
    match = re.search(r"Redshift\s+([0-9.]+)", full_version_string(cur))
    return match.group(1) if match else None


def is_redshift(cur):
    return "redshift" in full_version_string(cur).lower()


def current_database(cur):
    cur.execute("SELECT current_database()")
    return common.scalar_result(cur)


def discover_all_schemas(cur):
    cur.execute("""
        SELECT schema_name
        FROM information_schema.schemata
        WHERE schema_name NOT LIKE 'pg_%'
        AND schema_name != 'information_schema'
    """)
    return common.first_column(cur)


class Catalog(object):
    def __init__(self, *, database, schemas):
        self.database = database
        self.schemas = schemas

    @classmethod
    def discover(cls, cur):
        return cls(
            database=current_database(cur),
            schemas=discover_all_schemas(cur),
        )


def find_username(cur, username):
    cur.execute(
        "SELECT usename FROM pg_catalog.pg_user WHERE usename = %s",
        (username,)
    )
    return common.scalar_result(cur)


def create_user(cur, username, pw):
    if is_redshift(cur):
        cur.execute("CREATE USER {} PASSWORD %s"
                    .format(quote_ident(username, cur)),
                    (pw,))
    else:
        cur.execute("CREATE USER {} WITH ENCRYPTED PASSWORD %s"
                    .format(quote_ident(username, cur)),
                    (pw,))


def drop_user(cur, username):
    cur.execute("DROP USER {}".format(quote_ident(username, cur)))


def update_pw(cur, username, pw):
    if is_redshift(cur):
        cur.execute("ALTER USER {} PASSWORD %s"
                    .format(quote_ident(username, cur)),
                    (pw,))
    else:
        cur.execute("ALTER USER {} WITH ENCRYPTED PASSWORD %s"
                    .format(quote_ident(username, cur)),
                    (pw,))


def apply_pw(cur, username, pw):
    if find_username(cur, username):
        update_pw(cur, username, pw)
    else:
        create_user(cur, username, pw)


def revoke_everything(cur, catalog, username):
    cur.execute("REVOKE ALL ON DATABASE {} FROM {}"
                .format(quote_ident(catalog.database, cur),
                        quote_ident(username, cur)))
    schema_sqls = [
        "REVOKE ALL ON SCHEMA {} FROM {}",
        "REVOKE ALL ON ALL TABLES IN SCHEMA {} FROM {}",
        "REVOKE ALL ON ALL SEQUENCES IN SCHEMA {} FROM {}",
        "REVOKE ALL ON ALL FUNCTIONS IN SCHEMA {} FROM {}",
    ]
    for schema in catalog.schemas:
        for sql in schema_sqls:
            cur.execute(sql.format(quote_ident(schema, cur),
                                   quote_ident(username, cur)))


def apply_statements(cur, catalog, username, statements):
    for stmt in statements:
        sqls = tmpl.render_and_split(
            stmt,
            all_schemas=catalog.schemas,
            database=quote_ident(catalog.database, cur),
            username=quote_ident(username, cur),
        )
        for sql in sqls:
            cur.execute(sql)


def connect(dbconf):
    dbconf = dbconf.copy()
    if "port" not in dbconf:
        if dbconf["type"] == "redshift":
            dbconf["port"] = 5439
        else:
            dbconf["port"] = 5432
    dsn = ("postgresql://{user}:{password}@{host}:{port}/{database}"
           .format(**dbconf))
    return psycopg2.connect(dsn)


class controlled_cursor(object):
    def __init__(self, dbconf):
        self.dbconf = dbconf
        self._conn = None
        self._cursor = None

    def __enter__(self):
        self._conn = connect(self.dbconf)
        self._cursor = self._conn.cursor()
        return self._cursor

    def __exit__(self, exception_type, exception_value, traceback):
        if not exception_type:
            self._conn.commit()
        self._cursor.close()
        self._conn.close()


class Postgresql(common.Database):
    def implement_grant(self, grant):
        logger.debug("implementing grant for %s in %s",
                     grant.username, self.name)
        with controlled_cursor(self.dbconf) as cur:
            if grant.password:
                apply_pw(cur, grant.username, grant.password)
            elif not find_username(cur, grant.username):
                return GrantResult.NO_PASSWORD
            catalog = Catalog.discover(cur)
            revoke_everything(cur, catalog, grant.username)
            apply_statements(cur, catalog, grant.username,
                             grant.statements)
            return GrantResult.APPLIED

    def drop_user(self, username):
        with controlled_cursor(self.dbconf) as cur:
            if not find_username(cur, username):
                return GrantResult.NO_CHANGE
            logger.debug("dropping user %s from %s", username, self.name)
            catalog = Catalog.discover(cur)
            revoke_everything(cur, catalog, username)
            cur.connection.commit()
            drop_user(cur, username)
            return GrantResult.REVOKED

    def discover_dbversion(self):
        with controlled_cursor(self.dbconf) as cur:
            if is_redshift(cur):
                return get_redshift_version(cur)
            return get_pg_version(cur)
