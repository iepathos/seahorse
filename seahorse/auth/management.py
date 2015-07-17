# -*- coding: utf-8 -*-
"""
Seahorse management commands are synchronous, just executed
by users from their shell using the manage.py control script.
"""
from ..db import get_db_conn_synchronous
from ..utils import encrypt
import rethinkdb as r


def delete_user(email):
    conn = get_db_conn_synchronous()
    insert = r.table('users').get(email).delete().run(conn)
    conn.close()
    return insert


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
    conn.close()
    return insert


def activate_user(email):
    conn = get_db_conn_synchronous()
    update = r.table('users').get(email).update({
            'activated': True
        }).run(conn)
    conn.close()
    return update
