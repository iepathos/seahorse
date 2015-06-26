from tornado.escape import json_encode
from ..handlers import BaseHandler
from tornado.gen import coroutine
from ..utils import template, verify_key, WRONG_KEY
from .users import verify_user, add_user


class AuthBaseHandler(BaseHandler):

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", json_encode(user))
        else:
            self.clear_cookie("user")


class AuthLoginHandler(AuthBaseHandler):

    def get(self):
        try:
            error = self.get_argument("error")
        except:
            error = ""
        user = self.get_current_user()
        self.render(template("login.html"),
                    error=error,
                    user=user)

    @coroutine
    def post(self):
        email = self.get_argument("email", "")
        password = self.get_argument("password", "")
        auth = yield verify_user(self.db, email, password)
        if auth:
            self.set_current_user(email)
            self.redirect(self.get_argument("next", u"/"))
        else:
            error = "Login incorrect"
            user = self.get_current_user()
            self.render(template("login.html"),
                        error=error,
                        user=user)


class RegistrationHandler(AuthBaseHandler):

    def get(self):
        self.render(template('register.html'), error='')

    @coroutine
    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        rdb = yield add_user(self.db, email, password)
        if rdb.get('first_error') is None:
            # user added successfully
            # log user in and redirect
            self.set_current_user(email)
            self.redirect('/')
        else:
            # error = rdb.get('first_error')
            error = 'Error adding user to database.'
            self.render(template('register.html'), error=error)


class AuthLogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))
