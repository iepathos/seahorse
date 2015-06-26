#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.ioloop import IOLoop
from body.soul import make_app
from body.db import get_db_conn, setup_tables, rethink_listener
from tornado.gen import coroutine
import threading


@coroutine
def rethink_setup():
    yield setup_tables()
    print('Starting RethinkDB listener')
    threading.Thread(target=rethink_listener).start()


@coroutine
def run_server():
    db_conn = yield get_db_conn()
    seadog = make_app(db_conn)
    seadog.listen(8888)


if __name__ == "__main__":
    rethink_setup()
    IOLoop.current().run_sync(run_server)
    IOLoop.current().start()
