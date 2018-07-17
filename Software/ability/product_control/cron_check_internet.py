#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
# Write by Hoang Phuong
#
from threading import Thread

import time

from Commands import COMMANDS
from aos.system.sdk.python.send import send_json
from aos.system.libs.util import Util


TIME_CHECK = 60
MAX_COUNT = 3


class CronCheckInternet(Thread):

    def __init__(self):
        self.stop = True
        self.count = 0
        super(CronCheckInternet, self).__init__()

    def stop_thread(self):
        self.stop = True
        self.count = 0

    def reset(self):
        self.stop = False
        self.count = 0

    def run(self):
        while True:

            if self.stop is False:
                if not Util.internet_on():
                    self.count += 1
                    if self.count == MAX_COUNT:
                        self.send_PA()
                        self.stop_thread()
                    else:
                        time.sleep(TIME_CHECK)
            else:
                break

    def send_PA(self):
        data = {"action": COMMANDS.CHECK_INTERNET_CONNECTION, "from": "product_control",
                "data": {"data": False}}

        s = {"source": "", "type": "personal_assistant", "data": data, "protocol": ""}
        send_json(s)



CronCheckInternet().run()

