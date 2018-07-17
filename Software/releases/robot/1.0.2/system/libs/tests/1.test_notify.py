import unittest

from aos.system.libs.notify import Notify


class MyTestCase(unittest.TestCase):
    def test_play(self):
        self.assertEqual(True, Notify().run(notify_type=Notify.NotifyType.PLS_WAIT))

if __name__ == '__main__':
    unittest.main()
