import unittest

from aos.system.libs.card import Card
from aos.system.libs.user import User

data_user = User.login("phuongde@gmail.com", "123456")
print "data user longin ==>", data_user
token = data_user['data']['user']['access_token']


class TestCard(unittest.TestCase):

    def setUp(self):
        pass

    def test_add_card_with_data_OK(self):

        data = {
          "cc_number": "5555555555554444",
          "cc_expired": "12/20",
          "cc_cvc": "123"
        }
        rs = Card.add(data, token=token)
        print rs
        self.assertIsNotNone(rs)
        self.assertEqual(rs['status'], 1)
        self.assertEqual(rs['data']['payment_setting']['last_4_digits'], '4444')

    def test_add_card_with_miss_data_cc_expired(self):
        data = {
            "cc_number": "5555555555554444",
            "cc_cvc": "123"
        }
        print "token test_add_card_with_miss_data_cc_expired ==>", token
        rs = Card.add(data, token=token)
        print rs
        self.assertIsNotNone(rs)
        self.assertEqual(rs['status'], 0)

    def test_update_card_with_cc_expired(self):
        data = {
            "cc_number": "5555555555554444",
            "cc_expired": "12/30",
            "cc_cvc": "123"
        }
        rs = Card.add(data, token=token)
        print rs
        self.assertIsNotNone(rs)
        self.assertEqual(rs['status'], 1)
        self.assertEqual(rs['data']['payment_setting']['last_4_digits'], '4444')

        # neu lay thong in ve lai, thi se co cap nhat:
        payment_setting_id = rs['data']['payment_setting']['payment_setting_id']
        data = {
            "cc_number": "5555555555554444",
            "cc_expired": "12/30",
            "cc_cvc": "153",
            "payment_setting_id": payment_setting_id
        }
        rs = Card.update(data, token=token)
        print rs
        self.assertIsNotNone(rs)
        self.assertEqual(rs['status'], 1)
        self.assertEqual(rs['data']['payment_setting']['payment_setting_id'], payment_setting_id)

    def test_get_list_card(self):
        rs = Card.list(token=token)
        print rs
        self.assertIsNotNone(rs)
        self.assertEqual(rs['status'], 1)
        self.assertIsNotNone(len(rs['data']['payment_settings']) > 0)

if __name__ == '__main__':
    unittest.main()
