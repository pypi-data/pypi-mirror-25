# -*- coding: utf-8 -*-
# Copyright (c) 2016, 2017 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Utils functions to retrieve the client user ip
"""

PRIVATE_IP_PREFIX = (
    '0.',  # externally non-routable
    '10.',  # class A private block
    '169.254.',  # link-local block
    '172.16.', '172.17.', '172.18.', '172.19.',
    '172.20.', '172.21.', '172.22.', '172.23.',
    '172.24.', '172.25.', '172.26.', '172.27.',
    '172.28.', '172.29.', '172.30.', '172.31.',  # class B private blocks
    '192.0.2.',  # reserved for documentation and example code
    '192.168.',  # class C private block
    '255.255.255.',  # IPv4 broadcast address
) + (
    '2001:db8:',  # reserved for documentation and example code
    'fc00:',  # IPv6 private block
    'fe80:',  # link-local unicast
    'ff00:',  # IPv6 multicast
)

LOOPBACK_PREFIX = (
    '127.',  # IPv4 loopback device
    '::1',  # IPv6 loopback device
)


NON_PUBLIC_IP_PREFIX = PRIVATE_IP_PREFIX + LOOPBACK_PREFIX


def get_real_user_ip(remote_addr, *ips):
    """ Try to compute the real user ip from various headers
    """
    private_ip = None
    for list_ips in ips:
        for ip in list_ips.split(','):
            ip = ip.strip()
            if not ip:
                # Dummy IP address, skip it.
                continue
            elif ip.startswith(PRIVATE_IP_PREFIX):
                # Private IP address, store it nothing better comes up.
                if private_ip is None:
                    private_ip = ip
            elif not ip.startswith(LOOPBACK_PREFIX):
                # Public IP address, return immediatly.
                return ip
    if private_ip is not None and remote_addr.startswith(NON_PUBLIC_IP_PREFIX):
        return private_ip
    elif remote_addr:
        return remote_addr
