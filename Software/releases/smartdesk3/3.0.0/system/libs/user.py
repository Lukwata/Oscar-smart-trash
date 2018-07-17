#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
import json

from aos.system.configs.channel import PATH_USER_CONFIG
from aos.system.libs.api import user_info
from aos.system.libs.request_api import RequestApi
from util import Util

__response_success = {"status": "1"}
__response_fail = {"status": "0"}


__login__ = "auth"
__signup__ = "user/signup"
__update__ = "user/update"
__verify_token__ = "verify-token"


class User(object):
    user_id = None
    email = None
    user_hash = None
    token = None
    access_token = None
    refresh_token = None
    full_name = None

    def __init__(self):
        super(User, self).__init__()

    @staticmethod
    def login(email, password):
        params = {'email': email, 'password': password}
        try:
            return RequestApi().get_json(__login__, "POST", data=params)
        except Exception as ex:
            print str(ex)
        return None

    @staticmethod
    def signup(name, email, password):
        params = {"name": name, 'email': email, 'password': password}
        try:
            return RequestApi().get_json(__signup__, "POST", data=params)
        except Exception as ex:
            print str(ex)
        return None

    @staticmethod
    def update_token(token):
        user_product_info = Util.get_user_data()
        user_product_info['access_token'] = token
        Util.write_file(PATH_USER_CONFIG, user_product_info)
        return True

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
    def get_user_info():
        user = None
        user_product_info = Util.get_user_data()
        if user_product_info:
            try:
                user = User()
                user.email = user_product_info['email']
                user.refresh_token = user_product_info['refresh_token'] if 'refresh_token' in user_product_info else ""
                user.access_token = user_product_info['access_token']
                user.token = user.access_token
                user.user_id = user_product_info['id']
                user.user_hash = user_product_info['user_hash']
                user.full_name = user_product_info['fullname'] if 'fullname' in user_product_info else user_product_info['full_name']
            except Exception as e:
                print 'Error get_user_info ==> ' + str(e)
        return user

    @staticmethod
    def refresh_user():
        user = User.get_user_info()
        if user is not None and user.access_token is not None:
            try:
                return RequestApi(user.access_token).get_json(__verify_token__, "GET")
            except Exception as e:
                print 'Error refresh_user ==> ' + str(e)
        return None

    @staticmethod
    def sync_user_product_info():
        from aos.system.libs.util import Util
        DATA_PATH = Util.get_current_path_app() + "data/"
        USER_DATA_PATH = DATA_PATH + "user.json"

        user_p_info = None
        try:
            os_config = Util.get_product_config()
            if os_config:
                user_product_request = user_info(os_config['user_id'], os_config['email'], os_config['user_hash'], os_config['product_id'])
                if user_product_request and user_product_request['status']:
                    user_p_info = user_product_request['data']
                    Util.write_file(USER_DATA_PATH, user_p_info)

        except Exception as e:
            print 'Error(sync_user_product_info)->' + str(e)
        return user_p_info

# if __name__ == '__main__':
#     user = User()
#     user.call_user_info(575, 'testmaya3@gmail.com', '2ea0446ad1bce750daa903f9ddddbcaf')
