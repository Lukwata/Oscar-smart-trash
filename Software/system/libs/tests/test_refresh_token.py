import unittest

from aos.system.configs.channel import PATH_USER_CONFIG
from aos.system.libs.request_api import RequestApi
from aos.system.libs.user import User
from aos.system.libs.util import Util

user = User.login('phuongde@gmail.com', '123456')
refresh_token = user['data']['user']['refresh_token']


class TestRefreshTokenCase(unittest.TestCase):

    def test_refresh_token(self):

        result = RequestApi.refresh_token(refresh_token)

        self.assertTrue(result is not False)

        data_user = user['data']['user']
        token_old = 'test test'
        data_user['access_token'] = token_old
        print "token_old->" + token_old

        Util.write_file(PATH_USER_CONFIG, data_user)

        result = RequestApi().update_token()
        print "update_token->", result
        self.assertTrue(result)

        # check lai token moi co khac ban dau ko?
        user_data_new = Util.read_file(PATH_USER_CONFIG)
        print "token_new->" + user_data_new['access_token']

        self.assertNotEqual(token_old, user_data_new['access_token'])

    def test_refresh_token_fail(self):
        refresh_token = 'con gai den'
        result = RequestApi.refresh_token(refresh_token)
        print result
        self.assertTrue(result is False)


if __name__ == '__main__':
    unittest.main()
