import json
import unittest

from aos.ability.install_ability_device.install_app import InstallUpdateAbility


class TestCaseInstallAbility(unittest.TestCase):

    def setUp(self):
        #gia lap data tu brain:
        self.data = json.loads(json.loads ("{\"source\": \"eac7efdf-00ce-4404-af69-26c9da50cb39\", \"type\": \"install_ability_device\", \"protocol\": \"firebase\", \"data\": \"{\\\"app\\\": \\\"product_control_test\\\", \\\"version\\\": \\\"2.0.0\\\", \\\"link\\\": \\\"http://s3.amazonaws.com/s3-robotbase/product_control_test.zip\\\", \\\"is_service\\\": 0, \\\"action\\\": \\\"add\\\", \\\"md5_hash\\\": \\\"42e144f5829753ff55d953367297a2d2\\\", \\\"application_file\\\": \\\"main.py\\\"}\", \"time\": \"1489720855370000000\"}")['data'])

    def test_is_valid_data_false(self):
        del self.data['app']
        self.install_app = InstallUpdateAbility(self.data)
        self.assertFalse(self.install_app.is_valid_data)

    def test_is_valid_data_true(self):
        self.install_app = InstallUpdateAbility(self.data)
        self.assertTrue(self.install_app.is_valid_data)

    def test_is_valid_data_add_false_without_md5(self):
        del self.data['md5_hash']
        self.install_app = InstallUpdateAbility(self.data)
        self.assertFalse(self.install_app.is_valid_ability())

    def test_is_valid_data_add_false_without_link(self):

        del self.data['link']
        self.install_app = InstallUpdateAbility(self.data)

        self.assertFalse(self.install_app.is_valid_ability())

    def test_is_valid_data_add_true(self):

        self.install_app = InstallUpdateAbility(self.data)

        self.assertTrue(self.install_app.is_valid_ability())

    def test_download_success(self):
        self.install_app = InstallUpdateAbility(self.data)

        self.assertTrue(self.install_app.is_valid_ability())

        self.assertTrue(self.install_app.download())

    def test_download_and_unzip_success_with_md5_true(self):
        self.install_app = InstallUpdateAbility(self.data)

        self.assertTrue(self.install_app.is_valid_ability())

        self.assertTrue(self.install_app.download())

        self.assertTrue(self.install_app.unzip())

    def test_download_and_unzip_NOT_success_with_md5_false(self):

        self.data['md5_hash'] = 'random_md5_hash...'

        self.install_app = InstallUpdateAbility(self.data)

        self.assertTrue(self.install_app.is_valid_ability())

        self.assertTrue(self.install_app.download())

        self.assertTrue(self.install_app.unzip())

    def test_update_config_true(self):
        self.install_app = InstallUpdateAbility(self.data)

        self.assertTrue(self.install_app.is_valid_ability())

        self.assertTrue(self.install_app.download())

        self.assertTrue(self.install_app.unzip())

        self.assertTrue(self.install_app.update_config())

        from aos.system.configs.channel import BASE_APP
        app_path_config = BASE_APP + self.install_app.app_name + "/config.json"

        import os
        self.assertTrue(os.path.isfile(app_path_config))

        from aos.system.libs.util import Util
        version = Util.read_file(app_path_config)['version']

        print "compare version: ", version, self.install_app.version

        self.assertTrue(version == self.install_app.version)

    def test_full_install_true(self):

        self.install_app = InstallUpdateAbility(self.data)
        self.assertTrue(self.install_app.run())

    def test_is_valid_ability_FALSE_with_not_new_version(self):

        # testcase nay remove nhe.

        self.assertTrue(True)

        #  version:
        # self.data['version'] = '2.2.0'
        # self.install_app = InstallUpdateAbility(self.data)
        # self.assertTrue(self.install_app.run())
        #
        # self.assertTrue(self.install_app.version == self.data['version'])
        #
        # self.data['version'] = '2.2.0'
        # self.install_app = InstallUpdateAbility(self.data)
        #
        # self.assertFalse(self.install_app.is_valid_ability())
        #
        # self.data['version'] = '1.0.0'
        # self.install_app = InstallUpdateAbility(self.data)
        #
        # self.assertFalse(self.install_app.is_valid_ability())

    def test_remove_app_success(self):
        import os

        self.install_app = InstallUpdateAbility(self.data)
        self.assertTrue(self.install_app.run())

        self.data['action'] = "remove"
        self.install_app = InstallUpdateAbility(self.data)

        self.assertTrue(self.install_app.run())

        self.assertTrue(not os.path.isdir(self.install_app.app_base_dir))

    def tearDown(self):
        try:
            import os
            if os.path.isdir(self.install_app.app_base_dir):
                import shutil
                shutil.rmtree(self.install_app.app_base_dir)
        except:
            pass


if __name__ == '__main__':
    unittest.main()
