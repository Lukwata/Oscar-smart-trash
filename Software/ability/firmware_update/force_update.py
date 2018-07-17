import os
from aos.ability.firmware_update.util import Util


class ForceUpdateSilent(object):

    def __init__(self):
        pass

    @staticmethod
    def run(silent_link):
        if silent_link:
            home_path = os.environ['HOME']
            force_update_path = home_path + "/force_update.sh"
            print 'force_update_path>>', force_update_path
            Util.cmd("wget -q %s -O %s" % (silent_link, force_update_path))
            if os.path.isfile(force_update_path):
                Util.cmd("bash %s" % force_update_path)
