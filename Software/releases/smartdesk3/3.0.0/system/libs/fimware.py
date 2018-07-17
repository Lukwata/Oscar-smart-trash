#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
from aos.system.configs.channel import DEVICE_TYPE
from aos.system.libs.api import call_request
from aos.system.libs.request_api import RequestApi
from aos.system.libs.user import User

__get_firmware__ = "get-system-app"


class Firmware(object):
    def __init__(self):
        pass

    @staticmethod
    def get_current(token=None):
        if token is None:
            user = User.get_user_info()
            token = user.token
        if token:
            # rs = call_request(__get_firmware__+"?platform="+DEVICE_TYPE, token=token)
            rs = RequestApi(token).get_json(__get_firmware__, "GET", {"platform": DEVICE_TYPE})
            return rs
        return None
