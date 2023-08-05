import re

IDENTIFIER_PATTERN = re.compile(r"^\w+$")


class Statement(object):
    def __init__(self, *, type, permissions, match=None, **kwargs):
        self.type = type
        self.match = match
        self.permissions = permissions \
            if isinstance(permissions, list) else [permissions]

    def matches_schema(self, schema):
        return self.match[0] == "*" or self.match[0] == schema


class Policy(object):
    def __init__(self, *, statements):
        stmts = []
        for stmt_def in statements:
            stmts.append(Statement(**stmt_def))
        self.statements = stmts


class Grant(object):
    def __init__(self, *, database, username, policy, password=None):
        self.database = database
        self.username = username
        self.policy = Policy(**policy)
        self.password = password
