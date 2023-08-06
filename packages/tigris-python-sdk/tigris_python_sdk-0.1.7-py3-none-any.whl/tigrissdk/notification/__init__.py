# coding: utf-8


from __future__ import unicode_literals, absolute_import
from ..exception import TigrisException
from ..auth.user import User


class Notification(object):
    """ Tigris Notification object """

    BASE_ENDPOINT = 'notifications'

    def __init__(self, notification_obj, session):
        """
        :param notification_obj:
        :type notification_obj:
            `dict`
        :param session:
            The client session
        :type session:
            :class:`TigrisSession`
        """
        self._session = session
        self._populate(notification_obj)

    @property
    def id(self):
        return self._id

    @property
    def created(self):
        return self._created

    @property
    def sender(self):
        return self._sender

    def _populate(self, notification_obj):
        """
        :param notification_obj:
            A `dict` of notification data
        :type notification_obj:
            `dict`
        """
        try:
            self._id = notification_obj['id']
        except KeyError:
            self._id = False
        try:
            self._sender = User({'id': notification_obj['sender_id']})
        except KeyError:
            self._sender = None
        try:
            self.message = notification_obj['message']
        except KeyError:
            self.message = None
        try:
            self.title = notification_obj['title']
        except KeyError:
            self.title = None
        try:
            self._created = notification_obj['created']
        except KeyError:
            self._created = None
        try:
            self.sent = notification_obj['sent']
        except KeyError:
            self.sent = None
        try:
            self.available = notification_obj['available']
        except KeyError:
            self.available = True
        try:
            self.recipients = [
                User({'id': r['id']}) for r in notification_obj['recipients']
            ]
        except KeyError:
            self.recipients = None

    def get(self):
        """
        Retrieves the Notification data.
        :rtype:
            :class:`Notification`
        """
        url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
        content, status_code, headers = self._session._get(url)
        self._populate(content)
        return self

    def save(self, new=False):
        """
        Upserts the Notification object to the DB.

        :param new:
            Determines whether or not this Notification is to be inserted or updated.
        :type new:
            `bool` (default False)
        """
        notification_obj = dict(vars(self))
        recipients = [r._id for r in self.recipients]
        del notification_obj['_id']
        del notification_obj['_created']
        del notification_obj['_session']
        if new:
            del notification_obj['recipients']
            url = self.BASE_ENDPOINT
            data = {
                'notification': notification_obj,
                'recipients': recipients
            }
            (
                content,
                status_code,
                headers
            ) = self._session.post(url, data=data)
            if 'error' in content:
                raise TigrisException(content['error'])
            self._populate(content['result'])
        else:
            notification_obj['recipients'] = recipients
            url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
            data = {'fields': notification_obj}
            (
                content,
                status_code,
                headers
            ) = self._session.put(url, data=data)
            if 'error' in content:
                raise TigrisException(content['error'])
            self.get()
        return self

    def destroy(self):
        """
        Destroys the Notification
        """
        url = '{0}/{1}'.format(self.BASE_ENDPOINT, self._id)
        self._session._delete(url)
