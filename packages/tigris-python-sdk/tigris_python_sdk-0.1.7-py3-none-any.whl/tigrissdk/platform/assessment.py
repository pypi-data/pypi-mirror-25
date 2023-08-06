# coding: utf-8


from __future__ import unicode_literals, absolute_import
from ..exception import TigrisException
# import urllib.parse


class Quiz(object):
    """ Tigris Quiz object """

    BASE_ENDPOINT = 'quizzes'

    def __init__(self, quiz_obj, session):
        """
        Instantiates a Quiz

        :param quiz_obj:
            A dict of quiz data
        :type quiz_obj:
            `dict`
        :param session:
            The client session
        :type session:
            :class:`TigrisSession`
        """
        self._session = session
        self._populate(quiz_obj)

    @property
    def id(self):
        return self._id

    @property
    def created_on(self):
        return self._created_on

    def _populate(self, quiz_obj):
        try:
            self._id = quiz_obj['id']
        except KeyError:
            self._id = False
        try:
            self.course_id = quiz_obj['course_id']
        except KeyError:
            self.course_id = None
        try:
            self.module_id = quiz_obj['module_id']
        except KeyError:
            self.module_id = None
        try:
            self.status = quiz_obj['status']
        except KeyError:
            self.status = -1
        try:
            self._created_on = quiz_obj['created_on']
        except KeyError:
            self._created_on = None
        try:
            self.last_updated_on = quiz_obj['last_updated_on']
        except KeyError:
            self.last_updated_on = None
        try:
            self.data = quiz_obj['data']
        except KeyError:
            self.data = None

    def evaluate(self, submission):
        """
        Evaluates a quiz by ID

        :param submission:
            The quiz submission.
        :type submission:
            `dict`
        :rtype:
            `dict`
        """
        url = '{0}/{1}/evaluate'.format(self.BASE_ENDPOINT, self._id)
        data = {
            'course-id': self.course_id,
            'module-id': self.module_id,
            'submission': submission
        }
        content, status_code, headers = self._session._post(
            url,
            data)
        return content['result']

    def get(self):
        """
        Retrieves a quiz by ID

        :rtype:
            `dict`
        """
        url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
        content, status_code, headers = self._session._get(url)
        self._populate(content)
        return self

    def get_log(self, user_id, enrollment_id):
        """
        Retrieves a enrollment log.

        :param user_id:
            User ID.
        :type user_id:
            `int`
        :param enrollment_id:
            Enrollment ID for the quiz.
        :type enrollment_id:
            `int`
        :rtype:
            `dict`
        """
        url = '{0}/{1}/users/{2}/enrollments/{3}'.format(
            self.BASE_ENDPOINT,
            self._id,
            user_id,
            enrollment_id)
        content, status_code, headers = self._session._get(url)
        return content

    def save(self, new=False):
        """
        Upserts the Quiz object.

        :param new:
            Determines whether or not this Quiz is to be inserted or updated.
        :type new:
            `bool`
        :rtype:
            `dict`
        """
        quiz_obj = dict(vars(self))
        del quiz_obj['status']
        del quiz_obj['_created_on']
        del quiz_obj['_session']
        del quiz_obj['_id']
        del quiz_obj['_session']
        if new:
            data = {
                'course-id': self.course_id,
                'module-id': self.module_id,
                'status': self.status,
                'details': quiz_obj
            }
            content, status_code, headers = self._session._post(
                self.BASE_ENDPOINT,
                data=data)
            if 'error' in content:
                raise TigrisException(content['error'])
            self._populate(content['result'])
        else:
            url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
            content, status_code, headers = self._session._patch(
                url,
                data={'details': quiz_obj})
            if 'error' in content:
                raise TigrisException(content['error'])
            self.get()
        return self

    def save_log(self, log, new=False):
        """
        Upserts the Quiz log

        :param log:
            The log dict.
        :type log:
            `dict`
        :param new:
            Determines whether or not this log is to be inserted or updated.
        :type new:
            `bool`
        :rtype:
            `dict`
        """
        if new:
            data = {'enrollment-id': log['enrollment_id']}
            url = '{0}/{1}'.format(self.BASE_ENDPOINT, log['enrollment_id'])
            content, status_code, headers = self._session._post(url, data=data)
        else:
            enrollment_id = log['enrollment_id']
            user_id = log['user_id']
            del log['user_id']
            del log['enrollment_id']
            data = {'details': log}
            url = '{0}/{1}/users/{2}/enrollments/{3}'.format(
                self.BASE_ENDPOINT,
                self._id,
                user_id,
                enrollment_id)
            content, status_code, headers = self._session._put(url, data=data)
        return content['result']

    def destroy(self):
        """
        Deletes the Quiz from Tigris
        """
        url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
        self._session._delete(url)

    def destroy_log(self, enrollment_id):
        """
        Deletes a quiz assessment associated with that assessment.

        :param enrollment_id:
            Enrollment ID for the quiz.
        :type enrollment_id:
            `int`
        :rtype:
            `dict`
        """
        url = '{0}/{1}/enrollment/{2}'.format(
            self.BASE_ENDPOINT,
            self._id,
            enrollment_id)
        content, status_code, headers = self._session._delete(url)
        return content


class Test(object):
    """ Tigris Test object """

    BASE_ENDPOINT = 'tests'

    def __init__(self, test_obj, session):
        """
        Instantiates a Test

        :param test_obj:
            A dict of test data
        :type test_obj:
            `dict`
        :param session:
            The client session
        :type session:
            :class:`TigrisSession`
        """
        self._session = session
        self._populate(test_obj)

    @property
    def id(self):
        return self._id

    @property
    def created_on(self):
        return self._created_on

    def _populate(self, test_obj):
        try:
            self._id = test_obj['id']
        except KeyError:
            self._id = False
        try:
            self.course_id = test_obj['course_id']
        except KeyError:
            self.course_id = None
        try:
            self.status = test_obj['status']
        except KeyError:
            self.status = -1
        try:
            self._created_on = test_obj['created_on']
        except KeyError:
            self._created_on = None
        try:
            self.last_updated_on = test_obj['last_updated_on']
        except KeyError:
            self.last_updated_on = None
        try:
            self.data = test_obj['data']
        except KeyError:
            self.data = None

    def evaluate(self, submission):
        """
        Evaluates a test by ID

        :param submission:
            The test submission.
        :type submission:
            `dict`
        :rtype:
            `dict`
        """
        url = '{0}/{1}/evaluate'.format(self.BASE_ENDPOINT, self._id)
        data = {'submission': submission}
        content, status_code, headers = self._session._post(
            url,
            data)
        return content['result']

    def get(self):
        """
        Retrieves a test by ID

        :rtype:
            `dict`
        """
        url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
        content, status_code, headers = self._session._get(url)
        self._populate(content)
        return self

    def get_log(self, user_id, enrollment_id):
        """
        Retrieves a enrollment log.

        :param user_id:
            User ID.
        :type user_id:
            `int`
        :param enrollment_id:
            Enrollment ID for the test.
        :type enrollment_id:
            `int`
        :rtype:
            `dict`
        """
        url = '{0}/{1}/users/{2}/enrollments/{3}'.format(
            self.BASE_ENDPOINT,
            self._id,
            user_id,
            enrollment_id)
        content, status_code, headers = self._session._get(url)
        return content

    def save(self, new=False):
        """
        Upserts the Test object.

        :param new:
            Determines whether or not this Test is to be inserted or updated.
        :type new:
            `bool`
        :rtype:
            `dict`
        """
        test_obj = dict(vars(self))
        del test_obj['status']
        del test_obj['_created_on']
        del test_obj['_session']
        del test_obj['_id']
        del test_obj['_session']
        if new:
            data = {
                'course-id': self.course_id,
                'status': self.status,
                'details': test_obj
            }
            content, status_code, headers = self._session._post(
                self.BASE_ENDPOINT,
                data=data)
            if 'error' in content:
                raise TigrisException(content['error'])
            self._populate(content['result'])
        else:
            url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
            content, status_code, headers = self._session._patch(
                url,
                data={'details': test_obj})
            if 'error' in content:
                raise TigrisException(content['error'])
        return content['result']

    def save_log(self, log, new=False):
        """
        Upserts the Test log

        :param log:
            The log dict.
        :type log:
            `dict`
        :param new:
            Determines whether or not this log is to be inserted or updated.
        :type new:
            `bool`
        :rtype:
            `dict`
        """
        if new:
            data = {'enrollment-id': log['enrollment_id']}
            url = '{0}/{1}'.format(self.BASE_ENDPOINT, log['enrollment_id'])
            content, status_code, headers = self._session._post(url, data=data)
        else:
            enrollment_id = log['enrollment_id']
            user_id = log['user_id']
            del log['user_id']
            del log['enrollment_id']
            data = {'details': log}
            url = '{0}/{1}/users/{2}/enrollments/{3}'.format(
                self.BASE_ENDPOINT,
                self._id,
                user_id,
                enrollment_id)
            content, status_code, headers = self._session._put(url, data=data)
        return content['result']

    def destroy(self):
        """
        Deletes the Test from Tigris
        """
        url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
        self._session._delete(url)

    def destroy_log(self, enrollment_id):
        """
        Deletes a test assessment associated with that assessment.

        :param enrollment_id:
            Enrollment ID for the test.
        :type enrollment_id:
            `int`
        :rtype:
            `dict`
        """
        url = '{0}/{1}/enrollment/{2}'.format(
            self.BASE_ENDPOINT,
            self._id,
            enrollment_id)
        content, status_code, headers = self._session._delete(url)
        return content
