# -*- coding: utf-8 -*-
"""
Seahorse blog module
"""
import os
import logging
import markdown
from ..utils import template, raise_404
from tornado.gen import coroutine
from ..handlers import BaseHandler
from ..config import MARKDOWN_DIR


log = logging.getLogger('seahorse.blog.handlers')


def get_slug(filename):
    return str(filename)[:-3]


def make_slug_md(slug):
    return str(slug)+'.md'


def read_markdown(filename):
    """Returns text of given filename."""
    f = open(filename, 'r')
    md = f.read()
    f.close()
    return md


def get_html(filename):
    md = read_markdown(filename)
    html = markdown.markdown(md)
    return html


class BlogListHandler(BaseHandler):

    def get(self):
        files = os.listdir(MARKDOWN_DIR)
        slugs = [get_slug(f) for f in files]
        self.render(template('blog/list.html'), slugs=slugs)


class BlogDetailHandler(BaseHandler):

    @coroutine
    def get(self, slug):
        filename = os.path.join(MARKDOWN_DIR, make_slug_md(slug))
        try:
            html = get_html(filename)
        except (OSError, IOError) as e:
            log.error(e)
            raise_404(self)
        self.render(template('blog/detail.html'), content=html)
