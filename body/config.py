# -*- coding: utf-8 -*-
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
APP_DIR = os.path.join(BASE_DIR, 'body')
TEMPLATES_DIR = os.path.join(APP_DIR, 'templates')
STATIC_DIR = os.path.join(APP_DIR, 'static')
JS_DIR = os.path.join(STATIC_DIR, 'js')
JSX_DIR = os.path.join(STATIC_DIR, 'jsx')
CSS_DIR = os.path.join(STATIC_DIR, 'css')
IMG_DIR = os.path.join(STATIC_DIR, 'img')

RETHINK_HOST = 'localhost'
RETHINK_PORT = 28015
DB_NAME = 'test'

SECRET_KEY = 'seahorse'

SEAHORSE_EMAIL = os.environ.get('SEAHORSE_EMAIL')
SEAHORSE_EMAIL_PASS = os.environ.get('SEAHORSE_EMAIL_PASS')
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587


conf = {
    'debug': True,
    'template_path': TEMPLATES_DIR,
    'static_path': STATIC_DIR,
    'auto_reload': True,
    'xsrf_cookies': True,
    'cookie_secret': SECRET_KEY,
    'serve_traceback': True,
    'login_url': '/login/'
}
