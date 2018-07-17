import os


from aos.ability.firmware_update.util import Util, APT_REQUIREMENT_FILE
from aos.system.configs.channel import FIRMWARE_UPDATE__TMP_PATH, CURRENT_PATH


REQUIREMENT_FIRMWARE_PATH_UPDATE = FIRMWARE_UPDATE__TMP_PATH + APT_REQUIREMENT_FILE
REQUIREMENT_FIRMWARE_PATH_ROLLBACK = CURRENT_PATH + APT_REQUIREMENT_FILE


CMD_INSTALL_APT = "sudo apt-get install -y %s"


class PipPackage():
    name = ''
    version = None
    package_name = ''


class APT(object):

    # check need run install:
    @staticmethod
    def check_is_new_requirement():
        try:
            if os.path.exists(REQUIREMENT_FIRMWARE_PATH_ROLLBACK) and os.path.exists(REQUIREMENT_FIRMWARE_PATH_UPDATE):
                import filecmp
                return not filecmp.cmp(REQUIREMENT_FIRMWARE_PATH_ROLLBACK, REQUIREMENT_FIRMWARE_PATH_UPDATE)
        except Exception as e:
            print str(e)

        return True

    @staticmethod
    def get_current_version(package):
        try:
            cmd_str = 'get_version_pkg %s' % package
            output_str = Util.cmd(cmd_str)
            if output_str:
                return output_str.rstrip()
        except Exception as e:
            print 'error get version ->' + str(e)
        return None

    @staticmethod
    def convert_to_package(str_line):
        try:
            apt = PipPackage()
            apt.package_name = str_line.rstrip()
            apt_package = apt.package_name.split("=")
            if apt_package and len(apt_package) > 0:
                apt.name = apt_package[0]
                if len(apt_package) >= 2:
                    apt.version = apt_package[1]
                return apt

        except Exception as e:
            print 'error convert apt object -> ' + str(e)

        return None

    @staticmethod
    def remove_package(package):
        Util.cmd('sudo apt-get remove %s' % (package))
        return True

    @staticmethod
    def update():
        return APT.install(REQUIREMENT_FIRMWARE_PATH_UPDATE)

    @staticmethod
    def rollback():
        print "Rollback apt"
        return APT.install(REQUIREMENT_FIRMWARE_PATH_ROLLBACK)

    @staticmethod
    def install(requirement_path):

        if not os.path.exists(requirement_path):
            return True

        status = True

        try:

            with open(requirement_path) as file_requirement:
                for line in file_requirement:

                    apt_object = APT.convert_to_package(line)
                    if apt_object:
                        current_version = APT.get_current_version(apt_object.name)
                        if current_version is None or current_version != apt_object.version:
                            Util.cmd(CMD_INSTALL_APT % (apt_object.package_name))
                            # check install success:
                            if (apt_object.version is None and APT.get_current_version(apt_object.name) is not None) or (APT.get_current_version(apt_object.name) == apt_object.version):
                                print "install %s success" % (apt_object.package_name)
                            else:
                                status = False
                                print "install %s failed" % (apt_object.package_name)
                                break
                    else:
                        status = False
                        print "detect apt object at line: %s is faild" % (line)

                file_requirement.close()

        except Exception as e:
            status = False
            print "error install => " + str(e)

        return status

