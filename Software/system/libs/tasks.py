#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
from aos.system.libs.request_api import RequestApi
from aos.system.libs.user import User
from aos.system.libs.util import Util

__get_task__ = "task"
__get_task_pa__ = "task-pa"
__task_value__ = "task-value"
__group_task_variable_value__ = "group-task-variable-value"


class Tasks(object):
    def __init__(self):
        pass

    @staticmethod
    def get_list_task():
        # todo get API and get list task
        # hardcode:

        list_task_return = [{ "taks_id": "1", "icon": "http://icons.iconarchive.com/icons/custom-icon-design/flatastic-8/128/Navigate-up-icon.png", "name": "Stand up", "color": "#446677", "data": { "status": None, "product": { "user_id": 1070, "product_id": "6db3fff4-b8f7-4f83-9711-1f03d15c3828", "id": 1377, "created_from": "iOS", "address_long": 106.6749844, "address_lat": 10.81171757, "timezone": "Asia/Ho_Chi_Minh", "data": { "sit": "770", "stand": "0" }, "platform": "SMART_DESK", "product_name": "Smart desk" }, "hypothesi": "hello", "type": "product_control", "app": "product_control", "secret": None, "expires_at": None, "session_id": "2017-06-22-17-21-05.240299", "timestamp" : "", "token": None, "command": "hi", "user": { "user_name": "", "id": 1070, "full_name": "annie", "email": "windy.windie@yahoo.com" }, "history_id": 31716, "action": "stand_up", "variables": {}, "user_name": None, "email": None, "refresh_token": None, "analyzed_by": "new NLU" } }, { "taks_id": "2", "icon": "http://icons.iconarchive.com/icons/custom-icon-design/flatastic-8/128/Navigate-down-icon.png", "name": "Stand up", "color": "#446677", "data": { "status": True, "product": { "user_id": 1070, "product_id": "6db3fff4-b8f7-4f83-9711-1f03d15c3828", "id": 1377, "created_from": "iOS", "address_long": 106.6749844, "address_lat": 10.81171757, "timezone": "Asia/Ho_Chi_Minh", "data": { "sit": "770", "stand": "0" }, "platform": "SMART_DESK", "product_name": "Smart desk" }, "hypothesi": "hello", "type": "product_control", "app": "product_control", "secret": None, "expires_at": None, "session_id": "2017-06-22-17-21-05.240299", "timestamp" : "", "token": None, "command": "hi", "user": { "user_name": "", "id": 1070, "full_name": "annie", "email": "windy.windie@yahoo.com" }, "action": "sit_down", "variables": {}, "user_name": None, "email": None, "refresh_token": None, "analyzed_by": "new NLU"}}]
        print list_task_return[0]
        return list_task_return

    @staticmethod
    def get_list(token=None, product_id=None, app_name=None):
        if not token and not product_id:
            user = User.get_user_info()
            if user:
                token = user.token
                product_id = Util.get_product_id()

        if token and product_id:
            query_parameters = {"product_id": product_id}
            if app_name:
                query_parameters.update({"app_name": app_name})
            return RequestApi(token).get_json(__get_task__, query_parameters=query_parameters)
        return None

    @staticmethod
    def get_list_pa(token=None, product_id=None):
        if not token and not product_id:
            user = User.get_user_info()
            if user:
                token = user.token
                product_id = Util.get_product_id()

        if token and product_id:
            query_parameters = {"product_id": product_id}
            return RequestApi(token).get_json(__get_task_pa__, query_parameters=query_parameters)

        return None

    @staticmethod
    def add(**kwargs):
        token = kwargs["token"] if "token" in kwargs else None
        if not token:
            user = User.get_user_info()
            if user:
                token = user.token

        data = {}
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                data[key] = value

        if token:
            return RequestApi(token).get_json(__task_value__, "POST", data=data)

        return None

    @staticmethod
    def edit(**kwargs):
        token = kwargs["token"] if "token" in kwargs else None
        if not token:
            user = User.get_user_info()
            if user:
                token = user.token
        data = {}
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                data[key] = value

        if token:
            return RequestApi(token).get_json(__task_value__, "PUT", data=data)

        return None

    @staticmethod
    def user_remove_group_variable_value(id, token=None):
        if not token:
            user = User.get_user_info()
            if user:
                token = user.token

        data = {"id": id}

        if token:
            return RequestApi(token).get_json(__group_task_variable_value__, "DELETE", data=data)

        return None

    @staticmethod
    def user_set_default_group_variable_value(data, token=None):
        if not token:
            user = User.get_user_info()
            if user:
                token = user.token

        if token:
            return RequestApi(token).get_json(__group_task_variable_value__, "PUT", data=data)

        return None


