#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#
import hashlib
import json
import os
import urllib2
import zipfile

import shutil

import time

import sys

from aos.system.configs.channel import BASE_APP, DEVICE_TYPE
from aos.system.libs.notify import Notify
from aos.system.libs.util import Util

TEXT_UPDATE_DESCRIPTION = "Screen will go back for few minute when complete. Do not unplug during this time!"


class InstallUpdateAbility(object):

    def __init__(self, data, source=None):
        self.data = data
        self.source = source

        self.zip_file = None
        self.link = None
        self.version = None
        self.md5_hash = None
        self.is_valid_data = True

        self.app_name = self.data['app'] if 'app' in self.data else None
        self.action = self.data['action'] if 'action' in self.data else None
        self.app_base_dir = (BASE_APP + self.app_name) if self.app_name else None
        self.silent = self.data['silent'] if 'silent' in self.data else False
        self.total_size = self.data['total_size'] if 'total_size' in self.data else False
        self.total_size_downloaded = self.data[
            'total_size_downloaded'] if 'total_size_downloaded' in self.data else False

        if not self.app_name or not self.action:
            self.is_valid_data = False

    def run(self):
        if self.is_valid_data:
            if self.action == 'add':
                return self.add()
            if self.action == 'remove':
                return self.remove()
        else:
            print "not is_valid_data"

    def add(self):
        try:
            if self.is_valid_ability():
                Notify().run(Notify.NotifyType.PLS_WAIT)
                if self.download():
                    print "config md5_value =>", self.md5_hash
                    if self.md5_hash == self.md5(self.zip_file):
                        if self.unzip():
                            print "Unzip Success!"
                            time.sleep(2)
                            if self.install_requirements():
                                # if self.update_config():
                                # self.send_status("The %s app has been updated." % self.app_name)
                                return True
            else:
                print "not is_valid_ability"
        except Exception as e:
            print ("error: ", str(e))

        return False

    def remove(self):
        if os.path.isdir(self.app_base_dir):
            print "Removing app \"%s\" at \"%s\" ..." % (self.app_name, self.app_base_dir)
            shutil.rmtree(self.app_base_dir)
            print "Completed !"

        return not os.path.isdir(self.app_base_dir)

    def download(self):

        status = False
        if not os.path.isdir(self.app_base_dir):
            os.mkdir(self.app_base_dir)
            print "Created app \"%s\" base folder ..." % self.app_name

        try:

            print 'Downloading app >> ...', self.link
            print 'Save to %s...' % self.zip_file
            request = urllib2.urlopen(self.link)
            file_size = int(request.info().getheaders("Content-Length")[0])

            # self.send_status("Downloading: %s Bytes: %s" % (self.link.split('/')[-1], file_size), percentage=0)

            size = 0
            block_sz = 131072

            zip_file = open(self.zip_file, 'wb')

            while True:
                buffer = request.read(block_sz)
                if not buffer:
                    break
                size += len(buffer)
                percentage = float(float(size) / float(file_size)) * 100
                print "percentage of ability ===>", ("%.2f" % percentage)
                if self.total_size is not False and self.total_size_downloaded is not False:
                    percentage = float((float(size) + float(self.total_size_downloaded)) / float(self.total_size)) * 100
                zip_file.write(buffer)

                self.send_status("Downloaded: " + ("%.2f" % percentage) + " %", percentage)
                # sys.stdout.flush()

            zip_file.close()

            print "Finished!".ljust(20, ' ')

            return os.path.isfile(self.zip_file)

        except urllib2.HTTPError as e:
            print "HTTP Error:", e.code, self.link
        except urllib2.URLError as e:
            print "URL Error:", e.reason, self.link
        except Exception as e:
            print str(e)
            print "error update ....", sys.exc_info()

        return status

    def unzip(self):

        try:
            if not zipfile.is_zipfile(self.zip_file):
                print "Application zip file is invalid: %s" % self.zip_file
                return False

            z = zipfile.ZipFile(self.zip_file)
            c = self.app_name.lower() + "/"
            print "Extracting folder \"%s\" to destination folder \"%s\"" % (c, self.app_base_dir)
            for name in z.namelist():
                print name
                if name.lower().find(c) == 0 and name != c:
                    sub = name[len(c):]
                    if name.endswith("/"):
                        new_dir = os.path.join(self.app_base_dir, sub)
                        if not os.path.exists(new_dir):
                            os.mkdir(new_dir)
                        continue
                    source = z.open(name)
                    target = file(os.path.join(self.app_base_dir, sub), "wb")
                    with source, target:
                        shutil.copyfileobj(source, target)

            print "removing zip...."
            os.unlink(self.zip_file)
            z.close()

            return True

        except zipfile.BadZipfile:
            print "error: bad zip file"
        except Exception as e:
            print "error: ", str(e)
        return False

    def is_valid_ability(self):

        if self.data and 'link' in self.data and 'is_service' in self.data and 'application_file' in self.data and 'version' in self.data and 'md5_hash' in self.data:

            self.link = self.data['link']
            self.md5_hash = self.data['md5_hash']
            self.zip_file = self.app_base_dir + "/" + os.path.basename(self.link)

            self.version = self.data['version']

            app_config = Util.read_file(self.app_base_dir + "/config.json")

            if app_config:
                try:
                    return Util.convert_version(self.version) > Util.convert_version(app_config['version'])
                except Exception as e:
                    print e.message

            else:
                return True

        print "not_is_valid_ability"
        return False

    def install_requirements(self):

        print('installing requirement.txt ...')
        try:
            requirement_file = self.app_base_dir + "/requirements.txt"
            if os.path.exists(requirement_file):
                cmd_str = "sudo pip install  -r %s" % requirement_file
                Util.cmd(cmd_str, True)

                import pkg_resources
                from pkgutil import iter_modules
                modules = set(x[1] for x in iter_modules())
                print "modules=>", modules
                with open(requirement_file) as file_requirement:
                    for line in file_requirement:
                        requirement = line.rstrip()
                        print "check module => line=> ", requirement
                        if requirement not in modules:
                            print requirement
                            pkg_resources.require(requirement)

                    file_requirement.close()
        except Exception as e:
            print "install requirements.txt False!!!"
            print(str(e))
            print e.message
            return False

        return True

    def update_config(self):
        app_path_config = BASE_APP + self.app_name + "/config.json"
        # if not os.path.isfile(app_path_config):
        print ("creating config app " + app_path_config + "...")
        boot = self.data['boot'] if 'boot' in self.data else False
        if self.data['is_service'] == 1:
            boot = True
        sensor = self.data['sensor'] if 'sensor' in self.data else self.app_name
        config_data = {"application_file": self.data['application_file'],
                       'is_service': self.data['is_service'],
                       'name': self.app_name,
                       'version': self.data['version'], "type": 0, "boot": boot, "sensor": sensor}

        with open(app_path_config, 'w') as outfile:
            json.dump(config_data, outfile)
        return os.path.isfile(app_path_config)

    def md5(self, filename):
        hash_md5 = hashlib.md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        md5_value = hash_md5.hexdigest()
        print "md5_value", md5_value
        return md5_value

    def send_status(self, message, percentage=-1):
        print message

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
                    data = {"action": "install_ability_device_status", "value": message}
                    s = {"source": self.source, "type": "phone_control", "data": data, "protocol": ""}
                    send_json(s)
            except Exception as e:
                print str(e)
