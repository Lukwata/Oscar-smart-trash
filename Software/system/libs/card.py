#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
import json

from aos.system.libs.request_api import RequestApi
from aos.system.libs.user import User
from aos.system.libs.util import Util

__list__ = "user/payment-setting"
__add__ = "user/cc/add"
__update__ = "user/cc/update"


class Card(object):

    def __init__(self):
        pass

    @staticmethod
    def add(data, token=None):
        headers = {
            'content-type': "application/json"
        }
        if not token:
            user = User.get_user_info()
            if user:
                token = user.token
        if token:
            return RequestApi(token).get_json(__add__, "POST", data=json.dumps(data), headers=headers)
        return None

    @staticmethod
    def update(data, token=None):
        headers = {
            'content-type': "application/json"
        }
        if not token:
            user = User.get_user_info()
            if user:
                token = user.token
        if token:
            return RequestApi(token).get_json(__update__, "PUT", data=json.dumps(data), headers=headers)
        return None

    @staticmethod
    def list(token=None):
        if not token:
            user = User.get_user_info()
            if user:
                token = user.token
        if token:
            return RequestApi(token=token).get_json(__list__)
        return None


