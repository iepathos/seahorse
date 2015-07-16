# -*- coding: utf-8 -*-
from tornado.gen import coroutine
from tornado.log import access_log
from tornado.escape import json_encode
from ..handlers import BaseHandler
from ..utils import template, is_valid_email, \
                    check_signature, send_verification_email, \
                    gen_random_string, send_reset_password_email, \
                    send_password_changed_email
from .users import verify_user, add_user, activate_user, \
                   change_password, is_activated
from tornado.web import authenticated
import logging

log = logging.getLogger('seahorse.auth.handlers')


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
            access_log.info('%s registered and \
                            verification email sent.' % email)
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

        email = str(email)[2:-1]
        yield activate_user(self.db, email)
        access_log.info('%s email verified, \
                        user account activated and logged in.' % email)
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

        tmp_pass = gen_random_string()
        change_password(self.db, email, tmp_pass)
        yield send_reset_password_email(email, tmp_pass)
        self.redirect('/login/')


class PasswordChangeHandler(AuthBaseHandler):

    @authenticated
    def get(self):
        error = ''
        self.render(template('auth/change_password.html'), error=error)

    @coroutine
    @authenticated
    def post(self):
        old_pass = self.get_argument('old_password')
        new_pass = self.get_argument('new_password')
        new_pass_verify = self.get_argument('new_password1')
        email = self.get_current_user()
        if new_pass != new_pass_verify:
            error = 'New passwords must match'
            self.render(template('auth/change_password.html'), error=error)

        auth = yield verify_user(self.db, email, old_pass)
        if auth:
            change_password(self.db, email, new_pass)
            yield send_password_changed_email(email)
            self.redirect('/')
        else:
            access_log.info('Change password requested by %s, \
                            but wrong old password' % email)
            error = 'Wrong password, try again?'
            self.render(template('auth/change_password.html'), error=error)


class LoginHandler(AuthBaseHandler):

    def get(self):
        try:
            error = self.get_argument("error")
        except:
            error = ""
        self.render(template("auth/login.html"),
                    error=error,
                    user=self.get_current_user())

    @coroutine
    def post(self):
        email = self.get_argument("email")
        password = self.get_argument("password")
        auth = yield verify_user(self.db, email, password)
        if auth:
            # check if user has verfied their email address
            activated = yield is_activated(self.db, email)
            if activated:
                access_log.info('%s logged in.' % email)
                self.set_current_user(email)
                self.redirect(self.get_argument("next", u"/"))
            else:
                access_log.info('%s attempted login, \
                                but email not verified, \
                                re-sending verification email.' % email)
                yield send_verification_email(email)
                self.render(template("auth/verify_email.html"))
        else:
            access_log.info('%s failed login.' % email)
            self.render(template("auth/login.html"),
                        error="Login incorrect",
                        user=self.get_current_user())


class LogoutHandler(BaseHandler):

    def get(self):
        user = self.get_current_user()
        access_log.info('%s logged out.' % user)
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))
