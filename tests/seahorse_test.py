import rethinkdb as r
from tornado.testing import AsyncHTTPTestCase
from body.soul import make_app
from body.db import get_db_conn
from body.config import RETHINK_HOST, RETHINK_PORT, DB_NAME


class SeahorseTestCase(AsyncHTTPTestCase):

    def get_app(self):
        db_conn = r.connect(host=RETHINK_HOST,
                            port=RETHINK_PORT,
                            db=DB_NAME)
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
