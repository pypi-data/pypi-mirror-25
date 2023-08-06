#!/usr/bin/env python

import sys
import ssl
import json
import urlparse
import requests

from hyperwallet.exceptions import HyperwalletAPIException
from requests_toolbelt.adapters.ssl import SSLAdapter
from hyperwallet import __version__


class ApiClient(object):
    '''
    The Hyperwallet API Client.

    :param username:
        The username of this API user. **REQUIRED**
    :param password:
        The password of this API user. **REQUIRED**
    :param server:
        The base URL of the API. **REQUIRED**
    '''

    def __init__(self, username, password, server):
        '''
        Create an instance of the API client.
        This client is used to make the calls to the Hyperwallet API.
        '''

        # Base headers and the custom User-Agent to identify this client as the
        # Hyperwallet SDK.
        self.baseHeaders = {
            'User-Agent': 'Hyperwallet Python SDK v{}'.format(__version__),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        self.username = username
        self.password = password
        self.server = server

        # The complete base URL of the API.
        self.baseUrl = urlparse.urljoin(self.server, '/rest/v3/')

        # The default connection to persist authentication and SSL settings.
        defaultSession = requests.Session()
        defaultSession.mount(self.server, SSLAdapter(ssl.PROTOCOL_TLSv1_2))
        defaultSession.auth = (self.username, self.password)
        defaultSession.headers = self.baseHeaders

        self.session = defaultSession

    def _makeRequest(self,
                     method=None,
                     url=None,
                     data=None,
                     headers=None,
                     params=None):
        '''
        Process an API response to ensure a JSON object is returned always.

        :param method:
            The HTTP method to use for the request. **REQUIRED**
        :param url:
            A partial URL to specify the API endpoint. **REQUIRED**
        :param data:
            A dictionary containing data for the request body.
        :param headers:
            A dictionary containing additional request headers.
        :param params:
            A dictionary containing query parameters.
        :returns:
            A JSON object containing the response data or an error object.

        .. note::
            The Hyperwallet API supports **GET**, **POST**, and **PUT**.
        '''

        try:
            response = self.session.request(
                method=method,
                url=urlparse.urljoin(self.baseUrl, url),
                data=data,
                headers=headers,
                params=params
            )
        except Exception as e:
            # The request failed to connect
            raise HyperwalletAPIException({
                'errors': [{
                    'code': 'COMMUNICATION_ERROR',
                    'message': 'Connection to {} failed: {}'.format(
                        self.server,
                        e.message
                    )
                }]
            })

        if response.status_code is 204:
            return {}

        content = response.content.decode('utf-8')

        try:
            json_body = json.loads(content)
        except ValueError as e:
            # The response is not JSON
            raise HyperwalletAPIException({
                'errors': [{
                    'code': 'GARBAGE_RESPONSE',
                    'message': 'Invalid response: {}'.format(e.message)
                }]
            })

        if 'errors' in json_body:
            # The response is a valid JSON error object
            raise HyperwalletAPIException(json_body)

        return json_body

    def doGet(self, partialUrl, params={}):
        '''
        Submit a GET to the API.

        :param partialUrl:
            A partial URL to specify the API endpoint. **REQUIRED**
        :param params:
            A dictionary containing query parameters.
        :returns:
            The API response.
        '''

        return self._makeRequest(
            method='GET',
            url=partialUrl,
            params=params
        )

    def doPost(self, partialUrl, data, headers={}):
        '''
        Submit a POST to the API.

        :param partialUrl:
            A partial URL to specify the API endpoint. **REQUIRED**
        :param data:
            A dictionary containing data for the request body. **REQUIRED**
        :param headers:
            A dictionary containing additional request headers.
        :returns:
            The API response.
        '''

        return self._makeRequest(
            method='POST',
            url=partialUrl,
            data=json.dumps(data).encode('utf-8'),
            headers=headers
        )

    def doPut(self, partialUrl, data):
        '''
        Submit a PUT to the API.

        :param partialUrl:
            A partial URL to specify the API endpoint. **REQUIRED**
        :param data:
            A dictionary containing data for the request body. **REQUIRED**
        :returns:
            The API response.
        '''

        return self._makeRequest(
            method='PUT',
            url=partialUrl,
            data=json.dumps(data).encode('utf-8')
        )
