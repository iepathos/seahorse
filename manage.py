#!/usr/bin/env python
# -*- coding: utf-8 -*-
import code
import logging
import argparse
from tornado.ioloop import IOLoop
from seahorse.mind import run_server
from seahorse.jsx import jsx_compile
from seahorse.db import build_tables, rethink_setup, \
                        get_db_conn_synchronous
from seahorse.auth.management import add_user, delete_user, activate_user
from seahorse.auth.services import UsersService


__author__ = 'Glen Baker <iepathos@gmail.com>'
__version__ = '0.5-dev'


log = logging.getLogger('seahorse')


class AppContext(object):

    def __init__(self):
        self.db_conn = get_db_conn_synchronous()
        self.users = UsersService(self.db_conn)


def open_shell():
    """Opens an interactive shell with application context.

    Available Context Variables:

    db_conn - synchronous RethinkDB connection
    users - synchronous RethinkDB UsersService
    """
    app_ctx = AppContext()
    shell_ctx = globals()
    shell_ctx.update(vars(app_ctx))
    code.interact(local=shell_ctx)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='Seahorse Asynchronous Web Server'
        )
    parser.add_argument('-r', '--run', dest='run', action='store_true',
                        help='Runs Seahorse server.')
    parser.add_argument('--build_tables', dest='build_tables',
                        action='store_true', help='Build RethinkDB tables.')

    parser.add_argument('-jsx', '--jsx_compile', dest='jsx',
                        action='store_true',
                        help='Compile JSX static files into JS files')

    parser.add_argument('-s', '--shell', dest='shell',
                        action='store_true', help='Open an application shell.')

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
    elif args.shell:
        open_shell()
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
