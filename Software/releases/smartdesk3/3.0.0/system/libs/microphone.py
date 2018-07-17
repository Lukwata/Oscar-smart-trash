#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#

#phuong macbook
from aos.system.libs.util import Util


class Microphone:

    def __init__(self):
        super(Microphone, self).__init__()

    @staticmethod
    def mute():
        try:
            Util.cmd('amixer -D pulse sset Capture 0%')
        except:
            pass

    @staticmethod
    def unmute():
        try:
            Util.cmd('amixer -D pulse sset Capture 40%')
        except:
            pass

    @staticmethod
    def auto_check_mic():
        #Todo: auto set mic
        print "auto set mic"
        # try:
        #     if get_mic() == 0:
        #         print "Mic -> mute"
        #         Microphone.mute()
        #     else:
        #         print "Mic -> unmute"
        #         Microphone.unmute()
        # except:
        #     pass
