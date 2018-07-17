#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import urllib2
from collections import namedtuple

from aos.system.sdk.python.send import send_json


Colors = namedtuple('Colors', 'response, success, bold, fail, end')
COLORS = Colors(
    response='\033[94m',
    success="\033[1;1;34m",
    bold="\033[;1m",
    fail='\033[91m',
    end='\033[0m',
)

TEXT_UPDATE_DESCRIPTION = "Screen will go back for few minute when complete. Do not unplug during this time!"


class Logger(object):
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)


class Help(object):
    def __init__(self):
        pass

    @staticmethod
    def success_print(message):
        """Print a message in green text.
        Parameters
            message (str)
                Message to print.
        """
        print(COLORS.success, message, COLORS.end)

    @staticmethod
    def response_print(message):
        """Print a message in blue text.
        Parameters
            message (str)
                Message to print.
        """
        print(COLORS.response, message, COLORS.end)

    @staticmethod
    def fail_print(error):
        """Print an error in red text.
        Parameters
            error
                Error object to print.
        """
        print(COLORS.fail, error, COLORS.end)

    @staticmethod
    def fail_prints(array_error):
        """Print errors in red text.
            Parameters
                errors list
                    Error list to print.
            """
        for error in array_error:
            print(COLORS.fail, error, COLORS.end)

    @staticmethod
    def paragraph_print(message):
        """Print message with padded newlines.
        Parameters
            message (str)
                Message to print.
        """
        paragraph = '\n{}\n'
        print(paragraph.format(message))

    @staticmethod
    def s2b_kill_app(ability_name):
        s = {"source": "", "type": "stop_an_ability", "data": {"ability_name": ability_name}, "protocol": ""}
        send_json(s)

    @staticmethod
    def s2b_stop_check_update():
        s = {"source": "", "type": "stop_check_update", "data": {}, "protocol": ""}
        send_json(s)

    @staticmethod
    def s2b_continue_check_update():
        s = {"source": "", "type": "continue_check_update", "data": {}, "protocol": ""}
        send_json(s)

    @staticmethod
    def s2b_start_check_internet_connection():
        s = {"source": "", "type": "start_check_internet_connection", "data": {}, "protocol": ""}
        send_json(s)

    @staticmethod
    def s2b_updating(ability_name):
        s = {"source": "", "type": "checking_update_ability",
             "data": {"ability_name": ability_name, "action": "add"}, "protocol": ""}
        send_json(s)

    @staticmethod
    def s2b_remove_updating(ability_name):
        s = {"source": "", "type": "checking_update_ability",
             "data": {"ability_name": ability_name, "action": "remove"}, "protocol": ""}
        send_json(s)

    @staticmethod
    def s2b_result_install(status, app_name, message, action):
        data = {"status": True if status == 1 else False, "message": message, "sensor": app_name,
                "type": app_name, "action": action}

        s = {"source": "", "type": "install_result", "data": data, "protocol": ""}
        send_json(s)

    @staticmethod
    def s2b_start_app(ability_name):
        send_json({"source": "", "type": ability_name, "data": {"start": "1"}, "protocol": ""})

    @staticmethod
    def open_waiting_update_ability(text, message, percentage):
        data = {"action": "add", "from": "product_control",
                "data": {"status": 1, "message": "",
                         "data": {"title": text, "desc": message, "progress": percentage}}}

        s = {"source": "", "type": "waiting_update", "data": data, "protocol": ""}
        send_json(s)

    @staticmethod
    def s2b_list_tasks(ability_name, data):
        data = {"action": "list_tasks", "from": "product_control", "data": data}
        send_json({"source": "", "type": ability_name, "data": data, "protocol": ""})

    @staticmethod
    def get_size(link):
        try:
            request = urllib2.urlopen(link)
            return int(request.info().getheaders("Content-Length")[0])
        except Exception as e:
            print (str(e))
            return 0

    @staticmethod
    def smart_bool(s):
        if s is True or s is False:
            return s
        if str(s).lower() in ("yes", "y", "true", "t", "1"):
            return True
        if str(s).lower() in ("no", "n", "false", "f", "0",
                              "0.0", "", "none", "[]", "{}"):
            return False
        raise Exception('Invalid value for boolean conversion: ' + str(s))

    @staticmethod
    def get_os_version():
        from aos.system.configs.channel import CURRENT_PATH
        import os
        os_version = CURRENT_PATH + 'data/os_version.json'
        current_version = 100
        if os.path.isfile(os_version):
            from aos.system.libs.util import Util
            data = Util.read_file(os_version)
            if data:
                return int(str(data['version']))
        return current_version + 1

    @staticmethod
    def up_os_version():
        from aos.system.configs.channel import CURRENT_PATH
        os_version = CURRENT_PATH + 'data/os_version.json'
        version = Help.get_os_version() + 1
        from aos.system.libs.util import Util
        Util.write_file(os_version, {'version': version})

    @staticmethod
    def get_os_version_api():
        try:
            import os
            from aos.system.libs.request_api import RequestApi
            api_endpoint = 'system-version?platform=SMART_DESK_3'
            from aos.system.libs.user import User
            token = User.get_user_info().access_token

            response = RequestApi(token).get_json(api_endpoint)
            if response and response['status'] == 1:
                return str(response['data']['version'])

        except Exception as e:
            print (str(e))

        return ''
