#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
import sys

__author__ = 'hoangphuong'

from urllib import urlencode
import requests
import json
import os
import time

from errors import (
    UnauthorisedException, MalformedRequestException, InvalidRequestException,
    UnacceptableContentException, NotFoundException, RateLimitException, ServerException
)

__BASE_URL__ = "https://dev.autonomousbrain.com/v3/"
if 'API_BASE_URL' in os.environ:
    __BASE_URL__ = os.environ['API_BASE_URL']

#__BASE_URL__ = "https://dev.autonomousbrain.com/v4/"

current_path = os.path.dirname(os.path.abspath(__file__))

__refresh_token__ = "refresh-token"


class RequestApi(object):
    """
    Base class to handle url building, parameter encoding, adding authorisation and receiving responses.
    """

    def __init__(self, token=None):
        """
        Instantiate a new Api object.
        :param token: User token.

        """
        self.token = token

    @staticmethod
    def sanitise_path(path):
        """
        Adds a '/' to the path if it does not exist.
        :param path: Path that is to be sanitised.
        :return: string
        """
        if path[0] != '/':
            path = '/' + path

        return path

    @staticmethod
    def check_status(response):
        """
        Check the response that is returned for known exceptions and errors.
        :param response: Response that is returned from the call.
        :raise:
         MalformedRequestException if `response.status` is 400
         UnauthorisedException if `response.status` is 401
         NotFoundException if `response.status` is 404
         UnacceptableContentException if `response.status` is 406
         InvalidRequestException if `response.status` is 422
         RateLimitException if `response.status` is 429
         ServerException if `response.status` > 500
        """

        if response.status_code == 400:
            raise MalformedRequestException(response.content, response)

        if response.status_code == 401:
            raise UnauthorisedException(response.content, response)

        if response.status_code == 404:
            raise NotFoundException(response.content, response)

        if response.status_code == 406:
            raise UnacceptableContentException(response.content,response)

        if response.status_code == 422:
            raise InvalidRequestException(response.content,response)

        if response.status_code == 429:
            raise RateLimitException(response.content, response)

        if response.status_code >= 500:
            raise ServerException(response.content,response)

    def build_request(self, path, query_parameters):
        """
        Build the HTTP request by adding query parameters to the path.
        :param path: API endpoint/path to be used.
        :param query_parameters: Query parameters to be added to the request.
        :return: string
        """
        url = __BASE_URL__ + path
        if query_parameters:
            url += '?' + urlencode(query_parameters)

        return url

    @staticmethod
    def refresh_token(refresh_token):
        headers = {"Authorization": "Autonomous " + refresh_token}
        endpoint = __BASE_URL__ + __refresh_token__
        print "call api ==> " + endpoint,
        r = requests.post(endpoint, headers=headers)
        if r.status_code == 200:
            response = r.json()
            if response and 'status' in response and response['status'] == 1:
                return response['data']['access_token']

        return False

    def update_token(self):
        print "refresh-token..."
        try:
            from aos.system.libs.user import User
            user = User.get_user_info()
            self.token = RequestApi.refresh_token(user.refresh_token)
            if self.token:
                return User.update_token(self.token)
        except Exception as e:
            print str(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

        return False

    def get_json(self, uri_path, http_method='GET', query_parameters=None, data={}, headers=None):
        """
        Fetches the JSON returned, after making the call and checking for errors.
        :param uri_path: Endpoint to be used to make a request.
        :param http_method: HTTP method to be used.
        :param query_parameters: Parameters to be added to the request.
        :param data: Optional data, if required.
        :param headers: Optional headers, if required.
        :return: JSON
        """

        start_time = time.time()
        response_data = None

        try:
            query_parameters = query_parameters or {}
            headers = headers or {}

            # Add credentials to the request
            # query_parameters = self.add_credentials(query_parameters)
            if self.token:
                headers["Authorization"] = "Autonomous " + self.token

            # Build the request uri with parameters
            uri = self.build_request(uri_path, query_parameters)

            print "call API ==>" + uri
            print "with data ==> ", data

            # if http_method in ('POST', 'PUT', 'DELETE') and 'Content-Type' not in headers:
            #     headers['Content-Type'] = 'application/json'

            headers['Accept'] = 'application/json'

            response = requests.request(
                url=uri,
                method=http_method,
                data=data,
                headers=headers,
                timeout=30
            )
            print("--- %s seconds ---" % (time.time() - start_time))

            print "status ==>", response.status_code
            # print "response ==>", response.text

            if response.status_code == 401:
                if self.update_token():
                    response = requests.request(url=uri, method=http_method, data=data, headers=headers)
            if response and response.status_code == 200:
                response_data = json.loads(response.content)
            else:
                response_data = response
        except requests.Timeout:
            raise Exception("We're trying to reach our server. Please try again later.")
        except requests.ConnectionError:
            raise Exception("Can't seem to connect, please check your internet connection.")
        except Exception as e:
            print "error call API ->" + str(e)
            raise Exception("Something is broken. Please try again later.")

        return response_data
