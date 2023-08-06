# -*- coding: utf-8 -*-
# Copyright (c) 2016, 2017 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
from ._vendors.ipaddress import ip_address, ip_network
from .utils import UNICODE_CLASS


class IPNetworkListFilter(object):
    """ Matcher class for IP networks
    """

    def __init__(self, addresses=None):
        if addresses is None:
            addresses = []
        self.reset(addresses)

    def reset(self, addresses):
        """ Reset the list of matching networks
        """
        self._networks = [
            (value, ip_network(UNICODE_CLASS(value), strict=False))
            for value in addresses
        ]

    def __iter__(self):
        for value, _ in self._networks:
            yield value

    def match(self, address):
        """ Check if an IP address belongs to a network

        Return the first matching network, or None when the IP does not belong
        to any network.
        """
        if not self._networks:
            return
        ip = ip_address(UNICODE_CLASS(address))
        for value, network in self._networks:
            if ip in network:
                return value

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, list(self))

    def __str__(self):
        return ', '.join(self)


class RequestPrefixListFilter(object):
    """ Matcher class for request path prefixes
    """

    def __init__(self, prefixes=None):
        if prefixes is None:
            prefixes = []
        self.reset(prefixes)

    def reset(self, prefixes):
        """ Reset the list of request path prefixes
        """
        self._prefixes = list(prefixes)

    def __iter__(self):
        return iter(self._prefixes)

    def match(self, path):
        """ Check if a request path is matched by a prefix

        Return the first matching prefix, or None if the request path does not
        start with any recorded prefix.
        """
        if not self._prefixes:
            return
        for prefix in self._prefixes:
            if path.startswith(prefix):
                return prefix

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self._prefixes)

    def __str__(self):
        return ', '.join(self)
