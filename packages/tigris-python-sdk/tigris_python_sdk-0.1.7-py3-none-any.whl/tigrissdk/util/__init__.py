# coding: utf-8

from __future__ import unicode_literals, absolute_import
from ..exception import TigrisException


class Util(object):
    """ A collection of utility actions. """

    BASE_ENDPOINT = 'utils'

    def __init__(self, session):
        """
        :param session:
            The client session
        :type session:
            :class:`TigrisSession`
        """
        self._session = session

    def _make_generic_post(self, endpoint, key, data):
        """
        POSTs something via the API.

        :param endpoint:
            URI endpoint
        :type endpoint:
            `str`
        :param key:
            Return key
        :type key:
            `str`
        :param data:
            Dictionary data
        :type data:
            `dict`
        :rtype:
            `str`
        """
        url = '{0}/{1}'.format(self.BASE_ENDPOINT, endpoint)
        (
            content,
            status_code,
            headers
        ) = self._session._post(url, data=data)
        if 'error' in content:
            raise TigrisException(content['error'])
        return content[key]

    def get_token(self, token):
        """
        Gets a verification token.
        :param token:
            The verification token.
        :type token:
            `str`
        :rtype:
            `dict`
        """
        url = '{0}/token/{1}'.format(self.BASE_ENDPOINT, token)
        (
            content,
            status_code,
            headers
        ) = self._session._get(url)
        return content

    def upload(self, file_obj):
        """
        Uploads file (to Azure)
        :param file_obj:
            A file object
        :type file_obj:
        :rtype:
            `str`
        """
        url = '{0}/upload'.format(self.BASE_ENDPOINT)
        (
            content,
            status_code,
            headers
        ) = self._session._post(url, data=file_obj)
        if 'error' in content:
            raise TigrisException(content['error'])
        return content['uri']

    def generate_token(self, data):
        """
        Creates a new user verification token.

        :param data:
            User data.
        :type data:
            `dict`
        :rtype:
            `str`
        """
        return self._make_generic_post('token', 'token', data)

    def reset_password(self, data):
        """
        Creates a new user verification token.

        :param data:
            User data.
        :type data:
            `dict`
        :rtype:
            `str`
        """
        return self._make_generic_post('reset-password', 'token', data)

    def send_email(self, data):
        """
        Sends email via API.

        :param data:
            Email data.
        :type data:
            `dict`
        :rtype:
            `str`
        """
        return self._make_generic_post('send-email', 'result', data)

    def finalize(self, data):
        """
        Sends email via API.

        :param data:
            Finalize verification of new user.
        :type data:
            `dict`
        :rtype:
            `str`
        """
        return self._make_generic_post('finalize', 'result', data)

    def slugify(self, text):
        """
        Slugifies text into URL.

        :param text:
            Text to slugify.
        :type text:
            `str`
        :rtype:
            `str`
        """
        url = '{0}/slugify'.format(self.BASE_ENDPOINT)
        (
            content,
            status_code,
            headers
        ) = self._session._put(url, data={'val': text})
        if 'error' in content:
            raise TigrisException(content['error'])
        return content['result']
