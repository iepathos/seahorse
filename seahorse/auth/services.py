# -*- coding: utf-8 -*-
from tornado.gen import coroutine
from ..utils import encrypt, verify
from ..services import RethinkService, if_async


class UsersService(RethinkService):
    table = 'users'

    @if_async(coroutine)
    def new(self, id, raw_password):
        new_user = {
            'id': id,
            'password': encrypt(raw_password),
            'activated': False,
            'is_admin': False
        }
        if self.async:
            insert = yield self.insert(new_user)
        else:
            insert = self.insert(new_user)
        return insert

    @if_async(coroutine)
    def activate(self, id):
        if self.async:
            update = yield self.update(id, {'activated': True})
        else:
            update = self.update(id, {'activated': True})
        return update

    @if_async(coroutine)
    def is_activated(self, id):
        if self.async:
            activated = yield self.isTrue(id, 'activated')
        else:
            activated = self.isTrue(id, 'activated')
        return activated

    @if_async(coroutine)
    def verify(self, id, password):
        if self.async:
            data = yield self.get(id)
        else:
            data = self.get(id)
        if data is not None:
            return verify(password, data['password'])
        return False

    @if_async(coroutine)
    def set_password(self, id, raw_password):
        if self.async:
            update = yield self.update(id, {'password': encrypt(raw_password)})
        else:
            update = self.update(id, {'password': encrypt(raw_password)})
        return update

    @if_async(coroutine)
    def is_admin(self, id):
        if self.async:
            is_admin = yield self.isTrue(id, 'is_admin')
        else:
            is_admin = self.isTrue(id, 'is_admin')
        return is_admin
