# -*- coding: utf-8 -*-
from tornado.gen import coroutine
from ..db import get_db_conn_synchronous
from ..utils import encrypt
import rethinkdb as r


# def delete_user(user_id):
#     conn = get_db_conn_synchronous()
#     yield _delete_user(conn, user_id)


def add_user(email, raw_pass):
    conn = get_db_conn_synchronous()
    hash = encrypt(raw_pass)
    insert = r.table('users').insert({
            'id': email,
            'password': hash,
            'funds': 0,
            'activated': False,
            'is_admin': False
        }).run(conn)
    return insert
