from tornado.gen import coroutine
import rethinkdb as r
# from ..db import get_db_conn
from ..utils import encrypt, verify


@coroutine
def add_user(conn, email, raw_password):
    # encrypt password
    hash = encrypt(raw_password)
    insert = yield r.table('users').insert({
            'id': email,
            'password': hash,
            'funds': 0,
            'activated': False,
            'is_admin': False
        }).run(conn)
    return insert


@coroutine
def activate_user(conn, email):
    update = yield r.table('users').get(email).update({
            'activated': True
        }).run(conn)
    return update


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
def change_password(conn, email, raw_password):
    hash = encrypt(raw_password)
    update = yield r.table('users').get(email).update({
            'password': hash
        }).run(conn)
    return update


@coroutine
def make_admin(conn, email):
    yield r.table('users').get(email).update({
            'is_admin': True
        }).run(conn)


@coroutine
def is_admin(conn, email):
    user = yield r.table('users').get(email).run(conn)
    return user.get('is_admin', False)
