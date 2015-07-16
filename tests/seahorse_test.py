# -*- coding: utf-8 -*-
import os
from seahorse.mind import make_app
from seahorse.db import get_db_conn_synchronous
from tornado.testing import AsyncHTTPTestCase
from tests.mock_data import create_users, delete_users


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
APP_DIR = os.path.join(BASE_DIR, 'seahorse')
TEMPLATES_DIR = os.path.join(APP_DIR, 'templates')
STATIC_DIR = os.path.join(APP_DIR, 'static')
JS_DIR = os.path.join(STATIC_DIR, 'js')
JSX_DIR = os.path.join(STATIC_DIR, 'jsx')

SECRET_KEY = 'seahorse_test'

test_conf = {
    'debug': False,
    'template_path': TEMPLATES_DIR,
    'static_path': STATIC_DIR,
    'auto_reload': True,
    'xsrf_cookies': False,
    'cookie_secret': SECRET_KEY,
    'serve_traceback': False,
    'login_url': '/login/'
}


class SeahorseTestCase(AsyncHTTPTestCase):

    def setUp(self):
        super(SeahorseTestCase, self).setUp()
        self.db = get_db_conn_synchronous()
        self.app = self.get_app()
        create_users()

    def tearDown(self):
        super(SeahorseTestCase, self).tearDown()
        delete_users()
        self.db.close()

    def get_app(self):
        self.db = get_db_conn_synchronous()
        app = make_app(self.db, test_conf)
        return app

    def test_unauthenticated_home(self):
        url = '/'
        self.http_client.fetch(self.get_url(url), self.stop)
        response = self.wait()
        # Unauthenticated user should be redirected to login with homepage next
        self.assertTrue(
            str(response.effective_url).endswith('/login/?next=%2F')
        )

    def test_login(self):
        url = '/login/'
        # test get
        self.http_client.fetch(self.get_url(url), self.stop)
        response = self.wait()
        self.assertTrue(response.code == 200)

        # test post
