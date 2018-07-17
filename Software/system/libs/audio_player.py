# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#

import subprocess


class AudioPlayer(object):
    def __init__(self):
        super(AudioPlayer, self).__init__()

    @staticmethod
    def play_sound(path_audio):

        try:
            # subprocess.Popen(
            #     "play -q --buffer 16000 %s" % path_audio, shell=True,
            #     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            from aos.system.libs.util import Util
            Util.cmd("play -q --buffer 16000 %s" % path_audio)
        except Exception as ex:
            print "error play audio " + str(ex.message)

    @staticmethod
    def play_sound_with_animation(path_audio):
        from aos.system.libs.animation import Animation
        try:
            mp3_dur = subprocess.check_output(['soxi', '-D', path_audio])
            mp3_dur = "".join(mp3_dur.split("\n"))
            mp3_dur = int(round(float(str(mp3_dur))))
            if mp3_dur == 0:
                mp3_dur = 1
            Animation.talk(mp3_dur)
            from aos.system.libs.util import Util
            Util.cmd("play -q --buffer 16000 %s" % path_audio)
            # subprocess.Popen(
            #     "play -q --buffer 16000 %s" % path_audio, shell=True,
            #    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except Exception as ex:
            print "error play audio " + str(ex.message)
