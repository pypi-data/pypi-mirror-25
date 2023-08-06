# coding: utf-8


from __future__ import unicode_literals, absolute_import
from ..exception import TigrisException
from .assessment import Quiz
import urllib.parse


class Module(object):
    """ Tigris Module object """

    def __init__(self, module_obj, session):
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
        self.BASE_ENDPOINT = 'courses/{0}/modules'.format(
            module_obj['course_id']
        )
        self._session = session
        self._populate(module_obj)

    @property
    def id(self):
        return self._id

    @property
    def creator(self):
        return self._creator

    @property
    def created_on(self):
        return self._created_on

    def _populate(self, module_obj):
        try:
            self._id = module_obj['id']
        except KeyError:
            self._id = False
        try:
            self.course_id = module_obj['course_id']
        except KeyError:
            self.course_id = False
        try:
            self.order_index = module_obj['order_index']
        except KeyError:
            self.order_index = 1
        try:
            self.title = module_obj['title']
        except KeyError:
            self.title = None
        try:
            self.slug = module_obj['slug']
        except KeyError:
            self.slug = None
        try:
            self.description = module_obj['description']
        except KeyError:
            self.tags = None
        try:
            self.content = module_obj['content']
        except KeyError:
            self.content = None
        try:
            self.is_active = module_obj['is_active']
        except KeyError:
            self.is_active = True
        try:
            self._created_on = module_obj['created_on']
        except KeyError:
            self._created_on = None
        try:
            self.last_updated_on = module_obj['last_updated_on']
        except KeyError:
            self.last_updated_on = None
        try:
            self._creator = module_obj['creator']
        except KeyError:
            self._creator = None
        return

    def get(self):
        """
        Retrieves a module by ID

        :rtype:
            :class:`Module`
        """
        url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
        content, status_code, headers = self._session._get(url)
        self._populate(content)
        return self

    @property
    def quiz(self):
        """
        Retrieves module quiz

        :rtype:
            :class:`Quiz` or `None`
        """
        query = {'module-id': self._id}
        url = '{0}?{1}'.format(
            self.BASE_ENDPOINT,
            urllib.parse.urlencode(query)
        )
        try:
            content, status, headers = self._session._get(url)
            quiz = Quiz(content)
        except:
            quiz = None
        return quiz

    def save(self, new=False):
        """
        Upsets the Module object to the DB.

        :param new:
            Determines whether or not this Module is to be inserted or updated.
        :type new:
            `bool`
        :rtype:
            `dict`
        """
        module_obj = dict(vars(self))
        module_obj['creator'] = module_obj['_creator']
        del module_obj['_id']
        del module_obj['_created_on']
        del module_obj['_creator']
        del module_obj['_session']
        if new:
            url = self.BASE_ENDPOINT
            data = {'module': module_obj}
            content, status_code, headers = self._session._post(url, data=data)
            if 'error' in content:
                raise TigrisException(content['error'])
            self._populate(content['result'])
        else:
            del module_obj['course_id']
            url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
            data = {'module': module_obj}
            content, status_code, headers = self._session._patch(url, data=data)
            if 'error' in content:
                raise TigrisException(content['error'])
            self.get()
        return self

    def destroy(self):
        """
        Deletes a module.
        """
        url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
        self._session._delete(url)
