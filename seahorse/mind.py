# -*- coding: utf-8 -*-
from tornado.web import Application
from tornado.log import enable_pretty_logging
from tornado.gen import coroutine
from .config import conf, PORT, check_config
from .routes import routes
from .db import get_db_conn


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


@coroutine
def run_server():
    """Runs a development server."""
    db_conn = yield get_db_conn()
    seahorse = make_app(db_conn, conf)
    seahorse.listen(PORT)
