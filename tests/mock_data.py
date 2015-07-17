# -*- coding: utf-8 -*-
import os
import rethinkdb as r
from seahorse.utils import encrypt
from seahorse.db import get_db_conn_synchronous
from seahorse.auth.management import add_user, delete_user, \
                        activate_user

password = 'test'
hash = encrypt(password)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
APP_DIR = os.path.join(BASE_DIR, 'seahorse')
TEMPLATES_DIR = os.path.join(APP_DIR, 'templates')
STATIC_DIR = os.path.join(APP_DIR, 'static')
JS_DIR = os.path.join(STATIC_DIR, 'js')
JSX_DIR = os.path.join(STATIC_DIR, 'jsx')

SECRET_KEY = 'seahorse_test'

test_conf = {
    'debug': False,
    'template_path': TEMPLATES_DIR,
    'static_path': STATIC_DIR,
    'auto_reload': True,
    'xsrf_cookies': False,
    'cookie_secret': SECRET_KEY,
    'serve_traceback': False,
    'login_url': '/login/',
    'email_username': 'test@gmail.com',
    'email_pass': 'test123',
    'email_host': 'smtp.gmail.com',
    'email_port': 587,
}


def create_users():
    add_user('new_user', password)
    add_user('activated_user', password)
    activate_user('activated_user')


def delete_users():
    delete_user('new_user')
    delete_user('activated_user')
