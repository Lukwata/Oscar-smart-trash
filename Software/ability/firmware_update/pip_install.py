import os

from aos.ability.firmware_update.util import Util, PIP_REQUIREMENT_FILE, FOLDER_PIP_INSTALL
from aos.system.configs.channel import FIRMWARE_UPDATE__TMP_PATH, CURRENT_PATH

REQUIREMENT_FIRMWARE_PATH_UPDATE = FIRMWARE_UPDATE__TMP_PATH + PIP_REQUIREMENT_FILE
REQUIREMENT_FIRMWARE_PATH_ROLLBACK = CURRENT_PATH + PIP_REQUIREMENT_FILE

CMD_STORE = "sudo pip wheel --find-links %s --wheel-dir=%s -r %s"
CMD_INSTALL = "sudo pip install --no-index --find-links=%s -r %s"


class Pip(object):

    # check need run install:
    @staticmethod
    def check_is_new_requirement():
        try:
            if os.path.exists(REQUIREMENT_FIRMWARE_PATH_ROLLBACK) and os.path.exists(REQUIREMENT_FIRMWARE_PATH_UPDATE):
                import filecmp
                return not filecmp.cmp(REQUIREMENT_FIRMWARE_PATH_ROLLBACK, REQUIREMENT_FIRMWARE_PATH_UPDATE)
        except Exception as e:
            print str(e)

        return True

    @staticmethod
    def update():
        if os.path.exists(REQUIREMENT_FIRMWARE_PATH_UPDATE):
            cmd = CMD_STORE % (FOLDER_PIP_INSTALL, FOLDER_PIP_INSTALL, REQUIREMENT_FIRMWARE_PATH_UPDATE) + " && " +\
            CMD_INSTALL % (FOLDER_PIP_INSTALL, REQUIREMENT_FIRMWARE_PATH_UPDATE)
            return Pip.install(cmd, REQUIREMENT_FIRMWARE_PATH_UPDATE)
        return True

    @staticmethod
    def rollback():
        print "Rollback pip"
        if os.path.exists(REQUIREMENT_FIRMWARE_PATH_ROLLBACK):
            cmd = CMD_INSTALL % (FOLDER_PIP_INSTALL, REQUIREMENT_FIRMWARE_PATH_ROLLBACK)
            return Pip.install(cmd, REQUIREMENT_FIRMWARE_PATH_ROLLBACK)
        return True

    @staticmethod
    def install(cmd, req_path):
        print "installing new requirements.txt ..."

        try:
            if os.path.exists(req_path):

                print "install pip -> ", cmd
                Util.cmd(cmd, True)

                import pkg_resources
                from pkgutil import iter_modules
                modules = set(x[1] for x in iter_modules())
                print "modules ==>", modules
                with open(req_path) as file_requirement:
                    for line in file_requirement:
                        requirement = line.rstrip()

                        print "check module => line=> ", requirement
                        if requirement not in modules:
                            print requirement
                            pkg_resources.require(requirement)

                    file_requirement.close()

            return True

        except Exception as e:
            print "install requirements.txt False!!!"
            print(str(e))
            print e.message

        return False
