""" Core class PandaScore API """

import requests
try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from .errors import TokenError, JSONReadError, DataReadError, check_status
from .util import logger


class Api(object):
    """
    Makes requests to PandaScore API

    :param access_token: API key for your pandascore.co account
    :param end_point: End point for pandascore.co api
    """

    def __init__(self,
                 access_token=None,
                 end_point='https://api.pandascore.co',
                 max_requests=None):
        self.access_token = access_token
        self.end_point = end_point
        self.max_requests = max_requests

    def __make_request(self, url, params=None):
        """
            This method will make the API request, and return the request object.
        """
        if params is None:
            params = {}

        if not self.access_token:
            raise TokenError("No token provided. Please use a valid token")

        url = urlparse.urljoin(self.end_point, url)

        transform = lambda x: x
        headers = {}
        payload = 'params'

        headers.update({'Authorization': 'Bearer ' + self.access_token})
        kwargs = {'headers': headers, payload: transform(params)}

        # remove access token from log
        headers_str = str(headers).replace(self.access_token.strip(), 'TOKEN')
        logger.debug('GET %s %s:%s %s' % (url, payload, params, headers_str))

        return requests.get(url, **kwargs)

    def __pagination(self, url, params, data, req):
        """
            Perform multiple calls in order to have a full list of elements.
            The Pandascore API paginates all resources on the index method.
        """
        all_data = data
        request_num = 1
        while req.links['last']['url'] != req.links['next']['url']:
            url = req.links['next']['url']
            req = self.__make_request(url, params)
            data = req.json(object_pairs_hook=OrderedDict)
            # Merge the lists
            all_data.extend(data)
            # Check if max_requests limit has been reached
            request_num += 1
            if self.max_requests and request_num >= self.max_requests:
                break

        return all_data

    def get_data(self, url, params=None):
        """
            This method is will return the content of the response to the request.
        """
        if params is None:
            params = dict()

        params.setdefault("per_page", 50)

        req = self.__make_request(url, params)
        check_status(200, req)

        try:
            data = req.json(object_pairs_hook=OrderedDict)
        except ValueError as e:
            raise JSONReadError('Read failed from PandaScore: %s' % str(e))

        if not req.ok:
            msg = [data[m] for m in ("id", "message") if m in data][1]
            raise DataReadError(msg)

        if 'last' in req.links and data != []:
            return self.__pagination(url, params, data, req)
        else:
            return data
