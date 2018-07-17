import hashlib
import os
import urllib2
import zipfile
import shutil
import sys

import time

import pkg_resources


from aos.system.configs.channel import FIRMWARE_UPDATE__TMP_PATH, REQUIREMENT_FIRMWARE_PATH, CURRENT_PATH
from aos.system.sdk.python.send import send_json
from aos.system.libs.util import Util
from aos.system.libs.notify import Notify


class Update(object):

    def __init__(self, data, source=None):
        self.data = data
        self.source = source
        self.zip_file = None
        self.link = None
        self.version = None
        self.md5_hash = None

    def run(self):

        try:
            if self.is_valid_system():
                Notify().run(Notify.NotifyType.PLS_WAIT)
                self.send_status('Please Wait for updating your Autonomous device')

                if self.download():
                    print "config md5_value =>", self.md5_hash
                    if self.md5_hash == self.md5(self.zip_file):
                        if self.unzip():
                            print "Unzip Success!"
                            self.send_status('Please Wait for installing package ...')
                            time.sleep(2)
                            if self.install_requirements():
                                return self.update_config_and_reboot()
                            else:
                                print "install_requirements Failed!"
                        else:
                            print "Unzip Failed!"
                else:
                    print "download Failed!"

            else:
                # Neu that bai:
                self.send_status('Cannot update your firmware now. Please try again.')
                print "not is_valid_system"
                if os.path.isdir(FIRMWARE_UPDATE__TMP_PATH):
                    shutil.rmtree(FIRMWARE_UPDATE__TMP_PATH)

        except Exception as e:
            print "error update ....", str(e), sys.exc_info()

        return False

    def is_valid_system(self):

        if self.data and 'link' in self.data and 'version' in self.data and 'md5_hash' in self.data:

            self.link = self.data['link']
            self.version = self.data['version']
            self.md5_hash = self.data['md5_hash']

            self.zip_file = FIRMWARE_UPDATE__TMP_PATH + os.path.basename(self.link)

            return Util.is_valid_system(self.version)
        else:
            return False

    def download(self):
        try:
            print "checking tmp forder ..."
            if os.path.isdir(FIRMWARE_UPDATE__TMP_PATH):
                shutil.rmtree(FIRMWARE_UPDATE__TMP_PATH)

            os.mkdir(FIRMWARE_UPDATE__TMP_PATH)
            print "Created system folder tmp!"

            print 'Downloading system ...'
            print 'Save to %s...' % (self.zip_file)
            request = urllib2.urlopen(self.link)
            file_size = int(request.info().getheaders("Content-Length")[0])

            self.send_status("Downloading: %s Bytes: %s" % (self.link.split('/')[-1], file_size))

            size = 0
            block_sz = 131072

            zip_file = open(self.zip_file, 'wb')

            while True:
                buffer = request.read(block_sz)
                if not buffer:
                    break
                size += len(buffer)
                percentage = float(float(size) / float(file_size)) * 100
                zip_file.write(buffer)

                self.send_status("Downloaded: " + ("%.2f" % percentage) + " %")
                # sys.stdout.flush()

            zip_file.close()

            print "Finished!".ljust(20, ' ')

            return os.path.isfile(self.zip_file)

        except urllib2.HTTPError, e:
            print "HTTP Error:", e.code, self.link
        except urllib2.URLError, e:
            print "URL Error:", e.reason, self.link
        except Exception as e:
            print e.message
            print "error update ....", sys.exc_info()

        return False

    def update_config_and_reboot(self):
        srcfile = FIRMWARE_UPDATE__TMP_PATH + "system/tmp/system.json"

        if os.path.exists(srcfile):
            try:
                dest = CURRENT_PATH + "data/system.json"
                os.remove(dest)
                print 'remove config system successful'
                shutil.copy(srcfile, dest)
                print 'copy config system successful'

                print 'Done! Reboot now ...'
                Notify().run(Notify.NotifyType.REBOOT_NOW)
                self.send_status('Finished! Please Wait for restarting your Autonomous device ...')
                time.sleep(2)

                self.reboot()

                return True

            except Exception as e:
                print e
        return False

    def unzip(self):
        try:
            print 'Extracting system ...'
            if not zipfile.is_zipfile(self.zip_file):
                print "Application zip file is invalid: %s" % self.zip_file
                return False
            with zipfile.ZipFile(self.zip_file, "r") as z:
                print ("extracting to >> ",FIRMWARE_UPDATE__TMP_PATH)
                z.extractall(FIRMWARE_UPDATE__TMP_PATH)
            print "Completed ! and  removing ",self.zip_file, "..."
            os.remove(self.zip_file)
            print ('folder tmp system >> ', FIRMWARE_UPDATE__TMP_PATH + "system")

            return os.path.isdir(FIRMWARE_UPDATE__TMP_PATH + "system")

        except zipfile.BadZipfile:
            print "error unzip ...", os.path.basename(self.zip_file)
        except Exception as e:
            print "error unzip ...", sys.exc_info()
            print e.message

        return False

    def md5(self, filename):
        hash_md5 = hashlib.md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        md5_value = hash_md5.hexdigest()
        print "md5_value", md5_value
        return md5_value

    def install_requirements(self):
        print "installing requirements.txt ..."
        list_reject = ['oauth2client', 'urllib3']
        try:
            if os.path.exists(REQUIREMENT_FIRMWARE_PATH):
                cmd_str = "sudo pip install " + " -r %s" % (REQUIREMENT_FIRMWARE_PATH)
                Util.cmd(cmd_str, True)

                from pkgutil import iter_modules
                modules = set(x[1] for x in iter_modules())

                with open(REQUIREMENT_FIRMWARE_PATH) as file_requirement:
                    for line in file_requirement:
                        requirement = line.rstrip()
                        if requirement in list_reject: continue
                        print "check module => line=> ", requirement
                        if not requirement in modules:
                            print requirement
                            pkg_resources.require(requirement)

                    file_requirement.close()
        except Exception as e:
            print "install requirements.txt False!!!"
            print(str(e))
            print e.message
            return False

        return True

    def send_status(self, message):
        print message
        try:
            data = {"action": "update_firmware_status", "value": message}
            s = {"source": self.source + "_PHONE", "type": "phone_control", "data": data, "protocol": ""}
            send_json(s)
        except:
            pass

    def reboot(self):
        Util.cmd("sudo reboot")