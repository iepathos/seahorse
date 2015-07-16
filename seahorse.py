#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import argparse
from tornado.ioloop import IOLoop
from seahorse.mind import run_server
from seahorse.utils import jsx_compile
from seahorse.db import build_tables, rethink_setup


__author__ = 'Glen Baker <iepathos@gmail.com>'
__version__ = '0.4-dev'


log = logging.getLogger('seahorse')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='Seahorse Asynchronous Web Server'
        )
    parser.add_argument('--run', dest='run', action='store_true',
                        help='Runs Seahorse server')
    parser.add_argument('--jsx_compile', dest='jsx', action='store_true',
                        help='Compile JSX static files into JS files')
    parser.add_argument('--build_tables', dest='build_tables',
                        action='store_true', help='Build RethinkDB tables')

    args = parser.parse_args()
    if args.run:
        jsx_compile()
        rethink_setup()
        IOLoop.current().run_sync(run_server)
        IOLoop.current().start()
    elif args.jsx:
        jsx_compile()
    elif args.build_tables:
        IOLoop.current().run_sync(build_tables)
    else:
        parser.print_help()
