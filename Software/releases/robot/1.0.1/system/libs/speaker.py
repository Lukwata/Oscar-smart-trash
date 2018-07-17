#phuong macbook
from aos.system.libs.util import Util
import os
package = "aos.system." + os.environ['DEVICE_TYPE'] + ".util"
list_name = ["get_speaker_hwindex", "get_speaker_name"]

get_speaker_hwindex = getattr(__import__(package, fromlist=list_name), 'get_speaker_hwindex')
get_speaker_name = getattr(__import__(package, fromlist=list_name), 'get_speaker_name')

hwindex = get_speaker_hwindex()
speaker_name = get_speaker_name()


class VolumeControl:

    PERCENT_STEP = 10
    VOLUME_MAX = 100
    VOLUME_MIN = 1

    def __init__(self):
        super(VolumeControl, self).__init__()

    @staticmethod
    def set_volume_percent(percent):
        try:
            percent = int(str(percent))
        except Exception as ex:
            percent = None
            print str(ex)
        if percent:
            command = "amixer --quiet -c {} set {} {}%".format(hwindex, speaker_name, percent)
            Util.cmd(command)

    @staticmethod
    def set_volume_up():
        volume = VolumeControl.get_volume()
        volume += VolumeControl.PERCENT_STEP
        VolumeControl.set_volume_percent(volume)

    @staticmethod
    def set_volume_down():
        volume = VolumeControl.get_volume()
        volume -= VolumeControl.PERCENT_STEP
        VolumeControl.set_volume_percent(volume)

    @staticmethod
    def set_volume_max():
        VolumeControl.set_volume_percent(VolumeControl.VOLUME_MAX)

    @staticmethod
    def set_volume_min():
        VolumeControl.set_volume_percent(VolumeControl.VOLUME_MIN)

    @staticmethod
    def get_volume():
        percent = 100
        try:
            command = 'amixer -c {} get {} | egrep -o "[0-9]+%" | head -n1 | grep -o "[0-9]*"'.format(hwindex, speaker_name)
            percent = int(Util.cmd(command))
        except Exception as ex:
            print str(ex)
        return percent

