# coding: utf-8


from __future__ import unicode_literals, absolute_import
from ..exception import TigrisException
from .assessment import Test
from .module import Module
import urllib.parse


class Course(object):
    """ Tigris Course object """

    BASE_ENDPOINT = 'courses'

    def __init__(self, course_obj, session):
        """
        :param course_obj:
            A `dict` of the course data
        :type course_obj:
            `dict`
        :param session:
            The client session
        :type session:
            :class:`TigrisSession`
        """
        self._session = session
        self._populate(course_obj)

    @property
    def id(self):
        return self._id

    @property
    def creator(self):
        return self._creator

    @property
    def created_on(self):
        return self._created_on

    def _populate(self, course_obj):
        try:
            self._id = course_obj['id']
        except KeyError:
            self._id = False
        try:
            self.title = course_obj['title']
        except KeyError:
            self.title = None
        try:
            self.slug = course_obj['slug']
        except KeyError:
            self.slug = None
        try:
            self.teaser = course_obj['teaser']
        except KeyError:
            self.teaser = None
        try:
            self.description = course_obj['description']
        except KeyError:
            self.description = None
        try:
            self.long_description = course_obj['long_description']
        except KeyError:
            self.long_description = None
        try:
            self.tags = course_obj['tags']
        except KeyError:
            self.tags = None
        try:
            self.image = course_obj['image']
        except KeyError:
            self.image = None
        try:
            self.status = course_obj['status']
        except KeyError:
            self.status = 0
        try:
            self._created_on = course_obj['created_on']
        except KeyError:
            self._created_on = None
        try:
            self.last_updated_on = course_obj['last_updated_on']
        except KeyError:
            self.last_updated_on = None
        try:
            self._creator = course_obj['creator']
        except KeyError:
            self._creator = None

    def get(self):
        """
        Retrieves a course by ID

        :rtype:
            :class:`Course`
        """
        url = '{0}/{1}'.format(
            self.BASE_ENDPOINT,
            self._id
        )
        content, status_code, headers = self._session._get(url)
        self._populate(content)
        return self

    @property
    def modules(self):
        """
        Retrieves all modules for the course

        :rtype:
            `list` of :class:`Module`
        """
        url = '{0}/{1}/modules'.format(
            self.BASE_ENDPOINT,
            self._id
        )
        content, status_code, headers = self._session._get(url)
        modules = [Module({'id': m['id']}) for m in content]
        return modules

    @property
    def test(self):
        """
        Retrieves the course exam

        :rtype:
            :class:`Test` or `None`
        """
        query = {'course-id': self._id}
        url = '{0}?{1}'.format(
            self.BASE_ENDPOINT,
            urllib.parse.urlencode(query)
        )
        try:
            content, status, headers = self._session._get(url)
            test = Test(content)
        except:
            test = None
        return test

    def save(self, new=False):
        """
        Upserts a Course object into the DB.

        :param new:
            Determines whether or not this Course is to be inserted or updated.
        :type new:
            `bool`
        :rtype:
            `dict`
        """
        course_obj = dict(vars(self))
        course_obj['creator'] = course_obj['_creator']
        del course_obj['_id']
        del course_obj['_created_on']
        del course_obj['_creator']
        del course_obj['_session']
        if new:
            url = self.BASE_ENDPOINT
            data = {'course': course_obj}
            content, status_code, headers = self._session._post(url, data=data)
            if 'error' in content:
                raise TigrisException(content['error'])
            self._populate(content)
        else:
            url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
            data = {'course': course_obj}
            (
                content,
                status_code,
                headers
            ) = self._session._patch(url, data=data)
            if 'error' in content:
                raise TigrisException(content['error'])
            self.get()
        return self

    def destroy(self):
        """
        Deletes a course.
        """
        url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
        self._session._delete(url)

    def destroy_modules(self):
        """
        Deletes all modules in a course.
        """
        url = '{0}/{1}/modules'.format(self.BASE_ENDPOINT, self._id)
        self._session._delete(url)
