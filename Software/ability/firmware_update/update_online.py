#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
from __future__ import print_function
import hashlib
import os
import urllib2
import zipfile
import shutil
import sys

import time

from aos.ability.firmware_update.force_update import ForceUpdateSilent
from aos.ability.firmware_update.rollbak_offline import RollbackOffline
from aos.ability.firmware_update.util import LOG_PATH, Util as Util_Update
from apt_install import APT
from deb_install import Deb
from pip_install import Pip
from aos.system.configs.channel import FIRMWARE_UPDATE__TMP_PATH, CURRENT_PATH, DEVICE_TYPE
from aos.system.libs.util import Util
from aos.system.libs.notify import Notify

TEXT_UPDATE_DESCRIPTION = "Screen will go back for few minute when complete. Do not unplug during this time!"


class UpdateOnline(object):
    def __init__(self, data, source=None):
        self.data = data
        self.source = source
        self.zip_file = None
        self.link = None
        self.version = None
        self.md5_hash = None
        self.log_data = {"pip": 0, "deb": 0, "apt": 0}
        self.error_message = None
        self.silent = self.data['silent'] if 'silent' in self.data else False
        self.total_size = self.data['total_size'] if 'total_size' in self.data else False
        self.total_size_downloaded = self.data[
            'total_size_downloaded'] if 'total_size_downloaded' in self.data else False

    def force_update(self):
        print("is_force_update ...")
        try:
            ForceUpdateSilent.run(self.data['silent_link'])
        except Exception as e:
            print("error force update >> ", str(e))
            return False
        return True

    def run(self):
        # flow: https://code2flow.com/ty9ZIG
        try:
            self.error_message = None

            if self.is_force_update():
                return self.force_update()

            elif self.is_valid_system():
                Notify().run(Notify.NotifyType.PLS_WAIT)
                # self.send_status('Please Wait for updating your system ...', 5)

                if self.download():
                    print("config md5_value =>", self.md5_hash)
                    if self.md5_hash == self.md5(self.zip_file):
                        if self.unzip():
                            print("Unzip Success!")
                            # self.send_status('Please Wait for installing packages ...')
                            time.sleep(2)

                            if self.install_all_package():
                                # self.send_status("Update successful, please wait for rebooting ...")
                                self.remove_log()
                                self.update_config_and_reboot()
                                return True
                            else:
                                print("rollback now...")
                                RollbackOffline().run()
                        else:
                            print( "Unzip Failed!")
                else:
                    print("download Failed!")

        except Exception as e:
            print("error update ....", str(e), sys.exc_info())

        # Neu that bai:
        if self.error_message:
            self.send_status(self.error_message)
        else:
            self.send_status('Cannot update your firmware now. Please try again.')

        if os.path.exists(FIRMWARE_UPDATE__TMP_PATH):
            shutil.rmtree(FIRMWARE_UPDATE__TMP_PATH)

        return False

    def install_all_package(self):
        # flow: https://code2flow.com/h1ZCJS
        # 1. install pip
        if Pip.check_is_new_requirement():
            self.write_log('pip', 2)
            if Pip.update():
                self.write_log('pip', 1)
                self.send_status('Update pip package successful.')
            else:
                self.write_log('pip', 0)
                self.send_status('Update pip package failed.')
                return False

        # 2. install deb
        if Deb.check_is_new_requirement():
            self.write_log('deb', 2)
            if Deb.update():
                self.write_log('deb', 1)
                self.send_status('Update debian package successful.')
            else:
                self.write_log('deb', 0)
                self.send_status('Update debian package failed.')
                return False

        # 3. install apt:
        if APT.check_is_new_requirement():
            self.write_log('apt', 2)
            if APT.update():
                self.write_log('apt', 1)
                self.send_status('Update apt package successful.')
            else:
                self.write_log('apt', 0)
                self.send_status('Update apt package failed.')
                return False

        return True

    def is_valid_system(self):

        if self.data and 'link' in self.data and 'version' in self.data and 'md5_hash' in self.data:

            self.link = self.data['link']
            self.version = self.data['version']
            self.md5_hash = self.data['md5_hash']

            self.zip_file = FIRMWARE_UPDATE__TMP_PATH + os.path.basename(self.link)

            if not Util_Update.before_setup():
                self.error_message = 'Can not create temporary folders.'
                return False

            try:
                current_version = Util.get_version(CURRENT_PATH)
                if current_version > 0:
                    if current_version < Util.convert_version(self.version):
                        return True
                    elif current_version == Util.convert_version(self.version):
                        self.error_message = 'This firmware version is already installed.'
                    else:
                        self.error_message = 'This firmware version is too old.'
            except Exception as e:
                print( str(e))
                return True

            return False

    def download(self):
        try:
            print ("checking tmp forder ...")
            if os.path.isdir(FIRMWARE_UPDATE__TMP_PATH):
                shutil.rmtree(FIRMWARE_UPDATE__TMP_PATH)

            os.mkdir(FIRMWARE_UPDATE__TMP_PATH)
            print ("Created system folder tmp!")

            print('Downloading system ...')
            print('Save to %s...' % self.zip_file)
            request = urllib2.urlopen(self.link)
            file_size = int(request.info().getheaders("Content-Length")[0])

            # self.send_status("Downloading: %s Bytes: %s" % (self.link.split('/')[-1], file_size), 5)

            size = 0
            block_sz = 131072

            zip_file = open(self.zip_file, 'wb')

            while True:
                buffer = request.read(block_sz)
                if not buffer:
                    break
                size += len(buffer)
                percentage = float(float(size) / float(file_size)) * 100
                if self.total_size is not False and self.total_size_downloaded is not False:
                    percentage = float((float(size) + float(self.total_size_downloaded)) / float(self.total_size)) * 100
                zip_file.write(buffer)

                self.send_status("Downloaded: " + ("%.2f" % percentage) + " %", percentage)

                # sys.stdout.flush()

            zip_file.close()

            print ("Finished!".ljust(20, ' '))

            return os.path.isfile(self.zip_file)

        except urllib2.HTTPError as e:
            print("HTTP Error:", e.code, self.link)
        except urllib2.URLError as e:
            print ("URL Error:", e.reason, self.link)
        except Exception as e:
            print (e.message)
            print ("error update ....", sys.exc_info())

        self.error_message = 'An error occurred during the download process. ' + str(e)

        return False

    def update_config_and_reboot(self):
        srcfile = FIRMWARE_UPDATE__TMP_PATH + "system/tmp/system.json"

        if os.path.exists(srcfile):
            try:
                dest = CURRENT_PATH + "data/system.json"
                os.remove(dest)
                print ('remove config system successful')
                shutil.copy(srcfile, dest)
                print ('copy config system successful')

                print ('Done! Reboot now ...')
                Notify().run(Notify.NotifyType.REBOOT_NOW)
                self.send_status('Finished! Please Wait for restarting your Autonomous device ...')
                time.sleep(2)

                self.reboot()

                return True

            except Exception as e:
                self.error_message = 'Config fail. ' + str(e)
                print (str(e))
        return False

    def unzip(self):
        try:
            print ('Extracting system ...')
            if not zipfile.is_zipfile(self.zip_file):
                print ("Application zip file is invalid: %s" % self.zip_file)
                return False
            with zipfile.ZipFile(self.zip_file, "r") as z:
                print ("extracting to >> ", FIRMWARE_UPDATE__TMP_PATH)
                z.extractall(FIRMWARE_UPDATE__TMP_PATH)
            print("Completed ! and  removing ", self.zip_file, "...")
            os.remove(self.zip_file)
            print ('folder tmp system >> ', FIRMWARE_UPDATE__TMP_PATH + "system")
            if os.path.isdir(FIRMWARE_UPDATE__TMP_PATH + "system"):
                return True
        except zipfile.BadZipfile:
            print ("error unzip ...", os.path.basename(self.zip_file))
        except Exception as e:
            print("error unzip ...", sys.exc_info())
            print (str(e))
            self.error_message = 'Unzip fail. ' + str(e)

        return False

    def md5(self, filename):
        hash_md5 = hashlib.md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        md5_value = hash_md5.hexdigest()
        print ("md5_value", md5_value)
        return md5_value

    def send_status(self, message, percentage=-1):
        print (message)

        if self.silent is False:
            from aos.system.sdk.python.send import send_json
            try:
                if DEVICE_TYPE == "SMART_DESK_3":
                    if percentage > -1:
                        data = {"action": "add", "from": "product_control",
                                "data": {"status": 1, "message": "", "data": {
                                    "title": "Updating OS...",
                                    "desc": str("%.0f" % percentage) + '%',
                                    "progress": percentage}}}
                        s = {"source": self.source, "type": "waiting_update", "data": data, "protocol": ""}

                        send_json(s)
                else:
                    data = {"action": "update_firmware_status", "value": message}
                    s = {"source": self.source, "type": "phone_control", "data": data, "protocol": "firebase"}
                    send_json(s)
            except Exception as e:
                print (str(e))

    def is_force_update(self):
        if 'force_update' in self.data and 'silent_link' in self.data and \
                        self.data['force_update'] == 1 and self.data['silent_link']:
            return True
        return False

    def write_log(self, item_name=None, status=None):
        if item_name and status:
            self.log_data[item_name] = status
        Util.write_file(LOG_PATH, self.log_data)

    def remove_log(self):
        if os.path.isfile(LOG_PATH):
            os.remove(LOG_PATH)

    def reboot(self):
        Util.cmd("sudo reboot")
