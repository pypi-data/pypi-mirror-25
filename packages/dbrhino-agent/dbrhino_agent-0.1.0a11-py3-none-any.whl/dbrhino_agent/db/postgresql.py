from collections import namedtuple
import re
import logging
from functools import wraps
from .utils import Database, first_column, NoPasswordException
import psycopg2
from psycopg2.extras import quote_ident

logger = logging.getLogger(__name__)


def current_database(cur):
    cur.execute("SELECT current_database()")
    return first_column(cur)[0]


def discover_all_schemas(cur):
    cur.execute("""
        SELECT schema_name
        FROM information_schema.schemata
        WHERE schema_name NOT LIKE 'pg_%'
        AND schema_name != 'information_schema'
    """)
    return first_column(cur)


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

    def matching_schemas(self, stmt):
        return [sch for sch in self.schemas
                if stmt.matches_schema(sch)]


def find_username(cur, username):
    cur.execute(
        "SELECT usename FROM pg_catalog.pg_user WHERE usename = %s",
        (username,)
    )
    return first_column(cur)


def create_user(cur, username, pw):
    cur.execute("CREATE ROLE {} WITH LOGIN ENCRYPTED PASSWORD %s"
                .format(quote_ident(username, cur)),
                (pw,))


def drop_user(cur, username):
    cur.execute("DROP ROLE {}".format(quote_ident(username, cur)))


def update_pw(cur, username, pw):
    cur.execute("ALTER ROLE {} WITH ENCRYPTED PASSWORD %s"
                .format(quote_ident(username, cur)),
                (pw,))


def apply_pw(cur, username, pw):
    if find_username(cur, username):
        update_pw(cur, username, pw)
    else:
        create_user(cur, username, pw)


class GrantOp(object):
    def __init__(self, cur, catalog, username):
        self.cur = cur
        self.catalog = catalog
        self.username = username

    def validate(self, stmt):
        for perm in stmt.permissions:
            if perm.lower() not in self.valid_permissions:
                raise Exception("valid permissions: {} | received: {}"
                                .format(self.valid_permissions, perm))

    def render(self, **kwargs):
        return self.templ.format(**kwargs)

    def log_and_execute(self, sql, *args, **kwargs):
        logger.debug("sql: " + sql)
        self.cur.execute(sql, *args, **kwargs)


class DatabaseOp(GrantOp):
    def revoke_all(self):
        self.cur.execute("REVOKE ALL ON DATABASE {} FROM {}"
                         .format(quote_ident(self.catalog.database, self.cur),
                                 quote_ident(self.username, self.cur)))

    valid_permissions = {"create", "connect", "temporary", "temp", "all"}
    templ = "GRANT {perms} ON DATABASE {db} TO {user}"

    def apply(self, stmt):
        self.validate(stmt)
        if stmt.match is not None:
            logger.warn('"match" is ignored for database grants')
        sql = self.render(perms=",".join(stmt.permissions), user=self.username,
                          db=self.catalog.database)
        self.log_and_execute(sql)


class SchemaOp(GrantOp):
    def revoke_all(self):
        for schema in self.catalog.schemas:
            self.cur.execute("REVOKE ALL ON SCHEMA {} FROM {}"
                             .format(quote_ident(schema, self.cur),
                                     quote_ident(self.username, self.cur)))

    valid_permissions = {"create", "usage", "all"}
    templ = "GRANT {perms} ON SCHEMA {schema} TO {user}"

    def apply(self, stmt):
        self.validate(stmt)
        for schema in self.catalog.matching_schemas(stmt):
            sql = self.render(perms=",".join(stmt.permissions),
                              user=self.username, schema=schema)
            self.log_and_execute(sql)


class AllTablesInSchemaOp(GrantOp):
    def revoke_all(self):
        for schema in self.catalog.schemas:
            self.cur.execute("REVOKE ALL ON ALL TABLES IN SCHEMA {} FROM {}"
                             .format(quote_ident(schema, self.cur),
                                     quote_ident(self.username, self.cur)))

    valid_permissions = {"select", "insert", "update", "delete", "truncate",
                  "references", "trigger", "all"}
    templ = "GRANT {perms} ON ALL TABLES IN SCHEMA {schema} TO {user}"

    def apply(self, stmt):
        self.validate(stmt)
        for schema in self.catalog.matching_schemas(stmt):
            sql = self.render(perms=",".join(stmt.permissions),
                              user=self.username, schema=schema)
            self.log_and_execute(sql)

grant_operations = {
    "database": DatabaseOp,
    "schema": SchemaOp,
    "all_tables_in_schema": AllTablesInSchemaOp,
}


def revoke_everything(cur, catalog, username):
    for op_cls in grant_operations.values():
        op = op_cls(cur, catalog, username)
        op.revoke_all()


def apply_statements(cur, catalog, username, statements):
    for stmt in statements:
        grant_op_cls = grant_operations[stmt.type]
        grant_op_cls(cur, catalog, username).apply(stmt)


class controlled_cursor(object):
    def __init__(self, connect_to):
        self.connect_to = connect_to

    def __enter__(self):
        self._conn = psycopg2.connect(self.connect_to)
        self._cursor = self._conn.cursor()
        return self._cursor

    def __exit__(self, exception_type, exception_value, traceback):
        if not exception_type:
            self._conn.commit()
        self._cursor.close()
        self._conn.close()


class Postgresql(Database):
    def implement_grant(self, grant):
        logger.debug("implementing grant for {} in {}"
                     .format(grant.username, self.name))
        with controlled_cursor(self.connect_to) as cur:
            if grant.password:
                apply_pw(cur, grant.username, grant.password)
            elif not find_username(cur, grant.username):
                raise NoPasswordException(grant.username)
            catalog = Catalog.discover(cur)
            revoke_everything(cur, catalog, grant.username)
            apply_statements(cur, catalog, grant.username,
                             grant.policy.statements)

    def drop_user(self, username):
        logger.info("dropping user {} from {}".format(username, self.name))
        with controlled_cursor(self.connect_to) as cur:
            catalog = Catalog.discover(cur)
            revoke_everything(cur, catalog, username)
            cur.connection.commit()
            drop_user(cur, username)
