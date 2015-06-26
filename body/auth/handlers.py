from tornado.gen import coroutine
from tornado.log import access_log
from tornado.escape import json_encode
from ..handlers import BaseHandler
from ..utils import template, is_valid_email
from .users import verify_user, add_user


class AuthBaseHandler(BaseHandler):

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", json_encode(user))
        else:
            self.clear_cookie("user")


class RegistrationHandler(AuthBaseHandler):

    def get(self):
        self.render(template('register.html'), error='')

    @coroutine
    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        if not is_valid_email(email):
            error = 'Please enter a valid email address'
            self.render(template('register.html'), error=error)

        rdb = yield add_user(self.db, email, password)
        if rdb.get('first_error') is None:
            # user added successfully
            access_log.info('%s registered and logged in.' % email)
            self.set_current_user(email)
            self.redirect('/')
        else:
            access_log.error(rdb.get('first_error'))
            error = 'An error occurred adding user to database.'
            self.render(template('register.html'), error=error)


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
            access_log.info('%s logged in.' % email)
            self.set_current_user(email)
            self.redirect(self.get_argument("next", u"/"))
        else:
            access_log.info('%s failed login.' % email)
            error = "Login incorrect"
            user = self.get_current_user()
            self.render(template("login.html"),
                        error=error,
                        user=user)


class AuthLogoutHandler(BaseHandler):

    def get(self):
        user = self.get_current_user()
        access_log.info('%s logged out.' % user)
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))
