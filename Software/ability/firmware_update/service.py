#!/usr/bin/env python

from __future__ import print_function

import datetime
import json
import os

from aos.system.sdk.python.send import send_json

from aos.ability.firmware_update.update_online import UpdateOnline
from aos.system.libs.util import Util
from aos.system.sdk.python.service_wrapper import AutonomousService


def output(status):
    data = {"status": status, "message": ""}
    s = {"source": "", "type": "update_firmware_result", "data": data, "protocol": ""}
    send_json(s)

def callback(data_json, error):
    data = data_json['data']
    source = data_json['source']

    UpdateOnline(data, source=source).run()


if __name__ == '__main__':
    AutonomousService().run(callback)