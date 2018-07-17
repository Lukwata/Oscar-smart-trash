import unittest

from aos.system.libs.user import User

data_user = User.login("phuongde@gmail.com", "123456")
print "data user longin ==>", data_user
token = data_user['data']['user']['access_token']


class UserTestCase(unittest.TestCase):
    def test_update_user(self):
        from random import randint
        num = str(randint(0, 9) * 1000000)
        data = {"phone": num, "fullname": "Phuong De Xom"}
        data = User.update(data, token)
        self.assertEqual(data['status'], 1)
        self.assertEqual(data['data']['customer']['phone'], num)


if __name__ == '__main__':
    unittest.main()
