from collections import namedtuple
import re
import logging
from functools import wraps


class Database(object):
    def __init__(self, *, name, connect_to, parsed_url):
        self.name = name
        self.connect_to = connect_to
        self.parsed_url = parsed_url
        self.type = parsed_url.scheme


class GrantPermission(object):
    NONE = "none"
    SELECT = "select"


def first_column(cur):
    return [x for x, in cur.fetchall()]


class NoPasswordException(Exception):
    def __init__(self, username):
        msg = "User {} has to set a password".format(username)
        super().__init__(msg)
