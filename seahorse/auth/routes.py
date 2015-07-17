# -*- coding: utf-8 -*-
from .handlers import RegistrationHandler, \
                      EmailVerificationHandler, \
                      PasswordResetHandler, \
                      PasswordChangeHandler, \
                      LoginHandler, \
                      LogoutHandler

auth_routes = [
    (r'/register/', RegistrationHandler),
    (r'/verify/([^/]*)', EmailVerificationHandler),
    (r'/reset/password/', PasswordResetHandler),
    (r'/change/password/', PasswordChangeHandler),
    (r'/login/', LoginHandler),
    (r'/logout/', LogoutHandler),
]
