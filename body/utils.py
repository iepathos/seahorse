# -*- coding: utf-8 -*-
import os
import re
from react import jsx
from passlib.hash import pbkdf2_sha256
from itsdangerous import TimestampSigner
from .config import TEMPLATES_DIR, JS_DIR, JSX_DIR, SECRET_KEY


def gen_signature(data):
    """Generates a TimestampSignature using config SECRET_KEY."""
    s = TimestampSigner(SECRET_KEY)
    return s.sign(data)


def check_signature(signature, age):
    """Checks whether a timestamp signature is valid and under a given age."""
    s = TimestampSigner(SECRET_KEY)
    return s.unsign(signature, max_age=age)


def is_valid_email(address):
    """Returns True if email is valid format."""
    if re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", address):
        return True
    return False


def template(path):
    """Template pathing shortcut function."""
    return os.path.join(TEMPLATES_DIR, path)


def encrypt(password):
    """SHA256 Encryption shortcut function."""
    hash = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
    return hash


def verify(password, hash):
    """SHA256 verfication shortcut function."""
    return pbkdf2_sha256.verify(password, hash)


def raise_404(handler):
    handler.clear()
    handler.set_status(404)
    handler.render(template('404.html'))


WRONG_KEY = {
    'error': 'Wrong key.',
    'status_code': 403,
}


def rename_jsx(jsx_file):
    """Renames a .jsx filename to .js"""
    return str(jsx_file)[:-3]+'js'


def jsx_filepath(filename):
    """Returns filepath: static/jsx/filename"""
    return os.path.join(JSX_DIR, filename)


def js_filepath(filename):
    """Returns filepath: static/js/filename"""
    return os.path.join(JS_DIR, filename)


def jsx_compile():
    """Compiles .jsx files in static/jsx into .js files in static/js"""
    print('Compiling JSX static files into plain Javascript')
    transformer = jsx.JSXTransformer()
    jsx_files = os.listdir(JSX_DIR)
    for jsx_file in jsx_files:
        transformer.transform(
                jsx_filepath(jsx_file),
                js_path=js_filepath(rename_jsx(jsx_file)))
