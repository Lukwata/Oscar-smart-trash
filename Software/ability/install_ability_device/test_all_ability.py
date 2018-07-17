import unittest

from mock import patch

from aos.ability.install_ability_device.install_app import InstallUpdateAbility


class TestAllAbility(unittest.TestCase):

    def setUp(self):
        pass

    @patch("aos.ability.alarm.main.output")
    def test_download_install_run_alarm(self, output_mock_function):
        output_mock_function.output = None
        print "installing alarm ..."
        data = {
              "action" : "add",
              "app" : "alarm",
              "application_file" : "main.py",
              "is_service" : 1,
              "link" : "http://robotbase-cloud.s3.amazonaws.com/static/upload_apps/alarm_1.0_608_87.zip",
              "md5_hash" : "4b50ad6d75ebf80384d4c25c183a1c23",
              "version" : "10.0.0"
            }
        self.install_app = InstallUpdateAbility(data)

        print "test install_app ..."
        self.assertTrue(self.install_app.is_valid_data)

        self.assertTrue(self.install_app.is_valid_ability() and self.install_app.action == 'add')

        print "test download app success ..."
        self.assertTrue(self.install_app.download())

        print "test unzip app success ..."
        self.assertTrue(self.install_app.unzip())

        print "test update_config app success ..."
        self.assertTrue(self.install_app.update_config())

        from aos.system.configs.channel import BASE_APP
        app_path_config = BASE_APP + self.install_app.app_name + "/config.json"

        import os
        self.assertTrue(os.path.isfile(app_path_config))

        from aos.system.libs.util import Util
        version = Util.read_file(app_path_config)['version']

        print "test compare version: ", version, self.install_app.version

        self.assertTrue(version == self.install_app.version)

        print "remove app to run full test"
        try:
            import os
            if os.path.isdir(self.install_app.app_base_dir):
                import shutil
                shutil.rmtree(self.install_app.app_base_dir)
        except:
            pass

        print "full test install alarm ..."
        self.assertTrue(self.install_app.run())
        print "download and install alarm successful!"

        print "testing alarm ..."

        from aos.ability.alarm.main import read_time_alarm, read_timer, set_timer, set_alarm

        time_json = {"hour": 4, "min": 0, "p": ""}
        str = read_time_alarm(time_json)
        print str
        # self.assertTrue(str is not None)

        time_json = {"hour": 12, "min": 0, "p": "a.m"}
        str = read_time_alarm(time_json)
        print str
        # self.assertTrue(str is not None)

        str = read_timer(time_json)
        print str
        # self.assertTrue(str is not None)

        print "test set alarm:"
        params = {'mount_of_min': '1', 'mount_of_hour': '',
                  'time': '{"status": "1","time": "8","hour": "13","min": "40","p": ""}'}

        # self.assertTrue(set_timer(params, ""))

        print "test set alarm:"
        # self.assertTrue(set_alarm(params, ""))

    def test_download_install_run_spotify(self):
        print "testing spotify ..."
        import os
        from aos.ability.spotifys.Spotifys import Spotifys
        current_path = os.path.dirname(os.path.abspath(__file__))
        spotify_app = Spotifys("/home/travis/aos/ability/spotifys/spotify_appkey.key")
        print "test check login true ..."
        is_login = spotify_app.login("baohoanyc", 'bao12345')
        self.assertTrue(is_login)

    def test_download_install_run_uber(self):

        print "installing uber ..."
        self.data = {
              "action" : "add",
              "app" : "uber",
              "application_file" : "main.py",
              "is_service" : 1,
              "link" : "http://robotbase-cloud.s3.amazonaws.com/static/upload_apps/uber_1.1_608_92.zip",
              "md5_hash" : "8630ce7272117da8ea7695f1c8ea70f3",
              "version" : "10.0.0"
            }
        self.install_app = InstallUpdateAbility(self.data)
        self.assertTrue(self.install_app.run())
        print "download and install uber successful!"

        print "testing uber ..."
        print "request an uber"

        from aos.ability.uber.uber import Uber
        token = 'KA.eyJ2ZXJzaW9uIjoyLCJpZCI6Ikl5QnJCbWJjU3pTMWJlSjdKVEUyYUE9PSIsImV4cGlyZXNfYXQiOjE0OTc1ODcwMDYsInBpcGVsaW5lX2tleV9pZCI6Ik1RPT0iLCJwaXBlbGluZV9pZCI6MX0.Mm60JtxAalUik2V3sB9o5fnU27nWMycRSQ1FZh1PhBw'
        rf = "MA.CAESED4iPH2qNk4csIKXuBB1bdAiATEoATIBMQ.hvRny3eWYXDIYVVIsgySZgFyJ6LaNcrKynuQYu0TXfg.NJoM9SgYuxHDrwEmxyYbuvnT7lmdB36MdoeEj5_tnFY"

        app = Uber(sanbox=True)
        app.set_token(token=token)
        app.set_refresh_token(refresh_token=rf)

        print "get request current if exist"
        result = app.get_requests_current()
        if result is not False:
            request_id = result['request_id']
            print "status >> " + result['status']
            print "remove request_id:"
            self.assertTrue(app.delete_request_car(request_id))

        result = app.request_car(start_latitude=10.800116, start_longitude=106.652385)
        self.assertTrue(result is not False)

        request_id = result['request_id']
        print "request_id current >> " + result['request_id']
        print "status current >> " + result['status']

        print "test get info request"
        info = app.get_request(request_id)
        self.assertTrue(info is not False)

        print "status from info >>", info['status']
        print "request_id from info >> " + result['request_id']

        self.assertTrue(info['request_id'] == request_id)

        print "remove request_id:"
        self.assertTrue(app.delete_request_car(request_id))

    def tearDown(self):
        try:
            import os
            if os.path.isdir(self.install_app.app_base_dir):
                import shutil
                shutil.rmtree(self.install_app.app_base_dir)
        except:
            pass

