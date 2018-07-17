#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
import time
from threading import Thread

from Commands import COMMANDS
from messages import MESSAGE
from aos.system.configs.channel import CURRENT_PATH, BASE_APP
from aos.system.libs.ability import Ability
from aos.system.libs.fimware import Firmware
from aos.system.libs.util import Util
from aos.system.sdk.python.send import send_json

TIME_CHECK = 600


class CheckFirmwareUpdate(Thread):
    def __init__(self):
        self.stop = False
        self.full_list_app = None
        super(CheckFirmwareUpdate, self).__init__()

    def confirm_update_os(self):
        update_button = {
            "background": "#3897f0",
            "textColor": "#ffffff",
            "text": "Update",
            "actions": [
                {
                    "type": "product_control",
                    "source": "",
                    "data": {
                        "action": COMMANDS.FIRMWARE_UPDATE,
                        "data": {},
                        "from": "personal_assistant"
                    },
                    "protocal": ""
                },
            ]
        }

        data = {
            "title": MESSAGE.CONFIRM_FORCE_UPDATE_OS_TITLE,
            "icon": "https://s3.amazonaws.com/robotbase-cloud/static/common_icon/update.png",
            "desc": MESSAGE.CONFIRM_FORCE_UPDATE_OS_DESCRIPTION,
            "block": 1,
            "buttons": [update_button]
        }
        package = {"type": "personal_assistant", "source": "",
                   "data": {"action": "notification", "from": "product_control",
                            "data": {"message": "", "status": 1, "data": data}}}
        send_json(package)

        return False

    def check_has_update(self):

        # check new version firmware is available:
        firmware_data = Firmware.get_current()

        if firmware_data and 'status' in firmware_data and firmware_data['status'] == 1 and 'version' in firmware_data['data']:
            if Util.get_version(CURRENT_PATH) < Util.convert_version(firmware_data['data']['version']):
                if 'force_update' in firmware_data['data'] and firmware_data['data']['force_update'] == 1:
                    return self.confirm_update_os()
                else:
                    return True

        if self.full_list_app:
            for ab in self.full_list_app:
                if ab['is_core_app'] and ab['is_local'] == 1:
                    new_version = Util.convert_version(ab['version'])
                    app_base_dir = BASE_APP + ab['app']
                    app_config = Util.read_file(app_base_dir + "/config.json")
                    if not app_config or (app_config and Util.convert_version(app_config['version']) < new_version):
                        return True

        return False

    def run(self):
        while True:

            time.sleep(TIME_CHECK)

            if not self.stop:
                print "start check update ..."
                user_id = Util.get_user_id()
                product_id = Util.get_product_id()

                if user_id != -1 and product_id != '':
                    self.full_list_app = Ability.list()
                    if self.check_has_update():
                        print "Sending data to PA ====>"
                        send_json({"data": {"action": COMMANDS.NEW_FIRMWARE,
                                            "from": "product_control",
                                            "data": {"status": 1, "message": "",
                                                     "data": {
                                                         "version": CheckFirmwareUpdate.get_version_string_api()}}},
                                   "type": "personal_assistant"})
                        # time.sleep(TIME_CHECK)

    def force_check_update(self):
        self.full_list_app = Ability.list()
        if self.check_has_update():
            print "Sending data to PA ====>"
            send_json({"data": {"action": COMMANDS.NEW_FIRMWARE,
                                "from": "product_control",

                                "data": {"status": 1, "message": "",
                                         "data": {"version": CheckFirmwareUpdate.get_version_string_api()}}},
                       "type": "personal_assistant"})

    @staticmethod
    def get_version_string():
        from help import Help
        current_version = Help.get_os_version()
        return "%s.%s.%s" % (str(current_version)[0], str(current_version)[1], str(current_version)[2])

    @staticmethod
    def get_version_string_api():
        from help import Help
        return Help.get_os_version_api()
