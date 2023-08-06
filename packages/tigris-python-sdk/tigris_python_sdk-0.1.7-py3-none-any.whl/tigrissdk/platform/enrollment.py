# coding: utf-8


from __future__ import unicode_literals, absolute_import
from ..exception import TigrisException
# import urllib.parse


class Enrollment(object):
    """ Tigris Enrollment object """

    def __init__(self, enrollment_obj, session):
        """
        :param module_obj:
            A `dict` of the module data
        :type module_obj:
            `dict`
        :param session:
            The client session
        :type session:
            :class:`TigrisSession`
        """
        self.BASE_ENDPOINT = 'users/{0}/enrollments'.format(
            enrollment_obj['user_id']
        )
        self._session = session
        self._populate(enrollment_obj)

    @property
    def id(self):
        return self._id

    @property
    def user_id(self):
        return self._user_id

    @property
    def course_id(self):
        return self._course_id

    @property
    def registered_on(self):
        return self._registered_on

    @property
    def completed_on(self):
        return self._completed_on

    def _populate(self, enrollment_obj):
        try:
            self._id = enrollment_obj['id']
        except KeyError:
            self._id = False
        try:
            self._course_id = enrollment_obj['course_id']
        except KeyError:
            self._course_id = None
        try:
            self._user_id = enrollment_obj['user_id']
        except KeyError:
            self._user_id = None
        try:
            self.progress = enrollment_obj['progress']
        except KeyError:
            self.progress = None
        try:
            self._registered_on = enrollment_obj['registered_on']
        except KeyError:
            self._registered_on = None
        try:
            self._completed_on = enrollment_obj['completed_on']
        except KeyError:
            self._completed_on = None
        try:
            self.is_enrolled = enrollment_obj['is_enrolled']
        except KeyError:
            self.is_enrolled = None

    def get(self):
        """
        Retrieves the enrollment

        :rtype:
            :class:`Enrollment`
        """
        url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
        content, status_code, headers = self._session._get(url)
        self._populate(content)
        return self

    def save(self, new=False):
        """
        Upserts the Module object to the DB.
        :param new:
            Determines whether or not this Module is to be inserted or updated.
        :type new:
            `bool`
        :rtype:
            `dict`
        """
        enrollment_obj = dict(vars(self))
        del enrollment_obj['_id']
        del enrollment_obj['registered_on']
        del enrollment_obj['_session']
        if new:
            del enrollment_obj['completed_on']
            url = self.BASE_ENDPOINT
            data = {'fields': enrollment_obj}
            content, status_code, headers = self._session._post(url, data=data)
            if 'error' in content:
                raise TigrisException(content['error'])
            self._populate(content['result'])
        else:
            del enrollment_obj['course_id']
            del enrollment_obj['user_id']
            url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
            data = {'fields': enrollment_obj}
            content, status_code, headers = self._session._patch(url, data=data)
            if 'error' in content:
                raise TigrisException(content['error'])
            self.get()
        return self

    def destroy(self):
        """
        Destroys the Enrollment
        """
        url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
        self._session._delete(url)
