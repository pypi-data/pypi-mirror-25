# coding: utf-8


from __future__ import unicode_literals, absolute_import
from ..exception import TigrisException
import urllib.parse


class Permission(object):
    """ Tigris Permission object """

    BASE_ENDPOINT = 'permissions'

    def __init__(self, permission_obj, session):
        """
        :param permission_obj:
            The permission data.
        :type permission_obj:
            `dict`
        :param session:
            The network session.
        :type session:
            :class:`TigrisSession`
        """
        self._session = session
        self._populate(permission_obj)

    @property
    def id(self):
        return self._id

    def _populate(self, permission_obj):
        try:
            self._id = permission_obj['id']
        except KeyError:
            self._id = False
        try:
            self.name = permission_obj['name']
        except KeyError:
            self.name = None
        try:
            self.description = permission_obj['description']
        except KeyError:
            self.description = None
        try:
            self.is_active = permission_obj['is_active']
        except KeyError:
            self.is_active = None

    def activate(self):
        """
        Changes `is_active` to `True`
        """
        if not self._id:
            raise TigrisException(
                'ERROR: You are activate an unsaved permission. '
                'Please save it first, then activate.')
        self.is_active = True
        query = '?' + urllib.parse.urlencode({'activate': self.is_active})
        url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
        url = url + query
        self._session._put(url, data={})

    def deactivate(self):
        """
        Changes `is_active` to `False`
        """
        if not self._id:
            raise TigrisException(
                'ERROR: You are activate an unsaved permission. '
                'Please save it first, then activate.')
        self.is_active = False
        query = '?' + urllib.parse.urlencode({'activate': self.is_active})
        url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
        url = url + query
        self._session._put(url, data={})

    def destroy(self):
        """
        Deletes Permission
        """
        url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
        self._session._delete(url)

    def get(self):
        """
        Retrieves Permission
        :rtype:
            `dict`
        """
        if self._id:
            url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
            content, status_code, headers = self._session._get(url)
            self._populate(content)
            return content
        else:
            return None

    def save(self, new=False):
        """
        Upserts the User object.

        :param new:
            Determines whether or not this User is to be inserted or updated.
        :type new:
            `bool`
        :rtype:
            `dict`
        """
        permission_obj = dict(vars(self))
        del permission_obj['_session']
        del permission_obj['_id']
        if new:
            content, status_code, headers = self._session._post(
                self.BASE_ENDPOINT,
                data={'fields': permission_obj})
            if 'error' in content:
                raise TigrisException(content['error'])
            self._populate(content)
        else:
            url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
            content, status_code, headers = self._session._patch(
                url,
                data={'fields': permission_obj})
            if 'error' in content:
                raise TigrisException(content['error'])
            self.get()
        return self
