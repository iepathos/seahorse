# -*- coding: utf-8 -*-
import os
import logging
from .routes import routes
from .db import get_db_conn
from tornado.gen import coroutine
from tornado.web import Application
from tornado.autoreload import watch
from tornado.log import enable_pretty_logging
from .config import conf, PORT, check_config, JSX_DIR, CSS_DIR

log = logging.getLogger('seahorse.mind')


class Seahorse(Application):

    def __init__(self, config, db_conn):
        Application.__init__(self, routes, **config)
        self.db = db_conn


def make_app(db_conn, config):
    """Generates a Seahorse Application given an asynchronous
    database connection and an appropriate config."""
    enable_pretty_logging()
    check_config()
    return Seahorse(config=config, db_conn=db_conn)


def watch_directory(directory):
    for filename in os.listdir(directory):
        watch(os.path.join(directory, filename))


def watch_jsx_files():
    log.info('Adding JSX files to autoreload watch list')
    watch_directory(JSX_DIR)


def watch_css_files():
    log.info('Adding CSS files to autoreload watch list')
    watch_directory(CSS_DIR)


def watch_static_files():
    watch_jsx_files()
    watch_css_files()


@coroutine
def run_server():
    """Runs a development server."""
    db_conn = yield get_db_conn()
    seahorse = make_app(db_conn, conf)
    if conf['debug']:
        watch_static_files()
    seahorse.listen(PORT)
