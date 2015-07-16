# -*- coding: utf-8 -*-
import json
import rethinkdb as r
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler
from tornado.web import authenticated
from tornado.gen import coroutine
from .db import LISTENERS
from .utils import template


class BaseHandler(RequestHandler):

    def initialize(self):
        self.db = self.application.db
        self.users = r.table('users')

    def get_current_user(self):
        username = self.get_secure_cookie("user")
        if username:
            return username[1:-1].decode("utf-8")
        return None


class BaseWebSocketHandler(WebSocketHandler):

    def get_current_user(self):
        username = self.get_secure_cookie("user")
        if username:
            return username[1:-1].decode("utf-8")
        return None


class HomeHandler(BaseHandler):

    @authenticated
    @coroutine
    def get(self):
        user = self.get_current_user()
        self.render(template('home.html'),
                    user=self.get_current_user())


class DataSyncHandler(BaseWebSocketHandler):

    @authenticated
    @coroutine
    def open(self):
        LISTENERS.append(self)

    @authenticated
    def on_message(self, message):
        self.write_message(json.dumps(message))

    @authenticated
    def on_close(self):
        LISTENERS.remove(self)
