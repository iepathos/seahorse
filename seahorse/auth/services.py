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
        update = yield self.update(id, {'activated': True})
        return update

    @coroutine
    def is_activated(self, id):
        activated = yield self.bool_check(id, 'activated')
        return activated

    @coroutine
    def verify(self, id, password):
        data = yield self.get(id)
        if data is not None:
            return verify(password, data['password'])
        return False

    @coroutine
    def set_password(self, id, raw_password):
        update = yield self.update(id, {'password': encrypt(raw_password)})
        return update

    @coroutine
    def is_admin(self, id):
        is_admin = yield self.bool_check(id, 'is_admin')
        return is_admin
