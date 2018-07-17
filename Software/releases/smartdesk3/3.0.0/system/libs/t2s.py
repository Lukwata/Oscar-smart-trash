#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#

import unicodedata

from aos.system.sdk.python.send import send_json

class T2S:
    @staticmethod
    def run(text):
        if type(text) == type(u''):
            text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
        elif type(text) == type(''):
            text = unicodedata.normalize('NFKD', text.decode('utf8')).encode('ascii', 'ignore')

        data = {"text": text}
        source = ""
        s = {"source": source, "type": "t2s", "data": data, "protocol": "firebase"}

        send_json(s)
