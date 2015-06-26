import os
from .config import TEMPLATES_DIR, APP_PUBLIC_KEY
from passlib.hash import pbkdf2_sha256
import re


def is_valid_email(address):
    if re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", address):
        return True
    return False


def template(path):
    """Template pathing shortcut function."""
    return os.path.join(TEMPLATES_DIR, path)


def encrypt(password):
    hash = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
    return hash


def verify(password, hash):
    return pbkdf2_sha256.verify(password, hash)


def raise_404(handler):
    handler.clear()
    handler.set_status(404)
    handler.render(template('404.html'))


def verify_key(key):
    if key == APP_PUBLIC_KEY:
        return True
    return False

WRONG_KEY = {
    'error': 'Wrong key.',
    'status_code': 403,
}
