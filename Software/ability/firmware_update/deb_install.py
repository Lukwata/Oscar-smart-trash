import os

from aos.ability.firmware_update.util import Util, DEB_REQUIREMENT_FILE, FOLDER_DEB_TMP
from aos.system.configs.channel import FIRMWARE_UPDATE__TMP_PATH, CURRENT_PATH


REQUIREMENT_FIRMWARE_PATH_UPDATE = FIRMWARE_UPDATE__TMP_PATH + DEB_REQUIREMENT_FILE
REQUIREMENT_FIRMWARE_PATH_ROLLBACK = CURRENT_PATH + DEB_REQUIREMENT_FILE

URL = "https://s3.amazonaws.com/robotbase-cloud/deb-store/"

CMD_UPDATE_DEB = "mkdir -p %s && cd %s && wget -nc %s && sudo dpkg -i %s"
CMD_ROLLBACK_DEB = "echo %s && cd %s && echo %s && sudo dpkg -i %s"


# sudo dpkg -i {package_name} -> new install
# sudo dpkg -P {package_name} => remove
# dpkg -s <package> | grep Version  | grep -o '[0-9.]\+' -> get version
# a="$(dpkg-query -W -f=\'${Version}\' %s  2>&1)" res=$?; if [[ $res == 0 ]]; then echo $a; fi


class DebPackage():
    name = ''
    path = ''
    version = ''
    file_name = ''
    url = ''


class Deb(object):

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
    def get_new_version(deb_file):
        try:
            cmd_str = "dpkg -I %s | grep Version | awk '{print $2}'" % (deb_file)
            output_str = Util.cmd(cmd_str)
            if output_str:
                return output_str.rstrip()
        except Exception as e:
            print 'error get version ->' + str(e)
        return None

    @staticmethod
    def convert_to_package(str_line):
        try:
            deb = DebPackage()
            deb_package = str_line.rstrip().split()
            if deb_package and len(deb_package) >= 3:
                deb.name = deb_package[0]
                deb.file_name = deb_package[1]
                deb.version = deb_package[2]

                deb.path = FOLDER_DEB_TMP + deb.file_name
                deb.url = URL + deb.file_name
                return deb
        except Exception as e:
            print 'error convert deb object -> ' + str(e)

        return None

    @staticmethod
    def remove_package(package):
        Util.cmd('sudo dpkg -P %s' % (package))
        return not Deb.get_current_version(package)

    @staticmethod
    def update():
        cmd = CMD_UPDATE_DEB
        return Deb.install(cmd, REQUIREMENT_FIRMWARE_PATH_UPDATE)

    @staticmethod
    def rollback():
        print "Rollback deb"

        cmd = CMD_ROLLBACK_DEB
        return Deb.install(cmd, REQUIREMENT_FIRMWARE_PATH_ROLLBACK)

    @staticmethod
    def install(cmd, requirement_path):

        if not os.path.exists(requirement_path):
            return True

        status = True

        try:

            with open(requirement_path) as file_requirement:
                for line in file_requirement:

                    deb_object = Deb.convert_to_package(line)
                    if deb_object:
                        # Kiem tra version hien tai co khac voi version can cai ko?
                        current_version = Deb.get_current_version(deb_object.name)
                        print "before install:"
                        print 'current version of ' + deb_object.name + '=>', current_version
                        print 'new version of ' + deb_object.name + '=>', deb_object.version
                        if current_version is None or current_version != deb_object.version:
                            Util.cmd(cmd % (FOLDER_DEB_TMP, FOLDER_DEB_TMP, deb_object.url, deb_object.file_name))
                            # check install success:
                            print "affer install:"
                            current_version = Deb.get_current_version(deb_object.name)
                            new_version = Deb.get_new_version(deb_object.path)
                            print 'current version of ' + deb_object.name + '=>', current_version
                            print 'new version of ' + deb_object.name + '=>', deb_object.version, new_version
                            if os.path.isfile(deb_object.path) and current_version == new_version:
                                print "install %s success" % (deb_object.file_name)
                            else:
                                status = False
                                print "install %s failed" % (deb_object.file_name)
                                break
                    else:
                        status = False
                        print "detect deb object at line: %s is faild" % (line)

                file_requirement.close()

        except Exception as e:
            status = False
            print "error install => " + str(e)

        return status