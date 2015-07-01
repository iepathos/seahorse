# -*- coding: utf-8 -*-
import rethinkdb as r
from tornado.testing import AsyncHTTPTestCase
from body.soul import make_app
from body.config import RETHINK_HOST, RETHINK_PORT, DB_NAME
from body.db import get_db_conn_synchronous


class SeahorseTestCase(AsyncHTTPTestCase):

    def get_app(self):
        db_conn = get_db_conn_synchronous()
        app = make_app(db_conn)
        return app

    def test_unauthenticated_home(self):
        url = '/'
        self.http_client.fetch(self.get_url(url), self.stop)
        response = self.wait()
        # Unauthenticated user should be redirects to login with homepage next
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
