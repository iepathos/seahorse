# -*- coding: utf-8 -*-
from tornado.gen import coroutine
from tornado.log import access_log
from tornado.escape import json_encode
from ..handlers import BaseHandler
from ..utils import template, is_valid_email, \
                    check_signature, send_verification_email, \
                    gen_random_string, send_reset_password_email
from .users import verify_user, add_user, activate_user, \
                   change_password, is_activated


class AuthBaseHandler(BaseHandler):

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", json_encode(user))
        else:
            self.clear_cookie("user")


class RegistrationHandler(AuthBaseHandler):

    def get(self):
        self.render(template('auth/register.html'), error='')

    @coroutine
    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        if not is_valid_email(email):
            error = 'Please enter a valid email address'
            self.render(template('auth/register.html'), error=error)

        yield send_verification_email(email)

        rdb = yield add_user(self.db, email, password)
        if rdb.get('first_error') is None:
            # user added successfully
            access_log.info('%s registered and verification email sent.' % email)
            self.render(template('auth/verify_email.html'))
        else:
            access_log.error(rdb.get('first_error'))
            error = 'An error occurred adding user to the database.'
            self.render(template('auth/register.html'), error=error)


class EmailVerificationHandler(AuthBaseHandler):

    @coroutine
    def get(self, code):
        try:
            email = check_signature(code, 86400)  # 24 hours
        except:
            error = 'Signature %s did not authenticate.' % code
            access_log.error(error)
            self.render(template('auth/signature_invalid.html'), error='')

        email = str(email)
        yield activate_user(self.db, email)
        access_log.info('%s email verified, user account activated and logged in.' % email)
        self.set_current_user(email)
        self.redirect('/')

    @coroutine
    def post(self, code):
        email = self.get_argument('email')
        if not is_valid_email(email):
            error = 'Please enter a valid email address'
            self.render(template('auth/resend_verification.html'), error=error)
        yield send_verification_email(email)
        access_log.info('Sent email verification to %s' % email)
        self.render(template('auth/verification_sent.html'), error='')


class PasswordResetHandler(AuthBaseHandler):

    def get(self):
        error = ''
        self.render(template('auth/reset_password.html'), error=error)

    @coroutine
    def post(self):
        email = self.get_argument('email')
        if not is_valid_email(email):
            error = 'Please enter a valid email address'
            self.render(template('auth/reset_password.html'), error=error)
        # generate temporary password
        tmp_pass = gen_random_string()

        change_password(self.db, email, tmp_pass)

        yield send_reset_password_email(email, tmp_pass)
        self.redirect('/login/')


class ChangePasswordHandler(AuthBaseHandler):

    def get(self):
        pass

    def post(self, email):
        pass


class LoginHandler(AuthBaseHandler):

    def get(self):
        try:
            error = self.get_argument("error")
        except:
            error = ""
        user = self.get_current_user()
        self.render(template("auth/login.html"),
                    error=error,
                    user=user)

    @coroutine
    def post(self):
        email = self.get_argument("email", "")
        password = self.get_argument("password", "")
        auth = yield verify_user(self.db, email, password)
        if auth:
            # check if user has verfied their email address
            activated = yield is_activated(self.db, email)
            if activated:
                access_log.info('%s logged in.' % email)
                self.set_current_user(email)
                self.redirect(self.get_argument("next", u"/"))
            else:
                access_log.info('%s attempted login, but email not verified, re-sending verification email.' % email)
                yield send_verification_email(email)
                self.render(template("auth/verify_email.html"))
        else:
            access_log.info('%s failed login.' % email)
            error = "Login incorrect"
            user = self.get_current_user()
            self.render(template("auth/login.html"),
                        error=error,
                        user=user)


class LogoutHandler(BaseHandler):

    def get(self):
        user = self.get_current_user()
        access_log.info('%s logged out.' % user)
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))
