#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import threading
from tornado.ioloop import IOLoop
from body.soul import make_app
from body.db import get_db_conn, setup_tables, rethink_listener
from tornado.gen import coroutine
from body.jsx_compile import jsx_compile


__author__ = 'Glen Baker <iepathos@gmail.com>'
__version__ = '0.2-dev'


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
    parser = argparse.ArgumentParser(
            description='Seahorse Asynchronous Web Server'
        )
    parser.add_argument('--run', dest='run', action='store_true',
                        help='Runs Seahorse server')
    parser.add_argument('--jsx_compile', dest='jsx', action='store_true',
                        help='Compile JSX static files into JS files')

    args = parser.parse_args()
    if args.run:
        jsx_compile()
        rethink_setup()
        IOLoop.current().run_sync(run_server)
        IOLoop.current().start()
    elif args.jsx:
        jsx_compile()
    else:
        parser.print_help()
