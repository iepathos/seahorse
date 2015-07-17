# -*- coding: utf-8 -*-
from .config import conf
from .handlers import HomeHandler, \
                      DataSyncHandler
from .auth.routes import auth_routes
from .blog.routes import blog_routes
from tornado.web import StaticFileHandler

routes = [
    (r'/', HomeHandler),
    (r'/datasync/', DataSyncHandler),
    (r'/static/(.*)', StaticFileHandler,
     {'path': conf['static_path']}),
]

routes += auth_routes
routes += blog_routes
