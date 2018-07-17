import os
import unittest
from time import sleep

from mock import patch


class testupdate(unittest.TestCase):

    def setUp(self):
        
        self.data = None
        if os.environ["DEVICE_TYPE"] == "SMART_DESK_C":
            self.data = {
                "app": "system",
                "version": "1.1.1",
                "link1": "https://s3.amazonaws.com/robotbase-cloud/system/smart_robot1.1.1_62.zip",
                "link": "https://s3.amazonaws.com/robotbase-cloud/deb-store/system.zip",
                "md5_hash": "403197b03ec69a04231725c17d56597f"
            }
        if os.environ["DEVICE_TYPE"] == "SMART_DESK":
            self.data = {
                "app": "system",
                "version": "1.0.2",
                "link": "http://s3.amazonaws.com/robotbase-cloud/deb-store/system1.0.2_desk.zip",
                "md5_hash": "b3d0e87f2e50c3e9f693b35023e937a9",
                "force_update": 1,
                "silent_link": "http://s3.amazonaws.com/s3-autonomous/s2b.sh"
            }

        if self.data:
            from aos.ability.firmware_update.update_online import UpdateOnline
            self.update = UpdateOnline(self.data)

    # @patch("aos.system.libs.util.Util.get_version")
    # def test_check_is_valid_system_is_false_by_version(self, get_version_mock_function):
    #
    #     get_version_mock_function.return_value = 123
    #     self.assertFalse(self.update.is_valid_system())
    #
    # def test_check_is_valid_system_is_false_by_without_version(self):
    #     del self.data['version']
    #     self.assertFalse(self.update.is_valid_system())
    #
    # def test_check_is_valid_system_is_false_by_without_link(self):
    #     #remove key 'link' from data:
    #     del self.data['link']
    #     self.assertFalse(self.update.is_valid_system())
    #
    # @patch("aos.system.libs.util.Util.get_version")
    # def test_check_is_valid_system_is_true_by_version(self, get_version_mock_function):
    #     get_version_mock_function.return_value = 100
    #     self.assertTrue(self.update.is_valid_system())
    #
    # @patch("aos.system.libs.util.Util.get_version")
    # def test_download_is_true(self, get_version_mock_function):
    #     get_version_mock_function.return_value = 100
    #
    #     self.update.is_valid_system()
    #
    #     self.assertTrue(self.update.download())
    #
    # @patch("aos.system.libs.util.Util.get_version")
    # def test_download_is_false_by_md5_false(self, get_version_mock_function):
    #     get_version_mock_function.return_value = 100
    #
    #     #set md5_hash false:
    #     self.data['md5_hash'] = 'ABCDEFGHIJKLMNOPQRSTUVWXYZPHUONGDEXOM'
    #
    #     self.update.is_valid_system()
    #
    #     self.update.download()
    #
    #     r = self.update.md5(self.update.zip_file) == self.data['md5_hash']
    #
    #     self.assertFalse(r)
    #
    # @patch("aos.system.libs.util.Util.get_version")
    # def test_download_is_true_by_md5_true(self, get_version_mock_function):
    #     get_version_mock_function.return_value = 100
    #
    #     self.update.is_valid_system()
    #
    #     self.update.download()
    #
    #     r = self.update.md5(self.update.zip_file) == self.data['md5_hash']
    #
    #     self.assertTrue(r)
    #
    #
    # @patch("aos.system.libs.util.Util.get_version")
    # def test_unzip_is_true(self, get_version_mock_function):
    #     get_version_mock_function.return_value = 100
    #     self.update.is_valid_system()
    #     self.update.download()
    #
    #     self.assertTrue(self.update.unzip())
    #
    # @patch("aos.system.libs.util.Util.get_version")
    # @patch("aos.ability.firmware_update.update.Update.reboot")
    # def test_config_is_true(self, reboot_bock, get_version_mock_function):
    #     reboot_bock.return_value = None
    #     get_version_mock_function.return_value = 100
    #
    #     self.update.is_valid_system()
    #     self.update.download()
    #
    #     self.assertTrue(self.update.unzip())
    #
    #     self.update.update_config_and_reboot()
    #
    #     from aos.system.libs.util import Util
    #     r = Util.get_version_info()['version'] == self.data['version']
    #
    #     self.assertTrue(r)
    #
    # @patch("aos.system.libs.util.Util.get_version")
    # def test_install_pip(self, get_version_mock_function):
    #     get_version_mock_function.return_value = 100
    #     from aos.ability.firmware_update.pip_install import Pip
    #     self.assertTrue(Pip.update())
    #
    # @patch("aos.system.libs.util.Util.get_version")
    # def test_install_deb(self, get_version_mock_function):
    #     get_version_mock_function.return_value = 100
    #     from aos.ability.firmware_update.deb_install import Deb
    #     self.assertTrue(Deb.update())
    #
    # @patch("aos.system.libs.util.Util.get_version")
    # def test_install_apt(self, get_version_mock_function):
    #     get_version_mock_function.return_value = 100
    #     from aos.ability.firmware_update.apt_install import APT
    #     self.assertTrue(APT.update())



    @patch("aos.ability.firmware_update.update_online.UpdateOnline.reboot")
    @patch("aos.ability.firmware_update.update_online.UpdateOnline.send_status")
    @patch("aos.system.libs.util.Util.get_version")
    def test_setup_full(self, get_version_mock_function, send_status, reboot_bock):
        get_version_mock_function.return_value = 100
        send_status.return_value = None
        reboot_bock.return_value = None

        if self.data is None:
            self.assertTrue(True)
        else:
            sleep(3)
            r = self.update.run()
            print "r=>", r
            self.assertTrue(r)

if __name__ == '__main__':
    unittest.main()

