import re

IDENTIFIER_PATTERN = re.compile(r"^\w+$")


class Statement(object):
    def __init__(self, *, permissions, type=None, match=["*"],
                 **kwargs):
        self.permissions = permissions \
            if isinstance(permissions, list) else [permissions]
        self.type = type
        self.match = match
        self.extra = kwargs

    def matches_schema(self, schema):
        return self.match[0] == "*" or self.match[0] == schema


class Policy(object):
    def __init__(self, *, statements):
        stmts = []
        for stmt_def in statements:
            stmts.append(Statement(**stmt_def))
        self.statements = stmts


class Grant(object):
    def __init__(self, *, id, database, username, policy, version,
                 password=None):
        self.id = id
        self.database = database
        self.username = username
        self.policy = Policy(**policy)
        self.version = version
        self.password = password
