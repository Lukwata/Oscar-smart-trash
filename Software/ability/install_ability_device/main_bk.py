import argparse
import os
import json
import urllib2
import zipfile
import shutil

from aos.system.sdk.python.send import send_json

from aos.system.configs.channel import BASE_APP
from aos.system.libs.util import Util

sensor = None
type = 0
action = ""


def output(status):
    data = {"status": status, "message": "", "sensor": sensor, "type": type, "action": action}
    s = {"source": "", "type": "install_result", "data": json.dumps(data), "protocol": ""}
    print(json.dumps(s))
    send_json(json.dumps(s))


def download_ability(json_ability):

    global sensor

    status = False

    app_name = json_ability["app"]
    sensor = app_name

    app_base_dir = BASE_APP + app_name
    if not os.path.isdir(app_base_dir):
        os.mkdir(app_base_dir)
        print "Created app \"%s\" base folder ..." % app_name
    link = json_ability['link']
    try:
        print 'Downloading ' + link
        path_to_zip_file = app_base_dir + "/" + os.path.basename(json_ability['link'])
        f = urllib2.urlopen(link)
        buf = 16 * 1024
        with open(path_to_zip_file, 'wb') as line:
            while True:
                chunk = f.read(buf)
                if not chunk:
                    break
                line.write(chunk)

        if unzip(path_to_zip_file, app_base_dir):

            print('installing requirement.txt ...')
            try:
                if os.path.exists(app_base_dir + "/requirements.txt"):
                    Util.cmd("sudo pip install -r "+ app_base_dir + "/requirements.txt")
            except:
                pass

            app_path_config = BASE_APP + app_name + "/config.json"
            print ("creating config app "+app_path_config+"...")
            config_data = {"application_file": json_ability['application_file'], 'is_service': json_ability['is_service'], 'version': json_ability['version'], "type": 0}

            with open(app_path_config, 'w') as outfile:
                json.dump(config_data, outfile)

            status = True

    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code, link
    except urllib2.URLError, e:
        print "URL Error:", e.reason, link
    except Exception as e:
        print(str(e))

    return status


def unzip(source_path, dest_path):
    status = False
    try:
        if not zipfile.is_zipfile(source_path):
            print "Application zip file is invalid: %s" % source_path
            return False

        z = zipfile.ZipFile(source_path)
        c = sensor.lower() + "/"
        print "Extracting folder \"%s\" to destination folder \"%s\"" % (c, dest_path)
        for name in z.namelist():
            print name
            if name.lower().find(c) == 0 and name != c:
                sub = name[len(c):]
                if name.endswith("/"):
                    new_dir = os.path.join(dest_path, sub)
                    if not os.path.exists(new_dir):
                        os.mkdir(new_dir)
                    continue
                source = z.open(name)
                target = file(os.path.join(dest_path, sub), "wb")
                with source, target:
                    shutil.copyfileobj(source, target)
                status = True

        print "removing zip...."
        os.unlink(source_path)
        z.close()

    except zipfile.BadZipfile:
        print "error: bad zip file"
    except Exception as e:
        print "error: ", str(e)
    return status


def is_valid_ability(json_ability):
    app = json_ability['app']
    app_base_dir = BASE_APP + app

    app_config = Util.read_app_config(app_base_dir)

    if app_config:
        version = json_ability['version']
        try:
            if version != app_config['version']:
                result = True
            else:
                result = False
        except Exception as e:
            print e.message
            result = False
    else:
        result = True

    return result


def remove_ability(app):

    app_name = app["app"]

    global sensor
    sensor = app_name

    app_dir = BASE_APP + app_name
    if os.path.isdir(app_dir):
        print "Removing app \"%s\" at \"%s\" ..." % (app_name, app_dir)
        shutil.rmtree(app_dir)
        result = True
        print "Completed !"
    else:
        result = True

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '-data', help='data')
    parser.add_argument('-s', '-source', help='source')
    parser.add_argument('-p', '-protocol', help='protocol', required=False)

    args = parser.parse_args()
    data = json.loads(args.d)

    # source = ""
    # data = {"action": "add", "app":"smartthings", "version": "1.0.0", "is_service": 1, "application_file":"main.py", "link":"http://robotbasecloud-env-kq6xxhigdt.elasticbeanstalk.com/static/upload_apps/smartthings.zip"}
    # data ={"app": "alarm", "version": "1.1.12", "link": "https://s3.amazonaws.com/robotbase-cloud/static/upload_apps/alarm1.1.2.zip", "is_service": 0, "action": "add", "application_file": "main.py"}

    action = data['action']

    if action == 'add':
        if is_valid_ability(data):
            if download_ability(data):
                output(True)
            else:
                output(False)
        else:
            output(False)
    elif action == 'remove':
        remove_ability(data)
        output(True)



