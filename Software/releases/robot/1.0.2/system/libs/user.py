from aos.system.libs.api import user_info


__response_success = {"status": "1"}
__response_fail = {"status": "0"}


class User(object):
    user_id = None
    email = None
    user_hash = None
    token = None
    full_name = None

    def __init__(self):
        super(User, self).__init__()

    @staticmethod
    def get_user_info():
        user = None
        user_product_info = User.sync_user_product_info()
        if user_product_info:
            try:
                user = User()
                print (user_product_info)
                user.user_hash = user_product_info['user_hash']
                user.user_id = user_product_info['id']
                user.email = user_product_info['email']
                user.token = user_product_info['token']
                user.full_name = user_product_info['full_name']
            except Exception as e:
                print 'Error (get_user_info)->' + str(e)
        return user

    @staticmethod
    def sync_user_product_info():
        from aos.system.libs.util import Util
        DATA_PATH = Util.get_current_path_app() + "data/"
        USER_DATA_PATH = DATA_PATH + "user.json"

        user_p_info = None
        try:
            os_config = Util.get_product_config()
            if os_config:
                user_product_request = user_info(os_config['user_id'], os_config['email'], os_config['user_hash'], os_config['product_id'])
                if user_product_request and user_product_request['status']:
                    user_p_info = user_product_request['data']
                    Util.write_file(USER_DATA_PATH, user_p_info)

        except Exception as e:
            print 'Error(sync_user_product_info)->' + str(e)
        return user_p_info

# if __name__ == '__main__':
#     user = User()
#     user.call_user_info(575, 'testmaya3@gmail.com', '2ea0446ad1bce750daa903f9ddddbcaf')
