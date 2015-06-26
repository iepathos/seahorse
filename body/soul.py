from tornado.web import StaticFileHandler, Application
from tornado.log import enable_pretty_logging
from .handlers import IndexHandler
from .config import conf


class HotWire(Application):

    def __init__(self, config, db_conn):
        handlers = [
            (r'/', IndexHandler),

            (r'/(apple-touch-icon\.png)', StaticFileHandler,
             dict(path=config['static_path'])),
        ]
        Application.__init__(self, handlers, **config)

        self.db = db_conn


def make_love_child(db_conn):
    return HotWire(config=conf, db_conn=db_conn)


def make_app():
    # Logging
    enable_pretty_logging()

    # Routing
    app = Application([
        (r"/", IndexHandler),
    ])
    return app
