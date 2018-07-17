from aos.ability.install_ability_device.install_app import InstallUpdateAbility
from aos.system.sdk.python.receive import receive_json
from aos.system.sdk.python.send import send_json

from aos.system.configs.channel import DEVICE_TYPE
from aos.system.libs.t2s import T2S


def output(status, action, source, sensor):
    data = {"status": status, "message": "", "sensor": sensor, "type": sensor, "action": action}
    s = {"source": source, "type": "install_result", "data": data, "protocol": ""}
    send_json(s)

    notify = ""

    if status:
        if action == "add":
            notify = "The %s app has been installed." % sensor
        if action == "remove":
            notify = "The %s app has been removed." % sensor
    else:
        notify = "Installation failed"
    if notify:
        if DEVICE_TYPE in ["SMART_DESK", "PERSONAL_ROBOT"]:
            T2S.run(notify)

        if DEVICE_TYPE in ["SMART_DESK_3"]:
            s = {"source": "", "type": "stop_an_ability", "data": {"ability_name": "waiting_update"}, "protocol": ""}
            send_json(s)
            sensor = ((str(sensor)).replace("_", " ")).title()
            sub_data = {"message": notify, "status": 1,
                        "data": {"desc": notify, "type": "non-blocking", "timeout": "2", "title": sensor}}
            data = {"action": "notification", "data": sub_data, "from": "install_ability_device"}
            sensor = {"source": "", "data": data, "type": "personal_assistant"}
            # send_json(sensor)


def run(data, source):
    install_update_app = InstallUpdateAbility(data, source)
    result = install_update_app.run()
    output(result, install_update_app.action, install_update_app.source, install_update_app.app_name)

if __name__ == '__main__':
    json_data = receive_json()

    data = json_data['data']
    source = json_data['source']

    # data = {"action": "add", "app":"smartthings", "version": "1.0.0", "is_service": 1, "application_file":"main.py", "link":"http://robotbasecloud-env-kq6xxhigdt.elasticbeanstalk.com/static/upload_apps/smartthings.zip"}
    # data ={"app": "alarm", "version": "1.1.12", "link": "https://s3.amazonaws.com/robotbase-cloud/static/upload_apps/alarm1.1.2.zip", "is_service": 0, "action": "add", "application_file": "main.py"}

    run(data, source)





