# -*- coding: utf-8 -*-
from tornado.gen import coroutine
import rethinkdb as r
from ..utils import encrypt, verify
from ..services import RethinkService


class UsersService(RethinkService):
    table = 'users'

    @coroutine
    def new(self, id, raw_password):
        new_user = {
            'id': id,
            'password': encrypt(raw_password),
            'activated': False,
            'is_admin': False
        }
        insert = yield self.insert(new_user)
        return insert

    @coroutine
    def activate(self, id):
        activated = {
            'activated': True
        }
        update = yield self.update(id, activated)
        return update

    @coroutine
    def is_activated(self, id):
        user = yield self.get(id)
        return user.get('activated', 'False')
