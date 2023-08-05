# -*- coding: utf-8 -*-

"""
F5 BIG-IQ auth plugin for HTTPie.
"""
import requests
from requests_f5auth import XF5Auth
from httpie.plugins import AuthPlugin

__version__ = '0.0.6'
__author__ = 'ivan mecimore'
__license__ = 'MIT'

class F5AuthPlugin(AuthPlugin):
    """Plugin registration"""

    name = 'X-F5-Auth-Token auth'
    auth_type = 'xf5'
    description = 'Authenticate using an X-F5-Auth-Token'

    def get_auth(self, username, password):
        if '//' in username:
            (provider, username) = username.split('//')
            return XF5Auth(username, password, loginProviderName=provider)

        return XF5Auth(username, password)
