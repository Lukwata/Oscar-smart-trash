import random
import string
import unittest
import os
import time
import logging
from mock import patch
from requests import HTTPError
from aos.system.libs.firebase import Firebase


class TestFirebase(unittest.TestCase):

    def setUp(self):
        os.environ['__FIREBASE_CONFIG__'] =  os.environ['HOME'] + "/aos/system/libs/tests/firebase.json"

    def tearDown(self):
        pass

    def test_init_firebase_without_config_return_invalid_firebase(self):
        os.environ['__FIREBASE_CONFIG__'] = ""
        fb = Firebase()
        self.assertIsNone(fb.firebase)

    def test_create_firebase(self):

        logging.debug("test truong hop tao 1 account bat ky, mong muon tra ve duoc id, token")
        name = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        email = name+'@autonomous.ai'
        password = '12345678'

        fb = Firebase()
        rs = fb.get_firebase_uid(email, password)

        self.assertTrue(rs)
        self.assertIsNotNone(fb.localId)
        self.assertIsNotNone(fb.idToken)

        ID1 = fb.localId

        logging.debug("id >> ", fb.localId)
        logging.debug( "token >> ", fb.idToken)

        logging.debug("test login lai, mong muon login thanh cong va id se trung voi `ID1`:")
        rs = fb.get_firebase_uid(email, password)

        logging.debug( "id login>> ", fb.localId)
        logging.debug( "token login>> ", fb.idToken)

        self.assertTrue(rs)
        self.assertTrue(fb.localId==ID1)

        logging.debug("test ghi data thanh cong cho 1 user ID1")
        product_id = 'product_id_A'
        data = {
            "type": "product_control",
            "source": "",
            "data": {"action": "call_taxi"},
            "protocol": "123",
            "timestamp": time.time(),
        }
        db = fb.firebase.database()
        results = db.child(fb.localId).child(product_id).push(data, fb.idToken)
        self.assertIsNotNone(results)

        logging.debug("test user A duoc xoa data cua chinh chanel cua no:")
        try:
            results = db.child(fb.localId).child(product_id).remove(fb.idToken)
            self.assertTrue(True)
        except Exception as e:
            logging.debug( str(e))
            self.assertTrue(False)

        logging.debug("nhung khong duoc xoa tren node ID goc")
        try:
            results = db.child(fb.localId).remove(fb.idToken)
            self.assertTrue(False)
        except Exception as e:
            logging.debug(str(e))
            self.assertTrue(True)

        logging.debug("test tao 1 user_B de write len chanel cua user A")
        rs = fb.get_firebase_uid("emailB@gmail.com", '12345678')
        self.assertTrue(rs)
        self.assertIsNotNone(fb.localId)
        self.assertTrue(fb.localId != ID1)

        logging.debug("test ghi data len chinh no truoc:")
        product_id = 'product_id_B'
        data = {
            "type": "product_control",
            "source": "",
            "data": {"action": "call_taxi"},
            "protocol": "123",
            "timestamp": time.time(),
        }
        db = fb.firebase.database()
        results = db.child(fb.localId).child(product_id).push(data, fb.idToken)
        self.assertIsNotNone(results)

        logging.debug("test write data hop le len user A, product_id_A (UD1, not localID)")
        product_id = 'product_id_A'
        data = {
            "type": "product_control",
            "source": "product_id_B",
            "data": {"action": "call_taxi"},
            "protocol": "123",
            "timestamp": time.time(),
        }
        # results = db.child(ID1).child(product_id).push(data, fb.idToken)
        # self.assertIsNotNone(results)

        logging.debug("test user B ko duoc xoa data cua chanel user A (ID1)")
        try:
            results = db.child(ID1).child(product_id).remove(fb.idToken)
            self.assertTrue(False)
        except HTTPError as (e, text):

            if e.response.status_code == 401 and "Permission denied" in e.response.content:
                self.assertTrue(True)

        logging.debug("cang ko duoc xoa data cua user")
        try:
            results = db.child(ID1).remove(fb.idToken)
            self.assertTrue(False)
        except HTTPError as (e, text):
            if e.response.status_code == 401 and "Permission denied" in e.response.content:
                self.assertTrue(True)

        logging.debug("test user B ko duoc ghi data ko hop len le data cua chanel user A (ID1)")
        logging.debug("data khong du tham so:")
        del data['type']
        del data['data']
        try:
            results = db.child(ID1).child(product_id).push(data, fb.idToken)
            self.assertTrue(False)
        except HTTPError as (e, text):
            if e.response.status_code == 401 and "Permission denied" in e.response.content:
                self.assertTrue(True)

        logging.debug("data khong phai json")
        try:
            results = db.child(ID1).child(product_id).push("day ko phai la json", fb.idToken)
            self.assertTrue(False)
        except HTTPError as (e, text):
            if e.response.status_code == 401 and "Permission denied" in e.response.content:
                self.assertTrue(True)

        logging.debug("data khong duoc phep, nhu factory_reset")
        data = {
            "type": "product_control",
            "source": "product_id_X",#source nay ko ton tai
            "data": {"action": "factory_reset"},
            "protocol": "123",
            "timestamp": time.time(),
        }
        logging.debug("data khong duoc phep, source khong ton tai")
        try:
            results = db.child(ID1).child(product_id).push(data, fb.idToken)
            self.assertTrue(False)
        except HTTPError as (e, text):
            if e.response.status_code == 401 and "Permission denied" in e.response.content:
                self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()