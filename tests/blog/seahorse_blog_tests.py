# -*- coding: utf-8 -*-
from ..seahorse_tests import SeahorseTestCase


class SeahorseBlogTests(SeahorseTestCase):

    def test_blog_list(self):
        url = '/blog/'
        self.assertGetReturns200(url)

    def test_log_detail(self):
        # TODO: setup test markdown dir to check against constant
        url = '/blog/hello-world'
        self.assertGetReturns200(url)
