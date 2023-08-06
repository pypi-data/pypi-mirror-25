# coding: utf-8

from __future__ import unicode_literals, absolute_import
from tigrissdk.config import API
from ..auth.user import User
from ..config import Client
from .tigris_session import TigrisSession
from ..exception import TigrisException


class TigrisAuthSession(TigrisSession):

    def __init__(self,
                 username,
                 password,
                 base_url=None,
                 default_headers=None):
        """
        Creates a session for use in the client.

        :param username:
            The username.
        :type username:
            `str`
        :param password:
            The pasword.
        :type password:
            `str`
        """
        if base_url is not None:
            super().__init__(base_url='{0}/api'.format(base_url))
        else:
            super().__init__(base_url=API.BASE_URL)
        payload = self._authenticate(username, password)
        self._user = payload['user']
        self._token = payload['token']
        self._default_headers = {
            'User-Agent': Client.USER_AGENT_STRING,
            'Authorization': 'Token {0}'.format(self._token)
        }
        if default_headers:
            self._default_headers.update(default_headers)

    @property
    def token(self):
        return self._token

    @property
    def user(self):
        return self._user

    def _authenticate(self, username, password):
        """
        Authenticates a user by username and password

        :param username:
            The name of the username.
        :type username:
            `str`
        :param password:
            The password to authenticate against.
        :type password:
            `str`
        :rtype:
            `dict`
        """
        payload = {
            "username": username,
            "password": password
        }
        try:
            content, code, headers = super()._post(
                'users/authenticate',
                data=payload)
            if code != 200:
                raise TigrisException(
                    'Could not authenticate user in Tigris. '
                    '(HTTP Code: {0})'.format(code)
                )
        except Exception as e:
            raise TigrisException(
                'ERROR: We couldn\'t authenticate this user. '
                'This could be because the credentials are incorrect '
                'or your Tigris instance is down.'
                'Underlying error: {0}'.format(e))
        return {'user': User(content['user'], self), 'token': content['token']}

    def destroy(self):
        """
        Destroys a session
        """
        try:
            content, code, headers = super()._post('users/logout', data={})
            self._user = None
            self._token = None
        except Exception as e:
            raise TigrisException(
                'ERROR: We were not able to log you out. '
                'Either you had no authenticated session, or '
                'something went very, very wrong.'
                'Underlying error: {0}'.format(e)
            )

    def refresh(self):
        """
        Refreshes session.
        """
        payload = {'id': self._user._id}
        try:
            content, code, headers = super()._put(
                'users/refresh',
                data=payload
            )
            if code != 200:
                raise TigrisException(
                    'Could not refresh user token due to HTTP error. '
                    '(HTTP Code: {0})'.format(code)
                )
        except Exception as e:
            raise TigrisException(
                'ERROR: We couldn\'t refresh the session token. '
                'Underlying error: {0}'.format(e)
            )
        self._token = content['token']

    def whoami(self):
        return self._user.shortname
