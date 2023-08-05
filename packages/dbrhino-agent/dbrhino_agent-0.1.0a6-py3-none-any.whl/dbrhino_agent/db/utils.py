from collections import namedtuple
import re
import logging
from functools import wraps


class Database(object):
    def __init__(self, *, name, connect_to, parsed_url):
        self.name = name
        self.connect_to = connect_to
        self.parsed_url = parsed_url


class GrantPermission(object):
    NONE = "none"
    SELECT = "select"
