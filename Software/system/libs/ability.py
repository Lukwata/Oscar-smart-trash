#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
from aos.system.libs.request_api import RequestApi
from aos.system.libs.user import User
from aos.system.libs.util import Util

__get_ability_list__ = "user/ability/all"
__add__ = "user/ability/add"
__remove__ = "user/ability/remove"


class Ability(object):
    def __init__(self):
        pass

    @staticmethod
    def list(token=None, product_id=None):
        try:
            list_abilities = []
            if not token and not product_id:
                user = User.get_user_info()
                if user:
                    token = user.token
                    product_id = Util.get_product_id()

            if token and product_id:
                response = RequestApi(token).get_json(__get_ability_list__, query_parameters={"product_id": product_id})
                if response:
                    if 'status' in response and response['status'] == 1:
                        data = response["data"]
                        if data:
                            for item_app in data:
                                try:
                                    if item_app["version"]:
                                        ability_data = {
                                            'is_local': item_app['is_local'],
                                            'is_service': item_app['is_service'],
                                            'is_core_app': item_app['is_core_app'],
                                            'boot': item_app['is_service'] == 1,
                                            'app': item_app['name'],
                                            'application_file': item_app['version']['application_file'],
                                            'version': item_app['version']['version'],
                                            'link': item_app['version']['source_codeURL'],
                                            'md5_hash': item_app['version']['md5_hash'],
                                            'action': ""
                                        }
                                        list_abilities.append(ability_data)
                                except Exception as e:
                                    print "data ability wrong!!!", str(e)

                            return list_abilities

        except Exception as e:
            print str(e)

        return None

    @staticmethod
    def get_all_ability_by_product_id(token=None, product_id=None):

        if not token and not product_id:
            user = User.get_user_info()
            if user:
                token = user.token
                product_id = Util.get_product_id()

        if token and product_id:
            return RequestApi(token).get_json(__get_ability_list__, query_parameters={"product_id": product_id})

        return None

    @staticmethod
    def get_all_ability(token=None):

        user = User.get_user_info()
        if user:
            return RequestApi(user.token).get_json(__get_ability_list__)

        return None

    @staticmethod
    def add(data, token=None, product_id=None):

        if not token and not product_id:
            user = User.get_user_info()
            if user:
                token = user.token
                product_id = Util.get_product_id()

        if token and product_id:
            return RequestApi(token).get_json(__add__, "POST", data=data)

        return None

    @staticmethod
    def remove(data, token=None):

        if not token:
            user = User.get_user_info()
            if user:
                return RequestApi(user.token).get_json(__remove__, "POST", data=data)

        return None
