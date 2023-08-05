# -*- coding: utf-8 -*-
"""
depends requests: https://github.com/kennethreitz/requests
"""
from .compat import str, SimpleCookie


def cookie_to_dict(cookie):
    """Convert a string cookie into a dict"""
    if isinstance(cookie, str):
        cookie = cookie.encode('utf-8')

    cookie_dict = dict()
    C = SimpleCookie(cookie)
    for morsel in C.values():
        cookie_dict[morsel.key] = morsel.value
    return cookie_dict


def dict_to_cookie(cookie_dict):
    """Convert a dict into a string cookie"""
    attrs = []
    for (key, value) in cookie_dict.items():
        attrs.append("%s=%s" % (key, value))
    return "; ".join(attrs)


def get_value_by_name(cookie, name):
    """get cookie value by name from a string cookie"""
    cookie_dict = cookie_to_dict(cookie)
    return cookie_dict.get(name)
