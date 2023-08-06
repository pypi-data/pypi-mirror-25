# coding: utf-8


from __future__ import unicode_literals, absolute_import
from ..exception import TigrisException
from .permission import Permission
# import urllib.parse


class Role(object):
    """ Tigris Role object """

    BASE_ENDPOINT = 'roles'

    def __init__(self, role_obj, session):
        """
        :param role_obj:
            The role data.
        :type role_obj:
            `dict`
        :param session:
            The network session.
        :type session:
            :class:`TigrisSession`
        """
        self._session = session
        self._populate(role_obj)

    @property
    def id(self):
        return self._id

    def _populate(self, role_obj):
        try:
            self._id = role_obj['id']
        except KeyError:
            self._id = False
        try:
            self.name = role_obj['name']
        except KeyError:
            self.name = None
        try:
            self.description = role_obj['description']
        except KeyError:
            self.description = None
        try:
            self.is_active = role_obj['is_active']
        except KeyError:
            self.is_active = None
        try:
            self.permissions = [Permission({'id': p}, self._session) for p in role_obj['permissions']]
        except KeyError:
            self.permissions = None

    def destroy(self):
        """
        Deletes Role
        """
        url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
        self._session._delete(url)

    def get(self):
        """
        Retrieves Role
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
        role_obj = dict(vars(self))
        del role_obj['deletable']
        del role_obj['_session']
        del role_obj['_id']
        if new:
            content, status_code, headers = self._session._post(
                self.BASE_ENDPOINT,
                data={'fields': role_obj})
            if 'error' in content:
                raise TigrisException(content['error'])
            self._populate(content)
            return self
        else:
            url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
            content, status_code, headers = self._session._patch(
                url,
                data={'fields': role_obj})
            if 'error' in content:
                raise TigrisException(content['error'])
            self.get()
            return self
