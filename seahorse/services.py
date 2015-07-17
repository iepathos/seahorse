# -*- coding: utf-8 -*-
import rethinkdb as r
from tornado.gen import coroutine


class RethinkService(object):
    """A RethinkDB based Service requires an asynchronous
    RethinkDB connection and a table name."""

    table = 'set table name here'

    def __init__(self, db_conn):
        self.conn = db_conn

    @coroutine
    def insert(self, json_data):
        insert = yield r.table(self.table)\
                        .insert(json_data)\
                        .run(self.conn)
        return insert

    @coroutine
    def update(self, id, json_data):
        update = yield r.table(self.table)\
                        .get(id)\
                        .update(json_data)\
                        .run(self.conn)
        return update

    @coroutine
    def delete(self, id):
        yield r.table(self.table).get(id).delete().run(self.conn)

    @coroutine
    def get(self, id):
        json_data = yield r.table(self.table).get(id).run(self.conn)
        return json_data
