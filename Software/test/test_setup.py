import unittest
import test.test_support as test_env
import os
import sys
import threading
import time
import zmq
import json
import logging

from mock import patch

from aos.system.libs.api import user_info

logging.basicConfig(format='======== LOG UNITTEST %(asctime)s %(message)s ', level=logging.DEBUG)

api_url = os.getenv("API_URL")

user_product_request = user_info(575, 'testmaya3@gmail.com', '4888c93a02a2e8d27bf9e2508782d8e0', "3d80c9c8-69d7-42e2-8d5c-5e56e9aada02")
print user_product_request
user_p_info = user_product_request['data']
token = user_p_info['token']

class SetupBrainMockGetIpAdress(unittest.TestCase):
    def setUp(self):
        self.env = test_env.EnvironmentVarGuard()
        sys.path.append(os.environ['HOME'])  # Solution replace self.env.set('PYTHONPATH' ...
        self.env.set('DEVICE_TYPE', 'SMART_DESK')
        self.os_path = os.environ['HOME'] + '/aos/data/os_config.json'
        os.environ['__FIREBASE_CONFIG__'] = os.environ['HOME'] + "/aos/system/libs/tests/firebase.json"

    def tearDown(self):
        pass

    @patch('aos.system.libs.api.__BASE_URL__', api_url)
    @patch('aos.system.libs.util.Util.check_internet_connection')
    @patch('aos.system.libs.util.Util.get_ip_address')
    @patch('aos.system.setup.AutonomousSetup.check_wifi_loop')
    @patch('aos.system.libs.util.Util.has_s2t_feature')
    def test_setup_flow_newBoard_startOldConfig_phoneSendData(self, has_s2t_feature_mock, check_wifi_loop_mocked,
                                                              get_ip_address_mocked,
                                                              stop_hotspot_and_connect_wifi_mocked):
        get_ip_address_mocked.return_value = '192.168.42.1'
        check_wifi_loop_mocked.return_value = None
        has_s2t_feature_mock.return_value = None
        data = {'action': 'send_wifi_info',
                "wpa": "Do@nket201234",
                "ssid": "Robotbase",
                "user_id": 575,
                "user_hash": "4888c93a02a2e8d27bf9e2508782d8e0",
                "time_zone": "Asia/Ho_Chi_Minh",
                "firebase_uid": "123",
                "source": "phone",
                "verify_code": "verify_code" + str(time.time()),
                "address_long": 0,
                "address_lat": 0,
                "product_name": "con ga",
                "product_type": "SMART_DESK",
                "token": token

                }

        os_path = os.environ['HOME'] + '/aos/data/os_config.json'

        with self.env:
            from aos.system.setup import AutonomousSetup
            logging.debug("TH 1 - Board moi hoan toan, khong co file config.json")
            logging.debug("TH 1 - Gia su: PHONE gui data dung, connect duoc wifi")
            logging.debug("TH 1 - Mong moi doi cho: Gui nhan duoc data qua ZMQ")
            logging.debug("TH 1 - Mong moi doi cho: Phai tao duoc file config.json")

            # 1. Board moi hoan toan
            # -> Khong co os_config.json
            if os.path.isfile(os_path):
                os.remove(os_path)
            # gia su: PHONE gui data dung, conect wifi -> True:
            # Mong muon:
            # - phat duoc hotspot va gui nhan duoc data qua ZMQ
            # - phai co file os_config.json
            stop_hotspot_and_connect_wifi_mocked.return_value = True

            t = threading.Thread(target=AutonomousSetup().setup_from_config_data)
            t.setDaemon(True)
            t.start()
            time.sleep(30)
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect("tcp://localhost:5004")
            socket.send_json(data)
            message = socket.recv()

            # Check receive message from PHONE ok
            message_json = json.loads(message)
            self.assertEquals(message_json['action'], 'check_send')
            self.assertEquals(message_json['value'], '1')

            # doi 5s de thread chay xong cac thiet lap
            time.sleep(15)

            # check file tao duoc file config.json:
            self.assertTrue(os.path.isfile(os_path))


            logging.debug('TH 2 - Gia su: board da ok -> restart board')
            logging.debug('TH 2 - config dung, gia lap KHONG ket noi duoc internet (do thong tin wifi bi thay doi ...)')
            logging.debug('TH 2 - Mong muon: phat hotspot + gui nhan duoc data tu PHONE')
            # 2: gia su board da ok -> restart board:
            # config dung, gia lap KHONG ket noi duoc internet (do thong tin wifi bi thay doi ...)
            # Mong muon:
            # phat hotspot + gui nhan duoc data tu PHONE:
            stop_hotspot_and_connect_wifi_mocked.return_value = False
            t = threading.Thread(target=AutonomousSetup().setup_from_config_data)
            t.setDaemon(True)
            t.start()
            logging.debug('TH 2 - Doi 40s de khoi dong lai board + voi config o TH 1')
            time.sleep(40)
            socket.send_json({"action": "hotpost_connected"})
            message = socket.recv()
            message_json = json.loads(message)
            self.assertTrue(os.path.isfile(os_path))
            self.assertEquals(message_json['action'], 'check_send')
            self.assertEquals(message_json['value'], '1')


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

            time.sleep(30)

            with open(os_path, 'r') as f:
                file_config_content_after = f.read()

            # Phone gui sai mat khau thi ko duoc update file config
            file_config_content_after = json.loads(file_config_content_after)
            self.assertNotEquals(file_config_content_after['wpa'], new_data['wpa'])

            # 3.2: kiem tra hotpost thuc su con chay ko -> gui data va nhan duoc data:
            logging.debug('TH 3 - PHONE gui sai mat khau thi ko duoc tat hotspot')
            time.sleep(20)
            socket.send_json({"action": "hotpost_connected", })
            message = socket.recv()
            message_json = json.loads(message)
            self.assertEquals(message_json['action'], 'check_send')
            self.assertEquals(message_json['value'], '1')
