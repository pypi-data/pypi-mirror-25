from collections import namedtuple
import re
import logging
from functools import wraps
from .utils import Database
import pymysql as mysql
from pymysql.converters import escape_str
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def escape_identifier(str_):
    assert str_
    # http://tinyurl.com/y9pvdprd
    return "`{}`".format(str_.replace("`", "``"))


class MyUname(object):
    def __init__(self, username, host):
        self.username = username
        self.host = host

    def __str__(self):
        return "{}@{}".format(escape_str(self.username),
                              escape_str(self.host))


def find_username(cur, my_uname):
    cur.execute(
        "SELECT user, host FROM mysql.user WHERE user = %s AND host = %s",
        (my_uname.username, my_uname.host,)
    )
    return cur.fetchone()


def create_user(cur, my_uname, pw):
    cur.execute("CREATE USER {} IDENTIFIED BY {}"
                .format(my_uname, escape_str(pw)))


def drop_user(cur, my_uname):
    cur.execute("DROP USER {}".format(my_uname))


def update_pw(cur, my_uname, pw):
    cur.execute("ALTER USER {} IDENTIFIED BY {}"
                .format(my_uname, escape_str(pw)))


def apply_pw(cur, my_uname, pw):
    if find_username(cur, my_uname):
        update_pw(cur, my_uname, pw)
    else:
        create_user(cur, my_uname, pw)


class Granter(object):
    def __init__(self, cur, my_uname):
        self.cur = cur
        self.my_uname = my_uname

    def validate(self, stmt):
        for perm in stmt.permissions:
            if not re.match("^[a-z]+$", perm, re.IGNORECASE):
                raise Exception("{} is not a valid permission".format(perm))

    def apply(self, stmt):
        self.validate(stmt)
        quoted_match = [(x if x == "*" else escape_identifier(x))
                        for x in stmt.match]
        self.log_and_execute(
            "GRANT {perms} ON {on} TO {my_uname}"
            .format(perms=", ".join(stmt.permissions),
                    on=(".".join(quoted_match)),
                    my_uname=self.my_uname)
        )

    def log_and_execute(self, sql, *args, **kwargs):
        logger.debug("sql: " + sql)
        self.cur.execute(sql, *args, **kwargs)


def apply_statements(cur, my_uname, statements):
    granter = Granter(cur, my_uname)
    for stmt in statements:
        granter.apply(stmt)


def revoke_everything(cur, my_uname):
    cur.execute("REVOKE ALL PRIVILEGES, GRANT OPTION FROM {}"
                .format(my_uname))


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
            my_uname = MyUname(grant.username, HOST)
            if grant.password:
                apply_pw(cur, my_uname, grant.password)
            elif not find_username(cur, my_uname):
                raise Exception("User has to set a password: " + my_uname)
            revoke_everything(cur, my_uname)
            apply_statements(cur, my_uname, grant.policy.statements)
