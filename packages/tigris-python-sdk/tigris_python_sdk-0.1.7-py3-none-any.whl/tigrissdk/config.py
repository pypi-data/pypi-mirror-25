# coding: utf-8

from __future__ import unicode_literals, absolute_import

from . import version
import os


class API(object):
    """Configuration object for the Tigris URL(s)."""
    BASE_URL = "{0}/api".format(os.getenv('TIGRIS_API_URI'))


class Client(object):
    """"Configuration object containing UA string."""
    VERSION = version.__version__
    USER_AGENT_STRING = 'tigris-python-sdk-{0}'.format(VERSION)
