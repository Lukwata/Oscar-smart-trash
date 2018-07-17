import unittest
import os
import threading
import time
import zmq
import json
import logging
import mock
import subprocess
from aos.system.libs.util import Util

logging.basicConfig(format='======== LOG UNITTEST %(asctime)s %(message)s ', level=logging.DEBUG)


class TestSetup(unittest.TestCase):
    def setUp(self):
        self.os_path = os.environ['HOME'] + '/aos/data/os_config.json'

    def tearDown(self):
        pass

    @mock.patch('aos.system.setup.AutonomousSetup.check_wifi_loop')
    def test_setup_flow_newBoard_startOldConfig_phoneSendData(self, check_wifi_loop_mock):
        check_wifi_loop_mock.return_value = False
        data = {'action': 'send_wifi_info',
                "product_id": "fb9db337-96ac-4b97-baa0-e858d9180576",
                "wpa": "autonomous123",
                "ssid": "AutonomousDevice",
                "user_id": 46,
                "user_hash": "b6a85f3a485dac01e59e086f5f9ec773",
                "time_zone": "Asia/Ho_Chi_Minh",
                "firebase_uid": "123"
                }
        # os_path = os.environ['HOME'] + '/aos/data/os_config.json'

        from aos.system.setup import AutonomousSetup
        logging.debug("TH 1 - Board moi hoan toan, khong co file config.json")
        logging.debug("TH 1 - Gia su: PHONE gui data dung, connect duoc wifi")
        logging.debug("TH 1 - Mong doi: Gui nhan duoc data qua ZMQ")
        logging.debug("TH 1 - Mong doi: Phai tao duoc file config.json")

        # 1. Board moi hoan toan
        # -> Khong co os_config.json
        if os.path.isfile(self.os_path):
            os.remove(self.os_path)
        # gia su: PHONE gui data dung, conect wifi -> True:
        # Mong muon:
        # - phat duoc hotspot va gui nhan duoc data qua ZMQ
        # - phai co file os_config.json

        t = threading.Thread(target=AutonomousSetup().setup_from_config_data)
        t.setDaemon(True)
        t.start()
        time.sleep(10)
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5004")
        socket.send_json(data)
        message = socket.recv()

        # Check receive message from PHONE ok
        message_json = json.loads(message)
        self.assertEquals(message_json['action'], 'check_send')
        self.assertEquals(message_json['value'], '1')

        logging.debug('TH 1 - Board da nhan data tu phone, doi den khi connect wifi xong va ghi file os_config.json')
        logging.debug('TH 1 - timeout la 200s ...')
        rs = False
        count = 0
        while (True):
            count += 1
            print count,
            rs = os.path.isfile(self.os_path)
            time.sleep(1)
            if rs or count >= 230:
                break

        # check file tao duoc file config.json:
        self.assertTrue(rs)
        logging.debug('TH 1 - Connect duoc wifi va tao os_config.json thanh cong')

        logging.debug('TH 2 - Gia su: board da ok -> restart board')
        logging.debug('TH 2 - config dung, gia lap KHONG ket noi duoc internet (do thong tin wifi bi thay doi ...)')
        logging.debug('TH 2 - Mong muon: phat hotspot + gui nhan duoc data tu PHONE')
        # 2: gia su board da ok -> restart board:
        # config dung, gia lap KHONG ket noi duoc internet (do thong tin wifi bi thay doi ...)
        # Mong muon:
        # phat hotspot + gui nhan duoc data tu PHONE:

        # Thay doi mat khau wifi
        data_wrong_pass_wifi = data.copy()
        data_wrong_pass_wifi['wpa'] = 'wrong_pass_wifi'
        Util.write_file(self.os_path, data_wrong_pass_wifi)
        subprocess.call(['sudo', 'ifdown', 'wlan0'])
        time.sleep(1)

        t = threading.Thread(target=AutonomousSetup().setup_from_config_data)
        t.setDaemon(True)
        t.start()
        logging.debug('TH 2 - Doi 180s de khoi dong lai board voi mat khau wifi da thay doi')
        time.sleep(180)
        socket.send_json({"action": "hotpost_connected"})
        message = socket.recv()
        message_json = json.loads(message)
        self.assertTrue(os.path.isfile(self.os_path))
        self.assertEquals(message_json['action'], 'check_send')
        self.assertEquals(message_json['value'], '1')
        logging.debug('TH 2 - Phat hotspot va nhan data tu phone ok')

        # 3: truong hop gui data tu PHONE dung, nhung ko ket noi duoc wifi thi:
        # 3.1. KHONG update lai file config.json (TH2) neu phone gui sai mat khau
        logging.debug('TH 3 - Gui format data tu PHONE dung')
        logging.debug('TH 3 - Gia su sai mat khau wifi')
        logging.debug('TH 3 - Mong muon: KHONG duoc update mat khau vao file config.json')

        # Phone gui sai mat khau
        new_data = data.copy()
        new_data['wpa'] = '123456'
        socket.send_json(new_data)
        message = socket.recv()
        message_json = json.loads(message)
        self.assertEquals(message_json['action'], 'check_send')
        self.assertEquals(message_json['value'], '1')

        time.sleep(3)

        with open(self.os_path, 'r') as f:
            file_config_content_after = f.read()

        # Phone gui sai mat khau thi ko duoc update file config
        file_config_content_after = json.loads(file_config_content_after)
        self.assertNotEquals(file_config_content_after['wpa'], new_data['wpa'])

        # 3.2: kiem tra hotpost thuc su con chay ko -> gui data va nhan duoc data:
        logging.debug('TH 3 - PHONE gui sai mat khau thi ko duoc tat hotspot')
        logging.debug('TH 3 - Phai doi rat lau de board ket noi wifi va phat lai hotspot, timeout 250s ...')
        time.sleep(250)
        logging.debug('TH 3 - Sai mat khau, bat lai hotspot, phone send data')
        socket.send_json({"action": "hotpost_connected", })
        message = socket.recv()
        message_json = json.loads(message)
        self.assertEquals(message_json['action'], 'check_send')
        self.assertEquals(message_json['value'], '1')
