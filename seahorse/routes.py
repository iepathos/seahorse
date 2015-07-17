from .handlers import HomeHandler, \
                      DataSyncHandler
from .config import conf
from .auth.routes import auth_routes
from tornado.web import StaticFileHandler

routes = [
    (r'/', HomeHandler),
    (r'/datasync/', DataSyncHandler),
    (r'/static/(.*)', StaticFileHandler,
     {'path': conf['static_path']}),
]

routes += auth_routes
