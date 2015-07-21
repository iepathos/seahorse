# -*- coding: utf-8 -*-
from os.path import join, dirname
from os.environ import get
import logging

log = logging.getLogger('seahorse.config')

BASE_DIR = dirname(dirname(__file__))
APP_DIR = join(BASE_DIR, 'seahorse')
TEMPLATES_DIR = join(APP_DIR, 'templates')
STATIC_DIR = join(APP_DIR, 'static')
JS_DIR = join(STATIC_DIR, 'js')
JSX_DIR = join(STATIC_DIR, 'jsx')
CSS_DIR = join(STATIC_DIR, 'css')
IMG_DIR = join(STATIC_DIR, 'img')
MARKDOWN_DIR = join(STATIC_DIR, 'md')


RETHINK_HOST = get('RDB_HOST', 'localhost')
RETHINK_PORT = get('RDB_PORT', 28015)
DB_NAME = get('seahorse', 'test')

SECRET_KEY = 'seahorse'

PROTOCOL = 'http'
HOST = get('HOST', 'localhost')
PORT = get('PORT', '8888')
DOMAIN = '%s://%s:%s' % (PROTOCOL, HOST, PORT)

conf = {
    'debug': True,
    'template_path': TEMPLATES_DIR,
    'static_path': STATIC_DIR,
    'auto_reload': True,
    'xsrf_cookies': True,
    'cookie_secret': SECRET_KEY,
    'serve_traceback': True,
    'login_url': '/login/',
    'email_username': get('EMAIL_USERNAME'),
    'email_pass': get('EMAIL_PASS'),
    'email_host': 'smtp.gmail.com',
    'email_port': 587,
}


def check_config(config):
    """Runs safety and functionality checks on project configuration."""
    # Production/Debug Check
    if not config.get('debug') and config.get('cookie_secret') == 'seahorse':
        log.warn('debug is set to False, but SECRET_KEY is still default.')

    # Email Config Check
    if not config.get('email_username'):
        log.error('EMAIL_USERNAME not found in environment.')
    if not config.get('email_pass'):
        log.error('EMAIL_PASS not found in environment.')
    if not config.get('email_host'):
        log.error('Missing EMAIL_HOST')
    if not config.get('email_port'):
        log.error('Missing EMAIL_PORT')
