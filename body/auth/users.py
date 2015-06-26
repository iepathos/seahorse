from tornado.gen import coroutine
import rethinkdb as r
# from ..db import get_db_conn
from ..utils import encrypt, verify


@coroutine
def add_user(conn, email, password):
    # encrypt password
    hash = encrypt(password)
    insert = yield r.table('users').insert({
            'id': email,
            'password': hash,
            'funds': 0,
            'is_admin': False
        }).run(conn)
    return insert


@coroutine
def delete_user(conn, email):
    yield r.table('users').get(email).delete().run(conn)


@coroutine
def verify_user(conn, email, password):
    data = yield r.table('users').get(email).run(conn)
    if data is not None:
        return verify(password, data['password'])
    return False


@coroutine
def make_admin(conn, email):
    yield r.table('users').get(email).update({
            'is_admin': True
        }).run(conn)


@coroutine
def is_admin(conn, email):
    user = yield r.table('users').get(email).run(conn)
    return user.get('is_admin', False)
