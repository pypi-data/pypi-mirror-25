# coding: utf-8

from __future__ import unicode_literals, absolute_import
# from session.tigris_session import TigrisSession


class BaseObject(object):
    """ The base Tigris object  """

    def __init__(self, base_url, session):
        """
        :param base_url:
            The document root/hostname of the customer's instance.
        :type base_url:
            `str`
        :param session:
            The current Tigris session
        :type session:
            :class:`TigrisSession`
        """
        return
