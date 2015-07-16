# -*- coding: utf-8 -*-
from seahorse.mind import make_app
from seahorse.db import get_db_conn_synchronous
from tornado.testing import AsyncHTTPTestCase


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
