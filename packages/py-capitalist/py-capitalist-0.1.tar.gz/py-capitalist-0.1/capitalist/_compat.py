# coding: utf-8

try:
    from urllib.parse import urlencode
except ImportError:  # Python 2.7
    from urllib import urlencode  # noqa
