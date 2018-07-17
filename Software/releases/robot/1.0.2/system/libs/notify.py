# -*- coding: utf-8 -*-
import ConfigParser
import io
from aos.system.configs.channel import CURRENT_PATH, DEVICE_TYPE
from aos.system.libs.audio_player import AudioPlayer

package = "aos.system." + DEVICE_TYPE + ".util"
name = "play_sound"
play_sound = getattr(__import__(package, fromlist=[name]), name)


class Notify(object):

    def __init__(self):
        super(Notify, self).__init__()
        self.audio_player = AudioPlayer()
        self.read_config()

    def read_config(self):
        with open(CURRENT_PATH + "system/file_config.ini") as f:
            sample_config = f.read()
        self.config = ConfigParser.RawConfigParser(allow_no_value=True)
        self.config.readfp(io.BytesIO(sample_config))

    class NotifyType():
        IN_SETUP_MODE = 'now_in_setup_mode'
        WIFI_CONNETED = 'file_wifi_connected'
        CANNOT_CONNECT_WIFI_TRY_AGAIN = 'cant_connect_to_please_try_again'
        DEVICE_READY_TO_USE = 'your_smart_desk_is_ready_to_use'
        WIFI_ISNOT_SETUP = 'wifi_isnt_setup'
        DEVICE_CONNECTED_TO_HOTSPOT = 'you_are_connected_hotspot_finish_the_setup'
        PLS_WAIT = 'please_wait'
        REBOOT_NOW = 'system_reboot'
        CONTROL_BOX_NOT_RESPONSE = 'control_box_not_responding'
        LISTEN = 'listen'
        SAYCHEESE = 'say_cheese'
        WARNING = 'warning'

    def run(self, notify_type):
        try:
            print "notify_type>>", notify_type
            file = CURRENT_PATH + "system/files/sound_speak/" + self.config.get(DEVICE_TYPE, notify_type)
            print "playing file >> ", file
            play_sound(file)
            return True
        except Exception as e:
            print ("notify config not found =>" + str(e))
        return False
