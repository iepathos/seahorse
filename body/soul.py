# -*- coding: utf-8 -*-
from tornado.web import StaticFileHandler, Application
from tornado.log import enable_pretty_logging
from .handlers import IndexHandler
from .config import conf


class Seahorse(Application):

    def __init__(self, config, db_conn):
        handlers = [
            (r'/', IndexHandler),

            (r"/static/(.*)", StaticFileHandler,
             {'path': config['static_path']}),
        ]
        Application.__init__(self, handlers, **config)

        self.db = db_conn


def make_app(db_conn):
    # Logging
    enable_pretty_logging()
    return Seahorse(config=conf, db_conn=db_conn)
