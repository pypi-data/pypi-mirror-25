# coding: utf-8

from __future__ import unicode_literals, absolute_import

try:
    import requests as r
except:
    r = None


class TigrisSession(object):
    """
    Base session layer for Tigris.
    """

    def __init__(self,
                 base_url,
                 default_headers={}):
        """
        :param base_url:
            The customer endpoint docroot.
        :type base_url:
            `str`
        :param default_headers
        """
        self._base_url = base_url
        self._session = r.Session()
        self._default_headers = default_headers
        self._timeout = 80

    def _request(self, method, endpoint, headers, post_data=None):
        """
        Makes an HTTP request

        :param method:
            The name of the method
        :type method:
            `str`
        :param endpoint:
            The name of the endpoint
        :type endpoint:
            `str`
        :param headers:
            The name of the endpoint
        :type headers:
            `dict`
        :param post_data:
            PATCH/POST/PUT data.
        :type post_data:
            `dict`
        :rtype:
            `tuple` of `str`, `int`, `dict`
        """
        url = '{0}/{1}'.format(self._base_url, endpoint)
        try:
            try:
                result = self._session.request(method,
                                               url,
                                               headers=headers,
                                               json=post_data,
                                               timeout=self._timeout)
            except TypeError as e:
                raise TypeError(
                    'WARNING: We couldn\'t find a proper instance of '
                    'Python `requests`. You may need to update or install '
                    'the library, which you can do with `pip`: '
                    ' To update `requests`: '
                    ''
                    '    pip install -U requests '
                    ' To install `requests`:'
                    ''
                    '    pip install requests. '
                    'Alternatively, your POST data may be malformed. '
                    'Underlying error: {0}'.format(e))
            content = result.json()
            status_code = result.status_code
        except Exception as e:
            raise Exception(e)
        return content, status_code, result.headers

    def _delete(self, endpoint, headers={}):
        """
        Executes a DELETE request

        :param endpoint:
            The name of the endpoint
        :type endpoint:
            `url`
        :rtype:
            `tuple`
        """
        joined_headers = dict(headers, **self._default_headers)
        return self._request('delete', endpoint, joined_headers)

    def _get(self, endpoint, headers={}):
        """
        Executes a GET request

        :param endpoint:
            The name of the endpoint
        :type endpoint:
            `url`
        :rtype:
            `tuple`
        """
        joined_headers = dict(headers, **self._default_headers)
        return self._request('get', endpoint, joined_headers)

    def _head(self, endpoint, headers={}):
        """
        Executes a HEAD request

        :param endpoint:
            The name of the endpoint
        :type endpoint:
            `url`
        :rtype:
            `tuple`
        """
        joined_headers = dict(headers, **self._default_headers)
        return self._request('head', endpoint, joined_headers)

    def _patch(self, endpoint, data={}, headers={}):
        """
        Executes a PATCH request

        :param endpoint:
            The name of the endpoint
        :type endpoint:
            `url`
        :param data:
            The payload data to send
        :type data:
            `dict`
        :rtype:
            `tuple`
        """
        joined_headers = dict(headers, **self._default_headers)
        return self._request(
            'patch',
            endpoint,
            joined_headers,
            post_data=data)

    def _post(self, endpoint, data={}, headers={}):
        """
        Executes a POST request

        :param endpoint:
            The name of the endpoint
        :type endpoint:
            `url`
        :param data:
            The payload data to send
        :type data:
            `dict`
        :rtype:
            `tuple`
        """
        joined_headers = dict(headers, **self._default_headers)
        return self._request(
            'post',
            endpoint,
            joined_headers,
            post_data=data)

    def _put(self, endpoint, data={}, headers={}):
        """
        Executes a PATCH request

        :param endpoint:
            The name of the endpoint
        :type endpoint:
            `url`
        :param data:
            The payload data to send
        :type data:
            `dict`
        :rtype:
            `tuple`
        """
        joined_headers = dict(headers, **self._default_headers)
        return self._request(
            'put',
            endpoint,
            joined_headers,
            post_data=data)
