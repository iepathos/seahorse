# -*- coding: utf-8 -*-
from seahorse.mind import make_app
from seahorse.db import get_db_conn_synchronous
from tornado.testing import AsyncHTTPTestCase
from tests.mock_data import test_conf, create_users, delete_users


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
        if not hasattr(self, 'db'):
            self.db = get_db_conn_synchronous()
        app = make_app(self.db, test_conf)
        return app

    def assertGetReturns200(self, url):
        self.http_client.fetch(self.get_url(url), self.stop)
        response = self.wait()
        self.assertTrue(response.code == 200)
