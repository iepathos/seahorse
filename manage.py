#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import argparse
from tornado.ioloop import IOLoop
from seahorse.mind import run_server
from seahorse.utils import jsx_compile
from seahorse.db import build_tables, rethink_setup
from seahorse.auth.management import add_user, delete_user, activate_user


__author__ = 'Glen Baker <iepathos@gmail.com>'
__version__ = '0.4-dev'


log = logging.getLogger('seahorse')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='Seahorse Asynchronous Web Server'
        )
    parser.add_argument('-r', '--run', dest='run', action='store_true',
                        help='Runs Seahorse server')
    parser.add_argument('--build_tables', dest='build_tables',
                        action='store_true', help='Build RethinkDB tables')

    parser.add_argument('-jsx', '--jsx_compile', dest='jsx',
                        action='store_true',
                        help='Compile JSX static files into JS files')

    # user management
    parser.add_argument('--add_user', nargs='*', help='Add a user to the database. \
                        Expects id and raw password.')
    parser.add_argument('--delete_user', nargs='*', help='Delete a user from the database. \
                        Expects id.')
    parser.add_argument('--activate_user', nargs='*', help='Activate a user account. \
                        Expects id.')

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
    elif args.add_user:
        email = args.add_user[0]
        password = args.add_user[1]
        insert = add_user(email, password)
        if insert.get('errors') != 0:
            log.error('An error occured trying to add user %s to the database' % email)
            log.error(insert)
        else:
            log.info('Successfully added user %s to the database.' % email)
            log.info(insert)
    elif args.delete_user:
        email = args.delete_user[0]
        delete_user(email)
        log.info('Successfully deleted user %s from the database.' % email)
    elif args.activate_user:
        email = args.activate_user[0]
        activate_user(email)
        log.info('Activated account for user %s' % email)
    else:
        parser.print_help()
