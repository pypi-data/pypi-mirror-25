from collections import namedtuple
import re
import logging
from functools import wraps
from .utils import Database
import MySQLdb as mysql
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def find_username(cur, username, host):
    cur.execute(
        "SELECT user, host FROM mysql.user WHERE user = %s AND host = %s",
        (username, host,)
    )
    return cur.fetchone()


def create_user(cur, username, host, pw):
    cur.execute("""
        CREATE USER '{username}'@'{host}'
        IDENTIFIED BY '{password}'
    """.format(username=username, host=host, password=pw))


def drop_user(cur, username, host):
    cur.execute("DROP USER '{}'@'{}'".format(username, host))


def update_pw(cur, username, host, pw):
    cur.execute("""
        ALTER USER '{username}'@'{host}'
        IDENTIFIED BY '{password}'
    """.format(username=username, host=host, password=pw))


def apply_pw(cur, username, host, pw):
    if find_username(cur, username, host):
        update_pw(cur, username, host, pw)
    else:
        create_user(cur, username, host, pw)


class Granter(object):
    def __init__(self, cur, username, host):
        self.cur = cur
        self.username = username
        self.host = host

    def apply(self, stmt):
        self.log_and_execute(
            "GRANT {perms} ON {on} TO '{username}'@'{host}'"
            .format(perms=", ".join(stmt.permissions), on=(stmt.on or "*.*"),
                    username=self.username, host=self.host)
        )

    def log_and_execute(self, sql, *args, **kwargs):
        logger.debug("sql: " + sql)
        self.cur.execute(sql, *args, **kwargs)


def apply_statements(cur, username, host, statements):
    granter = Granter(cur, username, host)
    for stmt in statements:
        granter.apply(stmt)


def revoke_everything(cur, username, host):
    cur.execute("REVOKE ALL PRIVILEGES, GRANT OPTION FROM '{}'@'{}'"
                .format(username, host))


def connect(connect_opt):
    parsed_url = urlparse(connect_opt) \
        if type(connect_opt) == str else connect_opt
    kw = {}
    for opt, attr in (("host", "hostname"),
                      ("port", "port"),
                      ("user", "username"),
                      ("passwd", "password")):
        val = getattr(parsed_url, attr)
        if val:
            kw[opt] = val
    if parsed_url.path:
        kw["db"] = parsed_url.path[1:]
    return mysql.connect(**kw)


class controlled_cursor(object):
    def __init__(self, connect_opt):
        self.connect_opt = connect_opt

    def __enter__(self):
        self._conn = connect(self.connect_opt)
        self._cursor = self._conn.cursor()
        return self._cursor

    def __exit__(self, exception_type, exception_value, traceback):
        if not exception_type:
            self._conn.commit()
        self._cursor.close()
        self._conn.close()


HOST = "%"  # Will eventually have to make this configurable

class MySQL(Database):
    def implement_grant(self, grant):
        logger.debug("implementing grant for {} in {}"
                     .format(grant.username, self.name))
        with controlled_cursor(self.parsed_url) as cur:
            if grant.password:
                apply_pw(cur, grant.username, HOST, grant.password)
            elif not find_username(cur, grant.username, HOST):
                logger.info("User has to set a password: " + grant.username)
                return
            revoke_everything(cur, grant.username, HOST)
            apply_statements(cur, grant.username, HOST, grant.policy.statements)
