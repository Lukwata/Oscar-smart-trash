import unittest
import os
import threading
import time
import zmq
import json
import logging
import mock
import collections
import subprocess
import commands
from firebase import FirebaseApplication, FirebaseAuthentication
from firebase import jsonutil

# from aos.system.libs.util import Util

logging.basicConfig(format='======== LOG UNITTEST %(asctime)s %(message)s ', level=logging.DEBUG)


class TestProductControl(unittest.TestCase):
    def setUp(self):
        self.os_path = os.environ['HOME'] + '/aos/data/os_config.json'

        firebaseConfig = {
            'app_server_id': '8fed4642-2075-4b4d-a605-3478acd2b4dd',
            'dsn': 'https://personalrobot-1470372118376.firebaseio.com/',
            'uid': 'api@autonomousbrain.com',
            'dbSecret': 'DK1PezoaQS0usTCfp4tiskPxh5U62J2GxvLuTJdv',
        }
        auth = FirebaseAuthentication(secret=firebaseConfig['dbSecret'], email=firebaseConfig['uid'])
        self.firebase = FirebaseApplication(dsn=firebaseConfig['dsn'])
        self.firebase.authentication = auth
        self.product_id = '41425a58-153f-4250-9cc9-521be16350f9'

    def tearDown(self):
        pass

    def test_product_control(self):
        data = {'action': 'send_wifi_info',
                "product_id": self.product_id,
                "wpa": "autonomous123",
                "ssid": "AutonomousDevice",
                "user_id": 819,
                "user_hash": "b6a85f3a485dac01e59e086f5f9ec773",
                "time_zone": "Asia/Ho_Chi_Minh",
                "firebase_uid": "YjwdodoDuAb31duUj4DAw01HHXG3"
                }

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

        # Check deskRep already running and start
        output = commands.getoutput('ps -ef')
        if 'bash run.sh' not in output:
            temp_str = ('%s/aos/system/%s/deskApp/deskRep' % (os.getenv('HOME'), os.getenv('DEVICE_TYPE')))
            subprocess.Popen('bash run.sh'.split(), cwd=temp_str)

        time.sleep(20)
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

        # Bat dau test product control
        logging.debug('TH 1 - Bat dau test product control UP-STOP-DOWN-STOP')

        # Doi brain chay xong, send message via firebase
        message_firebase_down = {"type": "product_control",
                                 "source": self.product_id + "_PHONE",
                                 "data": {"action": "down", "value": "",
                                          "timestamp": "1489132841383.799072"},
                                 "protocol": "firebase", "time": "1489132841383809.000000"}
        message_firebase_down['data'] = json.dumps(message_firebase_down['data'])
        message_firebase_down = json.dumps(message_firebase_down)

        message_firebase_stop = {"type": "product_control",
                                 "source": self.product_id + "_PHONE",
                                 "data": {"action": "stop", "value": "",
                                          "timestamp": "1489132841383.799072"},
                                 "protocol": "firebase", "time": "1489132841383809.000000"}
        message_firebase_stop['data'] = json.dumps(message_firebase_stop['data'])
        message_firebase_stop = json.dumps(message_firebase_stop)

        message_firebase_up = {"type": "product_control",
                               "source": self.product_id + "_PHONE",
                               "data": {"action": "up", "value": "",
                                        "timestamp": "1489132841383.799072"},
                               "protocol": "firebase", "time": "1489132841383809.000000"}

        message_firebase_up['data'] = json.dumps(message_firebase_up['data'])
        message_firebase_up = json.dumps(message_firebase_up)

        self.firebase.delete('/', self.product_id + '_PHONE')

        self.firebase.post(url=self.product_id, data=message_firebase_up)
        self.firebase.post(url=self.product_id, data=message_firebase_stop)
        self.firebase.post(url=self.product_id, data=message_firebase_down)
        self.firebase.post(url=self.product_id, data=message_firebase_stop)
        self.firebase.post(url=self.product_id, data=message_firebase_up)
        self.firebase.post(url=self.product_id, data=message_firebase_up)
        self.firebase.post(url=self.product_id, data=message_firebase_stop)
        self.firebase.post(url=self.product_id, data=message_firebase_down)
        self.firebase.post(url=self.product_id, data=message_firebase_down)
        self.firebase.post(url=self.product_id, data=message_firebase_stop)

        res = []
        res_dict = {}
        # get response
        for i in range(3):
            response = self.firebase.get('/' + self.product_id + '_PHONE', None)
            time.sleep(3)
            res = response

        # sort response by time stamp
        for i in res:
            res_dict[json.loads(json.loads(res[i])['data'])['timestamp']] = json.loads(json.loads(res[i])['data'])[
                'action']
        res_dict_sorted = collections.OrderedDict(sorted(res_dict.items()))

        self.assertEquals(res_dict_sorted.items()[0][1], 'up')
        self.assertEquals(res_dict_sorted.items()[1][1], 'stop')
        self.assertEquals(res_dict_sorted.items()[2][1], 'down')
        self.assertEquals(res_dict_sorted.items()[3][1], 'stop')
        self.assertEquals(res_dict_sorted.items()[4][1], 'up')
        self.assertEquals(res_dict_sorted.items()[5][1], 'up')
        self.assertEquals(res_dict_sorted.items()[6][1], 'stop')
        self.assertEquals(res_dict_sorted.items()[7][1], 'down')
        self.assertEquals(res_dict_sorted.items()[8][1], 'down')
        self.assertEquals(res_dict_sorted.items()[9][1], 'stop')
