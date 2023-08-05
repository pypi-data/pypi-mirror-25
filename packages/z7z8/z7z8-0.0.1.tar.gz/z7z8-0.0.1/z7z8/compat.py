# -*- coding: utf-8 -*-

"""
pythoncompat
"""

import sys

# -------
# Pythons
# -------

# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)

# ---------
# Specifics
# ---------

if is_py2:
    from Cookie import SimpleCookie, Morsel

    builtin_str = str
    bytes = str
    str = unicode
    basestring = basestring
    numeric_types = (int, long, float)

elif is_py3:
    from http.cookies import SimpleCookie, Morsel  # noqa

    builtin_str = str
    str = str
    bytes = bytes
    basestring = (str, bytes)
    numeric_types = (int, float)
