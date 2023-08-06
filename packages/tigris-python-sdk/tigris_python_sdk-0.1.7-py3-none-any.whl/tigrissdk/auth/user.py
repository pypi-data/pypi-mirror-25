# coding: utf-8


from __future__ import unicode_literals, absolute_import
from ..exception import TigrisException
from .role import Role
# from ..platform.enrollment import Enrollment
import urllib.parse


class User(object):
    """ Tigris User object """

    BASE_ENDPOINT = 'users'

    def __init__(self, usr_obj, session):
        """
        Instantiates a User

        :param usr_obj:
            A dict of user data
        :type usr_obj:
            `dict`
        :param session:
        :type session:
            :class:`TigrisSession`
        """
        self._session = session
        self._populate(usr_obj)

    @property
    def id(self):
        return self._id

    @property
    def created_on(self):
        return self._created_on

    def _populate(self, usr_obj):
        try:
            self._id = usr_obj['id']
        except KeyError:
            self._id = False
        try:
            self.first_name = usr_obj['first_name']
        except KeyError:
            self.first_name = None
        try:
            self.last_name = usr_obj['last_name']
        except KeyError:
            self.last_name = None
        try:
            self.shortname = usr_obj['shortname']
        except KeyError:
            self.shortname = None
        try:
            self.email = usr_obj['email']
        except KeyError:
            self.email = None
        try:
            self.last_login = usr_obj['last_login']
        except KeyError:
            self.last_login = None
        try:
            self._created_on = usr_obj['created_on']
        except KeyError:
            self._created_on = None
        try:
            self.use_sso = usr_obj['use_sso']
        except KeyError:
            self.use_sso = False
        try:
            self.is_active = usr_obj['is_active']
        except KeyError:
            self.is_active = None
        try:
            self.roles = [Role({'id': r}, self._session) for r in usr_obj['roles']]
        except KeyError:
            self.roles = None

    def add_enrollment(self, enrollment_obj):
        url = '{0}/{1}/enrollments'.format(self.BASE_ENDPOINT, self._id)
        data = {'fields': enrollment_obj}
        content, status_code, headers = self._session._post(url, data=data)
        return content

    # @property
    # def roles(self):
    #     url = '{0}/{1}/roles'.format(self.BASE_ENDPOINT, self._id)
    #     content, status_code, headers = self._session._get(url)
    #     return content

    def get(self):
        """
        Retrieves a user by ID, username, or email
        :rtype:
            `dict`
        """
        try:
            if self._id:
                url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
                content, status_code, headers = self._session._get(url)
                self._populate(content)
                return self
            elif self.shortname:
                query = '?' + urllib.parse.urlencode(
                    {'shortname': self.shortname}
                )
                url = ''.join([self.BASE_ENDPOINT, query])
                content, status_code, headers = self._session._get(url)
                self._populate(content)
                return self
            elif self.email:
                query = '?' + urllib.parse.urlencode({'email': self.email})
                url = ''.join([self.BASE_ENDPOINT, query])
                content, status_code, headers = self._session._get(url)
                self._populate(content)
                return self
            else:
                raise TigrisException('No information to retrieve with.')
        except Exception as e:
            raise TigrisException(
                'ERROR: There is no user that can be retrieved '
                'with that information. '
                '(If the user is a new one, you can\'t get until '
                'you save the user.)'
                'Underlying error: {0}'.format(e)
            )

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
        usr_obj = dict(vars(self))
        usr_obj['id'] = self._id
        roles = [r._id for r in self.roles]
        del usr_obj['_created_on']
        del usr_obj['_session']
        del usr_obj['_id']
        if new:
            data = {
                'fields': usr_obj,
                'role': roles[0]
            }
            content, status_code, headers = self._session._post(
                self.BASE_ENDPOINT,
                data=data)
            if 'error' in content:
                raise TigrisException(content['error'])
            self._populate(content['result'])
        else:
            data = {
                'fields': usr_obj,
                'action': '',
                'roles': roles
            }
            url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
            content, status_code, headers = self._session._patch(
                url,
                data=data)
            if 'error' in content:
                raise TigrisException(content['error'])
            self.get()
        return self

    def destroy(self):
        """
        Deletes the User from Tigris
        """
        url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
        self._session._delete(url)
