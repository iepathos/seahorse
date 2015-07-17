# -*- coding: utf-8 -*-
from .handlers import RegistrationHandler, \
                      EmailVerificationHandler, \
                      PasswordResetHandler, \
                      PasswordChangeHandler, \
                      LoginHandler, \
                      LogoutHandler
from ..config import conf


auth_routes = [
    (r'/register/', RegistrationHandler),
    (r'/verify/([^/]*)', EmailVerificationHandler),
    (r'/reset/password/', PasswordResetHandler),
    (r'/change/password/', PasswordChangeHandler),
    (r'%s' % conf['login_url'], LoginHandler),
    (r'/logout/', LogoutHandler),
]
