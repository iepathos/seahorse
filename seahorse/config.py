# -*- coding: utf-8 -*-
import os
import logging

log = logging.getLogger('seahorse.config')

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
APP_DIR = os.path.join(BASE_DIR, 'seahorse')
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

EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
EMAIL_PASS = os.environ.get('EMAIL_PASS')
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587

PROTOCOL = 'http'
DOMAIN = '%s://localhost:8888' % PROTOCOL

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


def check_config():
    # Production/Debug Check
    if not conf.get('debug') and SECRET_KEY == 'seahorse':
        log.warn('debug is set to False, but SECRET_KEY is still default.')

    # Email Config Check
    if not EMAIL_USERNAME:
        log.error('EMAIL_USERNAME not found in environment.')
    if not EMAIL_PASS:
        log.error('EMAIL_PASS not found in environment.')
    if not EMAIL_HOST:
        log.error('Missing EMAIL_HOST')
    if not EMAIL_PORT:
        log.error('Missing EMAIL_PORT')
