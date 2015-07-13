# -*- coding: utf-8 -*-
from tornado.web import StaticFileHandler, Application
from tornado.log import enable_pretty_logging
from .config import conf
from .handlers import HomeHandler, DataSyncHandler
from .auth.handlers import RegistrationHandler, \
                           VerificationHandler, \
                           AuthLoginHandler, \
                           AuthLogoutHandler


class Seahorse(Application):

    def __init__(self, config, db_conn):
        handlers = [
            (r'/', HomeHandler),
            (r'/register/', RegistrationHandler),
            (r'/verify/([^/]*)', VerificationHandler),
            (r'/login/', AuthLoginHandler),
            (r'/logout/', AuthLogoutHandler),
            (r'/datasync/', DataSyncHandler),

            (r'/static/(.*)', StaticFileHandler,
             {'path': config['static_path']}),
        ]
        Application.__init__(self, handlers, **config)

        self.db = db_conn


def make_app(db_conn):
    enable_pretty_logging()
    return Seahorse(config=conf, db_conn=db_conn)
