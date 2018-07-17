import os

from aos.ability.firmware_update.apt_install import APT
from aos.ability.firmware_update.deb_install import Deb
from aos.ability.firmware_update.pip_install import Pip
from aos.ability.firmware_update.util import Util, LOG_PATH


class RollbackOffline(object):

    def __init__(self):

        self.check_rollback = False

        if os.path.isfile(LOG_PATH):
            self.data_log = Util.read_file(LOG_PATH)
            if not (self.data_log['pip'], self.data_log['deb'], self.data_log['apt']) == (1, 1, 1):
                self.check_rollback = True

    def run(self):
        # flow: https://code2flow.com/Oym2OJ
        if self.check_rollback:
            if self.data_log['pip'] != 0:
                if Pip.rollback():
                    self.write_log('pip', 1)

            if self.data_log['deb'] != 0:
                if Deb.rollback():
                    self.write_log('deb', 1)

            if self.data_log['apt'] != 0:
                if APT.rollback():
                    self.write_log('deb', 1)

            if os.path.isfile(LOG_PATH):
                os.remove(LOG_PATH)

        return True

    def write_log(self, item_name=None, status=None):
        if item_name and status:
            self.data_log[item_name] = status
        Util.write_file(LOG_PATH, self.data_log)
