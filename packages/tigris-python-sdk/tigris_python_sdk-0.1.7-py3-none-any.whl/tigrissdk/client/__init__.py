# coding: utf-8

from __future__ import unicode_literals, absolute_import

from ..session.tigris_auth_session import TigrisAuthSession
from ..auth.permission import Permission
from ..auth.role import Role
from ..auth.user import User
from ..notification import Notification
from ..platform.course import Course
from ..platform.module import Module
from ..platform.assessment import (Test, Quiz)
from ..util import Util
import urllib.parse


class Client(object):
    """Client for interacting with the Tigris REST API."""

    def __init__(self,
                 username='',
                 password='',
                 base_url=None,
                 api_token=None,
                 session=None,
                 **kwargs):
        """
        :param base_url:
            The hostname and root of the API.
        :type base_url:
            `str`
        :param username:
            The username.
        :type username:
            `str`
        :param password:
            The password.
        :type password:
            `str`
        :param api_token:
            The API token to be used in an OAuth flow.
        :type api_token:
            `str`
        :param session:
            The network session. If this is not None,
            `username` and `password` are ignored.
        :type session:
            :class:`TigrisSession`
        """
        super().__init__()

        self._api_token = api_token
        self._session = session or TigrisAuthSession(
            username=username,
            password=password,
            base_url=base_url
        )

    @property
    def session(self):
        return self._session

    @property
    def me(self):
        return self._session._user

    def course(self, course_dict):
        """
        Returns a Course object

        :param course_dict:
            course data.
        :type course_dict:
            `dict`
        :rtype:
            :class:`Course`
        """
        course = Course(course_dict, session=self._session)
        return course

    def courses(self, search=None):
        """
        Returns the list of courses.

        :param search:
            A filter query.
        :type search:
            `dict`
        :rtype:
            `list` of :class:`Course`
        """
        if search is not None:
            query = '?' + urllib.parse.urlencode(search)
        else:
            query = ''

        url = ''.join(['courses', query])
        content, status_code, headers = self._session._get(url)
        return [Course(c, session=self._session) for c in content]

    def module(self, module_dict):
        """
        Returns a Module object

        :param module_dict:
            module data.
        :type module_dict:
            `dict`
        :rtype:
            :class:`Module`
        """
        module = Module(module_dict, session=self._session)
        return module

    def modules(self, search=None):
        """
        Returns the list of modules.

        :param search:
            A filter query.
        :type search:
            `dict`
        :rtype:
            `list` of :class:`Module`
        """
        if search is not None:
            query = '?' + urllib.parse.urlencode(search)
        else:
            query = ''

        url = ''.join(['users', query])
        content, status_code, headers = self._session._get(url)
        return [Module(c, session=self._session) for c in content]

    def notification(self, notification_dict):
        """
        Returns a Notification object

        :param notification_dict:
            notification data.
        :type notification_dict:
            `dict`
        :rtype:
            :class:`Notification`
        """
        notification = Notification(notification_dict, session=self._session)
        return notification

    def notifications(self, search=None):
        """
        Returns the list of notifications.

        :param search:
            A filter query.
        :type search:
            `dict`
        :rtype:
            `list` of :class:`Notification`
        """
        if search is not None:
            query = '?' + urllib.parse.urlencode(search)
        else:
            query = ''

        url = ''.join(['users', query])
        content, status_code, headers = self._session._get(url)
        return [Notification(c, session=self._session) for c in content]

    def permission(self, permission_dict):
        """
        Returns a Permission object

        :param permission_dict:
            permission data.
        :type permission_dict:
            `dict`
        :rtype:
            :class:`Permission`
        """
        permission = Permission(permission_dict, session=self._session)
        return permission

    def permissions(self, search=None):
        """
        Returns the list of permissions.

        :param search:
            A filter query.
        :type search:
            `dict`
        :rtype:
            `list` of :class:`Permission`
        """
        if search is not None:
            query = '?' + urllib.parse.urlencode(search)
        else:
            query = ''

        url = ''.join(['users', query])
        content, status_code, headers = self._session._get(url)
        return [Permission(c, session=self._session) for c in content]

    def quiz(self, quiz_dict):
        """
        Returns a Quiz object

        :param quiz_dict:
            quiz data.
        :type quiz_dict:
            `dict`
        :rtype:
            :class:`Quiz`
        """
        quiz = Quiz(quiz_dict, session=self._session)
        return quiz

    def quizzes(self, search=None):
        """
        Returns the list of quizzes.

        :param search:
            A filter query.
        :type search:
            `dict`
        :rtype:
            `list` of :class:`Quiz`
        """
        if search is not None:
            query = '?' + urllib.parse.urlencode(search)
        else:
            query = ''

        url = ''.join(['users', query])
        content, status_code, headers = self._session._get(url)
        return [Quiz(c, session=self._session) for c in content]

    def role(self, role_dict):
        """
        Returns a Role object

        :param role_dict:
            Role data.
        :type role_dict:
            `dict`
        :rtype:
            :class:`Role`
        """
        role = Role(role_dict, session=self._session)
        return role

    def test(self, test_dict):
        """
        Returns a Test object

        :param test_dict:
            test data.
        :type test_dict:
            `dict`
        :rtype:
            :class:`Test`
        """
        test = Test(test_dict, session=self._session)
        return test

    def tests(self, search=None):
        """
        Returns the list of tests.

        :param search:
            A filter query.
        :type search:
            `dict`
        :rtype:
            `list` of :class:`Test`
        """
        if search is not None:
            query = '?' + urllib.parse.urlencode(search)
        else:
            query = ''

        url = ''.join(['users', query])
        content, status_code, headers = self._session._get(url)
        return [Test(c, session=self._session) for c in content]

    def user(self, user_dict):
        """
        Returns a User object.

        :param user_dict:
            The user data.
        :type user_dict:
            `dict`
        :rtype:
            :class:`User`
        """
        user = User(user_dict, session=self._session)
        return user

    def users(self, search=None):
        """
        Returns the list of users.

        :param search:
            A filter query.
        :type search:
            `dict`
        :rtype:
            `list` of :class:`User`
        """
        if search is not None:
            query = '?' + urllib.parse.urlencode(search)
        else:
            query = ''

        url = ''.join(['users', query])
        content, status_code, headers = self._session._get(url)
        return [User(c, session=self._session) for c in content]

    @property
    def util(self):
        """
        Creates a Util object
        """
        util = Util(session=self._session)
        return util
