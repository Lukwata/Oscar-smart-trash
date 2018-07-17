import os

import shutil

from aos.ability.firmware_update.rollbak_offline import RollbackOffline
from aos.ability.firmware_update.util import Util
from aos.system.configs.channel import FIRMWARE_UPDATE__TMP_PATH, CURRENT_PATH

FIRMWARE_UPDATE__TMP_PATH_SYSTEM = FIRMWARE_UPDATE__TMP_PATH + 'system'
# flow: https://code2flow.com/KpyKnL

rollback = RollbackOffline()

if rollback.check_rollback:
    rollback.run()
    if os.path.exists(FIRMWARE_UPDATE__TMP_PATH_SYSTEM):
        shutil.rmtree(FIRMWARE_UPDATE__TMP_PATH)
else:

    if os.path.exists(FIRMWARE_UPDATE__TMP_PATH_SYSTEM):
        # print "moving new system ..."
        # todo: co nen check thoi luong PIN o day, de dam bao lenh move luon success?
        cmd = 'mv --backup=numbered %s %s' % (FIRMWARE_UPDATE__TMP_PATH_SYSTEM, CURRENT_PATH)
        Util.cmd(cmd)
    #     if not os.path.exists(FIRMWARE_UPDATE__TMP_PATH_SYSTEM):
    #         print "moving successful!"
    #     else:
    #         print "moving fail!"
    # else:
    #     print "No update"
    #



