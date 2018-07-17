#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import os
from mock import patch
from aos.system.libs.device import Device
from aos.system.libs.util import Util

url = os.getenv("API_URL")

# user_product_request = user_info(575, 'testmaya3@gmail.com', '4888c93a02a2e8d27bf9e2508782d8e0', "3d80c9c8-69d7-42e2-8d5c-5e56e9aada02")
# print user_product_request
# user_p_info = user_product_request['data']
# token = user_p_info['token']


class DeviceTestCase(unittest.TestCase):

    def setUp(self):

        from aos.system.libs.user import User
        data_user = User.login("phuongde@gmail.com", "123456")
        print "data user longin ==>", data_user

        self.token = data_user['data']['user']['access_token']

    @patch('aos.system.libs.api.__BASE_URL__', url)
    def test_check_valid_data_true(self):

        info = {}
        key_array = ['action', 'source', 'verify_code', 'address_long', 'address_lat', 'time_zone', 'user_id', 'wpa', 'ssid', 'user_hash',
                     'product_name', 'product_type', 'token', 'address']
        for key in key_array:
            info[key] = 'anything'
        import json
        info = json.dumps(info)
        result = Util.check_invalid_data(info)
        print result.message
        self.assertTrue(result.status)

    @patch('aos.system.libs.api.__BASE_URL__', url)
    def test_check_valid_data_false_without_address_long(self):
        info = {}
        key_array = ['action', 'source', 'verify_code', 'address_long', 'address_lat', 'time_zone', 'user_id', 'wpa', 'ssid', 'user_hash',
                     'product_name', 'product_type', 'token', 'address']
        for key in key_array:
            info[key] = 'anything'

        #remove key `address_long`
        del info['address_long']

        import json
        info = json.dumps(info)
        result = Util.check_invalid_data(info)
        print result.message
        self.assertFalse(result.status)
        self.assertEquals(result.message, 'key `address_long` is required.')

    @patch('aos.system.libs.api.__BASE_URL__', url)
    def test_add_product(self):
        product_id = Device.gen_product_id(self.token)
        print "product_id==>" + product_id
        self.assertIsNotNone(product_id)
        data = {"product_id": product_id,
                "product_name": "device-name-test",
                "product_type": "SMART_DESK",
                "address_long": 0,
                "address_lat": 0,
                "timezone": "VN",
                "source": "android",
                "verify_code": "code",
                "address": Util.decode_text("139 hồng hà, p9, phu nhuan")}
        device = Device(**data)
        rs = device.add_product(self.token)
        print rs
        self.assertIsNotNone(rs)

    def test_check_product(self):
        rs = Device.check_product("test", "SMART_DESK_3")
        self.assertIsNotNone(rs)

    def test_update_address(self):

        product_id = Device.gen_product_id(self.token)
        print "product_id==>" + product_id
        self.assertIsNotNone(product_id)

        data = {"product_id": product_id,
                "product_name": "device-name-test",
                "product_type": "SMART_DESK",
                "address_long": 0,
                "address_lat": 0,
                "product_key": product_id,
                "timezone": "VN",
                "source": "android",
                "verify_code": product_id,
                "address": Util.decode_text("139 hồng hà, p9, phu nhuan")}
        device = Device(**data)
        rs = device.add_product(self.token)
        print "result ==>", rs
        self.assertIsNotNone(rs)

        address_data = {"address": Util.decode_text("139 Bui dinh them, p9, phu nhuan"), "address_long": 0, "address_lat": 0, "timezone": "VN"}
        rs = device.update_address(token=self.token, product_id=product_id, address_data=address_data)
        print rs
        self.assertIsNotNone(rs)
        self.assertEqual(rs['data']['address'], Util.decode_text("139 Bui dinh them, p9, phu nhuan"))


if __name__ == '__main__':
    unittest.main()
