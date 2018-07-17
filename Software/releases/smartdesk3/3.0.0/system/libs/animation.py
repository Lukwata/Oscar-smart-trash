#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#

import os

import zmq

from aos.ability.animation.UI.actions import ACTIONS
from aos.ability.animation.UI.config import INTERVAL_6


class Animation:

    def __init__(self):
        super(Animation, self).__init__()

    @staticmethod
    def talk(second):
        if(second):
            Animation.runAction(ACTIONS.TALK, second)

    @staticmethod
    def smile():
        Animation.runAction(ACTIONS.SMILE)

    @staticmethod
    def sad():
        Animation.runAction(ACTIONS.SAD)

    @staticmethod
    def thinking():
        Animation.runAction(ACTIONS.THINKING)

    @staticmethod
    def listen():
        Animation.runAction(ACTIONS.LISTEN)

    @staticmethod
    def blink():
        Animation.runAction(ACTIONS.BLINK)

    @staticmethod
    def happy():
        Animation.runAction(ACTIONS.HAPPY)

    # @staticmethod
    # def crying():
    #     Animation.runAction(ACTIONS.CRYING)

    @staticmethod
    def normal():
        Animation.runAction(ACTIONS.NORMAL)

    @staticmethod
    def shake():
        Animation.runAction(ACTIONS.SHAKE)

    @staticmethod
    def show_card(title="", description="", photo=None, second=INTERVAL_6):
        if not title and not description and not photo:
            raise NameError('param is empty')
        elif photo and not os.path.isfile(photo):
            raise NameError('photo is not exists')
        else:
            Animation.runAction(ACTIONS.SHOW_CARD, (title, description, photo, second))

    @staticmethod
    def hide_card():
        Animation.runAction(ACTIONS.HIDE_CARD)

    @staticmethod
    def runAction(action, value=None):
        context = zmq.Context()
        mainSocket = context.socket(zmq.PUSH)
        mainSocket.connect("ipc:///tmp/animation.ipc")
        package = {'action': action, 'value': value}
        mainSocket.send_json(package)
