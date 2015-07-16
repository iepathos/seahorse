# -*- coding: utf-8 -*-
from tornado.web import StaticFileHandler, Application
from tornado.log import enable_pretty_logging
from .config import conf, check_config
from .handlers import HomeHandler, DataSyncHandler
from .auth.handlers import RegistrationHandler, \
                           EmailVerificationHandler, \
                           PasswordResetHandler, \
                           LoginHandler, \
                           LogoutHandler


class Seahorse(Application):

    def __init__(self, config, db_conn):
        handlers = [
            (r'/', HomeHandler),
            (r'/register/', RegistrationHandler),
            (r'/verify/([^/]*)', EmailVerificationHandler),
            (r'/reset/password/', PasswordResetHandler),
            (r'/login/', LoginHandler),
            (r'/logout/', LogoutHandler),
            (r'/datasync/', DataSyncHandler),

            (r'/static/(.*)', StaticFileHandler,
             {'path': config['static_path']}),
        ]
        Application.__init__(self, handlers, **config)

        self.db = db_conn


def make_app(db_conn):
    enable_pretty_logging()
    check_config()
    return Seahorse(config=conf, db_conn=db_conn)
