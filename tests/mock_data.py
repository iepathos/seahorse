# -*- coding: utf-8 -*-
import rethinkdb as r
from seahorse.utils import encrypt
from seahorse.db import get_db_conn_synchronous
from seahorse.auth.management import add_user, delete_user, \
                        activate_user

password = 'test'
hash = encrypt(password)


def create_test_users():
    add_user('new_user', password)
    add_user('activated_user', password)
    activate_user('activated_user')


def delete_test_users():
    delete_user('new_user')
    delete_user('activated_user')
