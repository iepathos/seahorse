import os
import re
from passlib.hash import pbkdf2_sha256
from itsdangerous import TimestampSigner
from .config import TEMPLATES_DIR, SECRET_KEY


def gen_signature(data):
    s = TimestampSigner(SECRET_KEY)
    return s.sign(data)


def check_signature(signature, age):
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
