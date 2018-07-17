import json
import os
import subprocess

from aos.system.configs.channel import CURRENT_PATH, HOME_PATH, DEVICE_TYPE, BASE_APP

FOLDER_PIP_INSTALL = HOME_PATH + "/aos_packages/pip/wheels"
FOLDER_DEB_TMP = HOME_PATH + "/aos_packages/debs/"

LOG_PATH = CURRENT_PATH + "log.json"
PIP_REQUIREMENT_FILE = "system/"+DEVICE_TYPE+"/requirements/pip.txt"
APT_REQUIREMENT_FILE = "system/"+DEVICE_TYPE+"/requirements/apt.txt"
DEB_REQUIREMENT_FILE = "system/"+DEVICE_TYPE+"/requirements/deb.txt"

CMD_GET_VERSION = '/usr/local/bin/get_version_pkg'


class Util(object):

    @staticmethod
    def before_setup():
        try:
            print "check has get_version cmd..."
            if not os.path.isfile(CMD_GET_VERSION):
                print "create get_version cmd..."
                Util.cmd("sudo cp %s %s && sudo chmod +x %s" % (
                    BASE_APP + "firmware_update/get_version_pkg", CMD_GET_VERSION, CMD_GET_VERSION))
                if not os.path.isfile(CMD_GET_VERSION):
                    print "can't create get_version cmd"
            print "check and create FOLDER_PIP_INSTALL..."
            if not os.path.exists(FOLDER_PIP_INSTALL):
                Util.cmd("mkdir -p %s" % FOLDER_PIP_INSTALL)
            print "check and create FOLDER_DEB_TMP..."
            if not os.path.exists(FOLDER_DEB_TMP):
                Util.cmd("mkdir -p %s" % FOLDER_DEB_TMP)

        except Exception as ex:
            print str(ex)
        print "check and install pip wheel ..."
        Util.cmd("pip install wheel")
        return os.path.isfile(CMD_GET_VERSION) and os.path.exists(FOLDER_PIP_INSTALL) and os.path.exists(FOLDER_DEB_TMP)

    @staticmethod
    def cmd(cmd, output=True):
        # print "cmd >> ", cmd
        if output:
            return subprocess.Popen(
                cmd, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read()
        else:
            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Doc file json:

    @staticmethod
    def read_file(path):
        try:
            with open(path) as data_file:
                return json.load(data_file)
        except:
            pass
        return None

    # Ghi file json
    @staticmethod
    def write_file(path, content):
        try:
            with open(path, 'w') as outfile:
                json.dump(content, outfile)
        except:
            pass
            print "Cannot open file"