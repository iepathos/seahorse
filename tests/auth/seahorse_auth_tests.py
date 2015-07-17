# -*- coding: utf-8 -*-
from ..seahorse_tests import SeahorseTestCase


class SeahorseAuthTests(SeahorseTestCase):

    def test_home(self):
        url = '/'
        self.assertGetReturns200(url)

    def test_login(self):
        url = '/login/'
        self.assertGetReturns200(url)

    def test_register(self):
        url = '/register/'
        self.assertGetReturns200(url)

    def test_reset_password(self):
        url = '/reset/password/'
        self.assertGetReturns200(url)

    def test_change_password_unauthenticated(self):
        url = '/change/password/'
        self.http_client.fetch(self.get_url(url), self.stop)
        response = self.wait()
        expected_redirect = '/login/?next=%2Fchange%2Fpassword%2F'
        self.assertTrue(
            str(response.effective_url).endswith(expected_redirect)
        )
