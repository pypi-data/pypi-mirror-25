# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Generic WSGI HTTP Request / Response stuff
"""
from collections import defaultdict
from itertools import chain
from logging import getLogger

from .base import BaseRequest
from .ip_utils import get_real_user_ip

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

LOGGER = getLogger(__name__)


class PHPRequest(BaseRequest):
    """ Helper around PHP request
    """

    def __init__(self, environ):
        super(PHPRequest, self).__init__()
        self.environ = environ.get('request')

    @property
    def query_params(self):
        """ Return parsed query string from request
        """
        qs = self.environ.get('QUERY_STRING', {})
        return urlparse.parse_qs(qs)

    @property
    def form_params(self):
        # TODO: Reactivate reading the body
        return {}

    @property
    def cookies_params(self):
        return self.environ.get("COOKIE", {})

    @property
    def query_params_values(self):
        """ Return only query values as a list
        """
        return list(chain.from_iterable(self.query_params.values()))

    @property
    def client_ip(self):
        return get_real_user_ip(self.environ.get('REMOTE_ADDR'),
                                *(ip[1] for ip in self.get_client_ips_headers()))

    @property
    def hostname(self):
        return self.get_header('HTTP_HOST', self.environ.get('SERVER_NAME'))

    @property
    def method(self):
        return self.environ.get('REQUEST_METHOD')

    @property
    def client_user_agent(self):
        return self.get_header('HTTP_USER_AGENT')

    @property
    def referer(self):
        return self.get_header('HTTP_REFERER', None)

    @property
    def scheme(self):
        return self.environ.get('URL_SCHEME')

    @property
    def server_port(self):
        return self.environ.get('SERVER_PORT')

    @property
    def remote_port(self):
        return self.environ.get('REMOTE_PORT')

    @property
    def path(self):
        return self.environ.get('REQUEST_URI', '')

    @property
    def headers(self):
        return self.environ.get('HEADERS', {})

    @property
    def request_headers(self):
        return defaultdict(str, **self.headers)

    def get_header(self, name, default=''):
        """ Get a specific header name
        """
        return self.headers.get(name, default)

    @property
    def view_params(self):
        return {}

    @property
    def json_params(self):
        return {}
