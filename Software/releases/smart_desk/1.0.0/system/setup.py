#!/usr/bin/env python
#
# Copyright (C) 2017 Autonomous Inc. All rights reserved.
#

import os
import threading
from time import sleep
import sys
import subprocess
import zmq

from aos.system.configs.channel import PATH_WIFI_CONFIG, LOCAL_HOTSPOT, \
    IP_HOST_SPOT, DEVICE_TYPE, KILL_BRAIN_TMUX_CMD, \
    BRAIN_TMUX_CMD, PATH_PRODUCT_ID_CONFIG, __EMAIL_FIX__
from aos.system.libs.device import Device
from aos.system.libs.firebase import Firebase
from aos.system.libs.util import Util
from aos.system.libs.wifi import WifiHostpot
from aos.system.libs.notify import Notify


# ----------------------------


class AutonomousSetup(object):
    def __init__(self):

        print "init notify ..."
        self.notify = Notify() if Util.has_s2t_feature() else None

        print "pls wait ..."
        if self.notify: self.notify.run(Notify.NotifyType.PLS_WAIT)

        print "init hotspot ..."
        self.wifi_hostpot = WifiHostpot(DEVICE_TYPE)

        print "start zmq ..."
        self.context = None
        self.results_receiver = None

        # for check wifi loop:
        self.check_loop_wifi_is_running = False
        self.hotspot_flag = False
        self.wifi_connecting = False

        self.ssid = None
        self.wpa = None

        print "starting brain first ..."
        AutonomousSetup.run_brain()

    @staticmethod
    def run_brain():
        print "killing brain ..."
        Util.cmd(KILL_BRAIN_TMUX_CMD)
        print 'starting brain ... '
        Util.cmd(BRAIN_TMUX_CMD, False)

    def connect_wifi(self):
        self.wifi_connecting = True
        self.hotspot_flag = False
        is_onnected = self.wifi_hostpot.stop_hotspot_and_connect_wifi(self.ssid, self.wpa)
        self.wifi_connecting = False
        return is_onnected

    def start_hotspot(self):
        self.hotspot_flag = True
        print "status is false, sleep 5s for creating hotspot..."
        sleep(5)
        self.wifi_hostpot.start_hotspot()
        sleep(2)
        if Util.get_ip_address() == IP_HOST_SPOT:
            if self.notify:
                self.notify.run(Notify.NotifyType.IN_SETUP_MODE)
                Util.clear_cache_arp()
                # loop listen device connect:
                self.has_device_connected()

            # zmq listen:
            self.start_listen_data_from_phone()
        else:
            print "Not create hotspot, create again ..."
            self.start_hotspot()

    def start_listen_data_from_phone(self):
        self.stop_listen_hotspot()
        sleep(2)

        print("Starting zmq Context to get wifi data... ")
        self.context = zmq.Context()
        self.results_receiver = self.context.socket(zmq.REP)
        self.results_receiver.bind(LOCAL_HOTSPOT)
        print("Listening data info from phone...")

        while True:
            try:
                data_string = self.results_receiver.recv()
                print "Receive data!", data_string

                result = Util.check_invalid_data(data_string)
                if not result.status:
                    data_send = '{"action": "check_send", "value": "0", "error_message": "' + result.message + '"}'
                    self.results_receiver.send(data_send)
                else:
                    data_info = result.message
                    if data_info['action'] == 'send_wifi_info' or data_info['action'] == 'hotpost_connected':
                        data_send = '{"action": "check_send", "value": "1"}'
                        self.results_receiver.send(data_send)

                        if data_info['action'] == 'send_wifi_info':
                            #sleep for send to phone!:
                            sleep(3)
                            self.setup_from_phone_data(data_info)
                            break
            except:
                print "error receive package!:", sys.exc_info()

        self.stop_listen_hotspot()

    def stop_listen_hotspot(self):
        print ("stopping listen zmq ...")
        try:
            if self.context:
                self.context.close()
            if self.results_receiver:
                self.results_receiver.term()
        except:
            sys.exc_info()
            pass

    def setup_from_config_data(self):
        print "reading config for setup ..."
        try:
            # Check os_config:
            if os.path.isfile(PATH_WIFI_CONFIG):
                if self.ssid is None and self.wpa is None:
                    os_config = Util.read_file(PATH_WIFI_CONFIG)
                    self.ssid = os_config['ssid']
                    self.wpa = os_config['wpa']
                # check thu internet truoc:
                is_connected = Util.check_internet_connection(steps=10)
                # neu ko co internet thi connect thu lai wifi:
                if is_connected is False:
                    is_connected = self.connect_wifi()
                if is_connected:
                    self.ready_to_use()
                else:
                    self.not_ready_to_use()
            else:
                # neu ko co config thi run hotspot:
                self.start_hotspot()

        except Exception as e:
            print "Unexpected error:", str(e)
            pass

    def setup_from_phone_data(self, wifi_data):

        if self.notify: self.notify.run(Notify.NotifyType.PLS_WAIT)

        if wifi_data:
            try:
                # wifi connected
                self.ssid = wifi_data['ssid']
                self.wpa = wifi_data['wpa']
                if self.connect_wifi():

                    if self.notify: self.notify.run(Notify.NotifyType.WIFI_CONNETED)

                    wifi_data['product_id'] = Util.check_match_current_user(wifi_data['user_id'])
                    if wifi_data['product_id'] == '': wifi_data['product_id'] = Device.gen_product_id(wifi_data['token'])

                    print "New: add product now:"
                    if wifi_data['product_id'] != '':

                        if self.notify: self.notify.run(Notify.NotifyType.PLS_WAIT)

                        print "gen firebase_uid:"
                        firebase = Firebase()
                        if firebase.get_firebase_uid(wifi_data['product_id'] + __EMAIL_FIX__, wifi_data['user_hash']):
                            wifi_data['firebase_uid'] = firebase.localId
                            device = Device(**wifi_data)
                            if device.add_product(wifi_data['token']):
                                print "add product success.", "Ghi file de cac app khac lay data va xu ly:"

                                Util.write_file(PATH_WIFI_CONFIG, wifi_data)
                                Util.write_file(PATH_PRODUCT_ID_CONFIG, wifi_data)

                                print "update product_id cho pr_device config"
                                Util.update_pr_device_id(wifi_data['product_id'], wifi_data['firebase_uid'])

                                sleep(1)

                                print "restart brain again new config"
                                AutonomousSetup.run_brain()

                                sleep(10)
                                self.ready_to_use()

                                return

                # Co loi trong qua trinh setup hoac ko connect duoc wifi:
                if self.notify: self.notify.run(Notify.NotifyType.CANNOT_CONNECT_WIFI_TRY_AGAIN)
                self.start_hotspot()

            except Exception as e:
                print "data error => " + str(e)
                pass

    def not_ready_to_use(self):
        print 'no ready to use'
        if self.notify:
            self.notify.run(notify_type=self.notify.NotifyType.CANNOT_CONNECT_WIFI_TRY_AGAIN)
            if self.check_loop_wifi_is_running is False: self.check_wifi_loop()
        else:
            # Tren device ko co t2s thi phat hotspot:
            self.start_hotspot()

    def ready_to_use(self):
        print 'Ready to use'
        # set timezone for user location
        Util.set_date_time()
        if self.notify: self.notify.run(Notify.NotifyType.DEVICE_READY_TO_USE)
        if self.check_loop_wifi_is_running is False: self.check_wifi_loop()

    # Kiem tra neu co device connect toi thi thong bao cho user san sang setup truyen thong tin wifi qua
    def has_device_connected(self):
        try:
            proc = subprocess.Popen('sudo arp -a', shell=True, stdout=subprocess.PIPE)
            for line in proc.stdout:
                item = line.split()
                # name = item[0], IP = item[1], at = item[2],MAC = item[3]
                MAC = item[3]
                if "incomplete" not in MAC:
                    # print "has device: ", name, IP, MAC
                    if self.notify:
                        self.notify.run(Notify.NotifyType.DEVICE_CONNECTED_TO_HOTSPOT)
                    return
        except Exception as e:
            print "error in has_device_connected" + str(e)
            pass
        threading.Timer(3, self.has_device_connected).start()

    def check_wifi_loop(self):
        try:
            print "check connect and connect wifi ..."
            threading.Timer(120, self.check_wifi_loop).start()
            if self.check_loop_wifi_is_running is False:
                self.check_loop_wifi_is_running = True
                # khong muon lan dau tien chay code ben duoi!
                return
            if self.wifi_connecting is False and self.hotspot_flag is False and Util.get_ip_address() == 'unknown':
                if self.connect_wifi():
                    print "auto connect wifi ok!"
                else:
                    if self.notify:
                        self.notify.run(Notify.NotifyType.WIFI_ISNOT_SETUP)
            else:
                print "nothing!"
        except Exception as e:
            print "Unexpected error => " + str(e)


if __name__ == '__main__':
    AutonomousSetup().setup_from_config_data()
