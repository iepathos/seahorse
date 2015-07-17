# -*- coding: utf-8 -*-
import os
import re
import string
import random
from passlib.hash import pbkdf2_sha256
from itsdangerous import TimestampSigner
from .config import conf, TEMPLATES_DIR, DOMAIN
from tornado.gen import coroutine
from tornado_smtpclient.client import SMTPAsync
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tornado.template import Loader


loader = Loader(TEMPLATES_DIR)


def template(path):
    """Template pathing shortcut function."""
    return os.path.join(conf.get('template_path'), path)


# ERRORS
def raise_404(handler):
    """Raises a 404 not found on a given handler."""
    handler.clear()
    handler.set_status(404)
    handler.render(template('errors/404.html'))


def raise_403(handler):
    """Raises a 403 forbidden on a given handler."""
    handler.clear()
    handler.set_status(403)
    handler.render(template('errors/403.html'))


# AUTH
def gen_random_string(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def gen_signature(data):
    """Generates a TimestampSignature using config SECRET_KEY."""
    s = TimestampSigner(conf.get('cookie_secret'))
    return s.sign(str(data))


def check_signature(signature, age):
    """Checks whether a timestamp signature is valid and under a given age."""
    s = TimestampSigner(conf.get('cookie_secret'))
    return s.unsign(signature, max_age=age)


def is_valid_email(address):
    """Returns True if given string matches valid email format."""
    if re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", address):
        return True
    return False


def encrypt(password):
    """SHA256 Encryption shortcut function."""
    hash = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
    return hash


def verify(password, hash):
    """SHA256 verfication shortcut function."""
    return pbkdf2_sha256.verify(password, hash)


# EMAIL
@coroutine
def _get_smtp_connection():
    """Returns an open Asynchronous SMTP connection"""
    s = SMTPAsync()
    yield s.connect(conf.get('email_host'), conf.get('email_port'))
    yield s.starttls()
    yield s.login(conf.get('email_username'), conf.get('email_pass'))
    return s


@coroutine
def send_email_string(_from, _to, msg):
    """Asynchronously emails a string"""
    s = yield _get_smtp_connection()
    yield s.sendmail(_from, _to, msg)
    yield s.quit()


@coroutine
def seamail(to, msg):
    """Sends an email Asynchronously from the SERVER_EMAIL."""
    yield send_email_string(conf.get('email_username'), to, msg)


def create_email_msg(subject, _from, _to, text, html):
    """Creates a Multipart Email Message"""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = _from
    msg['To'] = _to

    part1 = MIMEText(str(text), 'plain')
    part2 = MIMEText(html.decode('utf-8'), 'html')
    msg.attach(part1)
    msg.attach(part2)
    return msg


def seamail_msg(subject, to, text, html):
    return create_email_msg(subject, conf.get('email_username'), to, text, html)


@coroutine
def send_verification_email(email):
    signature = gen_signature(email)
    text = "%s/verify/%s" % (DOMAIN, signature)
    html = loader.load("auth/verification_email.html").generate(
                        domain=DOMAIN,
                        signature=signature
                    )

    msg = seamail_msg('Verify Your Email Address', email, text, html)
    yield seamail(email, str(msg.as_string()))


@coroutine
def send_reset_password_email(email, tmp_pass):
    text = "Your temporary password: %s" % tmp_pass
    html = loader.load("auth/reset_password_email.html").generate(
                        password=tmp_pass
                    )

    msg = seamail_msg('Verify Your Email Address', email, text, html)
    yield seamail(email, str(msg.as_string()))


@coroutine
def send_password_changed_email(email):
    text = "Your password was changed.  If you did not request this change, \
            contact our tech support immediately."
    html = loader.load("auth/password_changed_email.html").generate()

    msg = seamail_msg('Your Password Was Changed', email, text, html)
    yield seamail(email, str(msg.as_string()))

