# -*- coding: utf-8 -*-
import rethinkdb as r
import logging
from tornado.gen import coroutine

log = logging.getLogger('seahorse.services')


def if_async(decorator):

    def conditional_decorator(fn):
        dec = decorator(fn)

        def wrapper(self, *args, **kw):
            if self.async:
                return dec(self, *args, **kw)
            return fn(self, *args, **kw)
        return wrapper

    return conditional_decorator


class RethinkService(object):
    """A RethinkDB based Service requires a
    RethinkDB connection.  It accepts asynchronous or
    synchronous connections with the async parameter.
    By default, RethinkService expects an asynchronous
    connection.  Set async=False if a synchronous
    connection is supplied."""

    table = 'set table name'
    async = True

    def __init__(self, db_conn, async=True):
        self.conn = db_conn
        self.async = async

    @if_async(coroutine)
    def make_table(self):
        try:
            if self.async:
                yield r.table_create(self.table).run(self.conn)
            else:
                r.table_create(self.table).run(self.conn)
            log.info("Table %s created successfully." % self.table)
        except r.RqlRuntimeError:
            log.info("Table %s already exists... skipping." % self.table)

    @if_async(coroutine)
    def insert(self, json_data):
        if self.async:
            insert = yield r.table(self.table)\
                            .insert(json_data)\
                            .run(self.conn)
        else:
            insert = r.table(self.table)\
                     .insert(json_data)\
                     .run(self.conn)
        return insert

    @if_async(coroutine)
    def update(self, id, json_data):
        if self.async:
            update = yield r.table(self.table)\
                            .get(id)\
                            .update(json_data)\
                            .run(self.conn)
        else:
            update = r.table(self.table)\
                      .get(id)\
                      .update(json_data)\
                      .run(self.conn)
        return update

    @if_async(coroutine)
    def delete(self, id):
        if self.async:
            yield r.table(self.table).get(id).delete().run(self.conn)
        else:
            r.table(self.table).get(id).delete().run(self.conn)

    @if_async(coroutine)
    def get(self, id):
        if self.async:
            json_data = yield r.table(self.table).get(id).run(self.conn)
        else:
            json_data = r.table(self.table).get(id).run(self.conn)
        return json_data

    @if_async(coroutine)
    def isTrue(self, id, field):
        if self.async:
            rv = yield self.get(id)
        else:
            rv = self.get(id)
        return rv.get(field, False)

    @if_async(coroutine)
    def set_field(self, id, field, val):
        if self.async:
            update = yield self.update(id, {field: val})
        else:
            update = self.update(id, {field: val})
        return update
