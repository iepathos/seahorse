# -*- coding: utf-8 -*-
from tornado.web import StaticFileHandler, Application
from tornado.log import enable_pretty_logging
from tornado.gen import coroutine
from .config import conf, PORT, check_config
from .handlers import HomeHandler, DataSyncHandler
from .auth.handlers import RegistrationHandler, \
                           EmailVerificationHandler, \
                           PasswordResetHandler, \
                           LoginHandler, \
                           LogoutHandler
from .db import get_db_conn


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


def make_app(db_conn, config):
    enable_pretty_logging()
    check_config()
    return Seahorse(config=config, db_conn=db_conn)


@coroutine
def run_server():
    """Runs a development server."""
    db_conn = yield get_db_conn()
    seahorse = make_app(db_conn, conf)
    seahorse.listen(PORT)
