# -*- coding: utf-8 -*-
from .handlers import BlogListHandler, BlogDetailHandler

blog_routes = [
    (r'/blog/', BlogListHandler),
    (r'/blog/([^/]*)', BlogDetailHandler),
]
