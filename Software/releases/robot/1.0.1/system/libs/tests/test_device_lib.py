import unittest

from mock import patch

from aos.system.libs.device import Device
from aos.system.libs.util import Util

url = "http://54.254.216.169/v2/"

class DeviceTestCase(unittest.TestCase):


    def setUp(self):
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6NTc1LCJpYXQiOjE0ODg4ODI3NDUsIm5iZiI6MTQ4ODg4Mjc0NSwiZXhwIjoxNDkxNDc0NzQ1fQ.Yv7jM0Ki-SeCUe0mAWH-BVgCXI4WRPwPDDNMfjGMx5g'

    @patch('aos.system.libs.api.__BASE_URL__', url)
    def test_check_valid_data_true(self):

        info = {}
        key_array = ['source', 'verify_code', 'address_long', 'address_lat', 'time_zone', 'user_id', 'wpa', 'ssid', 'user_hash',
                     'product_name', 'product_type', 'token']
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
        key_array = ['source', 'verify_code', 'address_long', 'address_lat', 'time_zone', 'user_id', 'wpa', 'ssid', 'user_hash',
                     'product_name', 'product_type', 'token']
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
        print product_id
        self.assertIsNotNone(product_id)
        device = Device ("code", product_id, "device-name-test", 'PERSONAL_ROBOT', 0, 0, 'VN' , 'android')
        rs = device.add_product(self.token)
        print rs
        self.assertIsNotNone(rs)


if __name__ == '__main__':
    unittest.main()
