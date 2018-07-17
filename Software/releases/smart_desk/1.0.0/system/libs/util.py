# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#

#phuong macbook:

import os
import socket
import subprocess
import json
import datetime
import sys
import pytz
import signal
import netifaces
from time import sleep

import unicodedata

from aos.system.configs.channel import CURRENT_PATH, DEVICE_TYPE, BRAIN_CONFIG_PATH, PATH_WIFI_CONFIG, \
    PATH_PRODUCT_ID_CONFIG, PATH_USER_CONFIG
from aos.system.libs.notify import Notify

package = "aos.system." + DEVICE_TYPE + ".util"
name = "get_speaker_hwindex"
get_speaker_hwindex = getattr(__import__(package, fromlist=[name]), name)


class Util(object):

    def __init__(self):
        super(Util, self).__init__()

    @staticmethod
    def get_current_path_app():
        return CURRENT_PATH

    @staticmethod
    def cmd(cmd, output=True):
        if output:
            return subprocess.Popen(
                cmd, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read()
        else:
            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    #Doc file json:
    @staticmethod
    def read_file(path):
        try:
            with open(path) as data_file:
                return json.load(data_file)
        except:
            pass
        return None

    #Ghi file json
    @staticmethod
    def write_file(path, content):
        try:
            with open(path, 'w') as outfile:
                json.dump(content, outfile)
        except:
            pass
            print "Cannot open file"


    #Lay version hien tai cua system:
    @staticmethod
    def get_version_info():
        result = Util.read_file(CURRENT_PATH + "data/system.json")
        return result

    @staticmethod
    def check_version():
        result = Util.read_file(CURRENT_PATH + "data/system.json")
        if result is not None:
            return result['version']
        return ""

    #Lay prodcut_id
    @staticmethod
    def get_product_id():

        product_id = ''
        result = Util.read_file(PATH_PRODUCT_ID_CONFIG)
        if result is not None:
            product_id = result['product_id']

        return product_id

    @staticmethod
    def get_product_config():
        return Util.read_file(PATH_WIFI_CONFIG)

    #Lay thong tin mic (co mute hay ko):
    @staticmethod
    def get_mic():
        mute = 1
        try:
            user_info = Util.read_file(PATH_USER_CONFIG)

            if user_info is not None:
                data = json.loads(user_info['product']['data'])
                mute = int(data['microphone'])
                print mute
        except IOError as e:
            print e.message
            pass
        except:
            pass
        return mute

    @staticmethod
    def get_user_data():
        try:
            user_info = Util.read_file(PATH_USER_CONFIG)

            if user_info is not None:
                data = json.loads(user_info['product']['data'])
                return data
        except IOError as e:
            print e.message
            pass
        except Exception as e:
            print e.message
            pass
        return None

    @staticmethod
    def get_product():
        product = None
        try:
            result = Util.read_file(PATH_USER_CONFIG)
            if result is not None:
                product = result['product']
        except:
            pass

        return product

    #Lay thong tin user_hash:
    @staticmethod
    def get_user_hash():
        user_hash = ''
        result = Util.read_file(PATH_WIFI_CONFIG)
        if result is not None:
            user_hash = result['user_hash']

        return user_hash


    #Lay thong tin user_id:
    @staticmethod
    def get_user_id():
        user_id = -1
        result = Util.read_file(PATH_WIFI_CONFIG)
        if result is not None:
            user_id = result['user_id']
        return user_id

    #Kiem tra co internet:
    @staticmethod
    def internet_connected():
        REMOTE_SERVER = "www.google.com"
        try:
            host = socket.gethostbyname(REMOTE_SERVER)
            s = socket.create_connection((host, 80), 2)
            return True
        except:
            pass
        return False

    @staticmethod
    def internet_on():
        for timeout in [1, 5, 10, 15]:
            try:
                IPS = ['unknown', '192.168.42.1']
                ip = Util.get_ip_address()
                if ip not in IPS:
                    import urllib2
                    urllib2.urlopen('http://google.com', timeout=timeout)
                    print "internet => OK"
                    return True
            except urllib2.URLError as err:
                print "No internet connection!"
                pass
        return False

    @staticmethod
    def check_internet_connection(steps = 5, sleeps = 2):
        for j in range(0, steps):
            sleep(sleeps)
            if Util.internet_on():
                return True
        return False

    # convert 24h <-> 12h ---------------------------
    @staticmethod
    def to12(hour24):
        return (hour24 % 12) if (hour24 % 12) > 0 else 12

    @staticmethod
    def IsPM(hour24):
        return hour24 > 11

    @staticmethod
    def to24(hour12, isPm):
        return (hour12 % 12) + (12 if isPm else 0)

    @staticmethod
    def IsPmString(pm):
        return "p.m" if pm else "a.m"

    @staticmethod
    def TestTo12():
        for x in range(24):
            print x, Util.to12(x), Util.IsPmString(Util.IsPM(x))

    @staticmethod
    def wifi_update():
        try:
            if os.path.isfile(PATH_WIFI_CONFIG):
                os.unlink(PATH_WIFI_CONFIG)
                print "removed os_config"
                sleep(1)
        except:
            print "error remove config..."

        try:
            #todo: Notify ...
            print "reboot now ..."
            sleep(2)
        except:
            print "error play_sound"

        os.system('sudo reboot now')

    @staticmethod
    def factory_reset():

        import shutil
        try:
            if os.path.isfile(PATH_WIFI_CONFIG):
                os.unlink(PATH_WIFI_CONFIG)
                print "removed os_config"
                sleep(2)
        except:
            pass
            print "not found os_config ..."

        try:
            if os.path.isfile(BRAIN_CONFIG_PATH):
                pr_device_data = Util.read_file(BRAIN_CONFIG_PATH)
                pr_device_data['firebase_uid'] = ''
                Util.write_file(BRAIN_CONFIG_PATH, pr_device_data)
                print "update pr_device.json"
                sleep(2)
        except:
            print "error update pr_device ..."

        try:

            if os.path.isfile(PATH_USER_CONFIG):
                os.unlink(PATH_USER_CONFIG)
                print "removed user_config"
        except:
            print "error remove user config..."

        try:
            config_training = CURRENT_PATH + "data/training"
            if os.path.isdir(config_training):
                shutil.rmtree(config_training)
                print "removed data trainning"
        except:
            print "error remove trainning ..."

        try:
            config_recipe = CURRENT_PATH + "data/recipe"
            if os.path.isdir(config_recipe):
                shutil.rmtree(config_recipe)
                print "removed data recipe"
        except:

            print "error remove recipe ..."

        try:
            config_reminder = CURRENT_PATH + "data/reminder"
            if os.path.isdir(config_reminder):
                shutil.rmtree(config_reminder)
                print "removed data reminder"
        except:
            print "error remove reminder ..."

        try:
            config_activity = CURRENT_PATH + "data/activity"
            if os.path.isdir(config_activity):
                shutil.rmtree(config_activity)
                print "removed data activity"
        except:
            print "error remove activity ..."

        try:
            #Todo: Notidy hehe...
            print "reboot now ..."
            sleep(2)
        except:
            print "error play_sound"

        os.system('sudo reboot now')

    @staticmethod
    def kill_app_by_name(name):
        try:
            list_pid = Util.cmd("pidof %s" % str(name))
            if list_pid != "":
                list_pid = list_pid.split()
                for pid in list_pid:
                    print "kill pid " + str(pid) + "by name" +name + " ...\n"
                    os.kill(int(pid), signal.SIGTERM)
                return True
        except:
            pass
        return False

    @staticmethod
    def get_mac_address():
        try:
            # Read MAC from file
            myMAC = open('/sys/class/net/wlan0/address').read()
            # Echo to screen
            return str(myMAC).rstrip()
        except:
            pass
        return None

    @staticmethod
    def get_ip_address():
        try:
            ip = netifaces.ifaddresses("wlan0")[netifaces.AF_INET][0]['addr']
            if ip is not None:
                return ip

        except Exception as ex:
            print "Cannot get address of wlan0 --> " + str(ex)
        return "unknown"

    @staticmethod
    def is_clone_sdcard():
        print "checking board ..."
        try:
            file_name = "used.dll"
            mac_address = Util.get_mac_address()
            print "mac_address:",mac_address
            if mac_address is not None:
                path = CURRENT_PATH + "logs/" + file_name
                print "path:", path
                if os.path.isfile(path):
                    content = Util.read_file(path)
                    if content:
                        mac_address_saved = content['mac_adderss']
                        if mac_address != mac_address_saved:
                            Notify().run(Notify.NotifyType.WARNING)
                            return False
                        else:
                            return True
                else:
                    Util.write_file(path, {"mac_adderss": mac_address})

        except:
            pass
            print "except is_clone_sdcard..."
        return True

    #Lay timezone name tu config:
    @staticmethod
    def get_time_zone():
        time_zone = "America/New_York"
        result = Util.read_file(PATH_WIFI_CONFIG)
        if result is not None:
            time_zone = result['time_zone']
        return time_zone

    #Set ngay gio he thong tu config #time_zone
    @staticmethod
    def get_time_system():
        time_zone = Util.get_time_zone()
        tz = pytz.timezone(time_zone)
        return datetime.datetime.now(tz)

    #set datetime for system:
    @staticmethod
    def set_date_time():
        try:
            #list commmad:
            Util.cmd('sudo rm /etc/localtime')
            Util.cmd("sudo ln -s /usr/share/zoneinfo/%s /etc/localtime" % Util.get_time_zone())
            Util.cmd('sudo ntpdate time.nist.gov')
        except:
            pass


    @staticmethod
    def validate_app_config(config):
        config_keys = ["application_file", "version", "type", "app"]
        if set(config_keys).issubset(set(config.keys())):
            return True
        return False

    @staticmethod
    def read_app_config(path):
        if os.path.isdir(path):
            path += "/config.json"
        if os.path.isfile(path):
            f = open(path, "r")
            data = f.read()
            f.close()
            data = json.loads(data.strip())
            if Util.validate_app_config(data):
                return data
        return None

    @staticmethod
    def get_speaker_hwindex():
        return get_speaker_hwindex()

    @staticmethod
    def get_version(path):
        try:
            result = Util.read_file(path + "data/system.json")
            if result is not None:
                return Util.convert_version(result['version'])
        except Exception as e:
            print(e.message)
            pass
        return 0

    @staticmethod
    def convert_version(string_version):
        try:
            list_num = string_version.split('.')
            version_num = ""
            for num in list_num:
                version_num += num
            if version_num:
                return int(version_num)
        except Exception as e:
            print(e.message)
            pass

        return 0

    @staticmethod
    def is_valid_system(new_version):
        curent_version = Util.get_version(CURRENT_PATH)
        if curent_version > 0:
            try:
                if curent_version < Util.convert_version(new_version):
                    result = True
                else:
                    result = False
            except Exception as e:
                pass
                print
                e.message
                result = False
            except:
                print
                "error check invald app", sys.exc_info()
                pass
        else:
            result = True

        return result

    @staticmethod
    def has_s2t_feature():
        s2t_ability_path = os.environ['HOME'] + "/aos/ability/s2t"
        if os.path.isdir(s2t_ability_path) is False:
            print 'S2T --> NO'
            return False
        else:
            print 'S2T --> YES'
            return True

    @staticmethod
    def gen_id():
        s = ""
        try:
            import random
            ALPHABET = "0123456789BCDFGHJKLMNPQRSTVWXYZ"
            for i in range(0, 3):
                s += ALPHABET[random.randrange(i, len(ALPHABET), 3)]
        except:
            pass
        return s

    @staticmethod
    def check_match_current_user(user_id):
        if os.path.isfile(PATH_PRODUCT_ID_CONFIG):
            data = Util.read_file(PATH_PRODUCT_ID_CONFIG)
            if data and 'product_id' in data and 'user_id' in data and data['user_id'] == user_id:
                return data['product_id']
        return ''

    @staticmethod
    def check_invalid_data(data_string):
        key_array = ['source', 'verify_code', 'address_long', 'address_lat', 'time_zone', 'user_id', 'wpa', 'ssid', 'user_hash', 'product_name', 'product_type', 'token']
        result = Util.Result()
        try:
            data_info = json.loads(data_string)
            if 'action' in data_info and data_info['action'] == "hotpost_connected":
                return Util.Result(status=True, message=data_info)
            for key in key_array:
                if key not in data_info:
                    return Util.Result(status=False, message='key `%s` is required.' % key)

            return Util.Result(status=True, message=data_info)

        except Exception as e:
            result.status = False
            result.message = "Unexpected error in check_invalid_data:", str(e)

        return result

    @staticmethod
    def update_pr_device_id(product_id, firebase_uid):
        json_data = Util.read_file(BRAIN_CONFIG_PATH)
        if json_data and product_id:
            json_data["id"] = product_id
            json_data["firebase_uid"] = firebase_uid
            Util.write_file(BRAIN_CONFIG_PATH, json_data)


    # xoa het cache truoc do cac device da connect toi:
    @staticmethod
    def clear_cache_arp():
        subprocess.Popen('sudo ip -s -s neigh flush all', shell=True, stdout=subprocess.PIPE)

    @staticmethod
    def decode_text(text):
        if type(text) == type(u''):
            text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
        elif type(text) == type(''):
            text = unicodedata.normalize('NFKD', text.decode('utf8')).encode('ascii', 'ignore')
        return text

    class Result(object):
        def __init__(self, status=True, message=object):
            self.status = status
            self.message = message


