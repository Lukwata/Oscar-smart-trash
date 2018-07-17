#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#


import datetime
from aos.system.sdk.python.send import send_json
from aos.system.libs.util import Util

class S2T:
    @staticmethod
    def run(command):

        product_id = Util.get_product_id()
        user_id = Util.get_user_id()
        json_data = dict()
        json_data['text'] = command
        json_data['user_id'] = user_id
        session_id = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S.%f")
        json_data['session_id'] = session_id
        json_data['product_id'] = product_id
        request = {"type": "nlu", "data": json_data, "source": ""}
        sensor_msg = request
        send_json(sensor_msg)
        print("s2t->" + command)

