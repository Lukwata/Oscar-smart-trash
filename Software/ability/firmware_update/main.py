from aos.ability.firmware_update.update_online import UpdateOnline
from aos.system.sdk.python.receive import receive_json
from aos.system.sdk.python.send import send_json
source = ""


def output(status):
    data = {"status": status, "message": ""}
    s = {"source": "", "type": "update_firmware_result", "data": data, "protocol": ""}
    send_json(s)


if __name__ == '__main__':
    json_data = receive_json()

    result = json_data['data']
    source = json_data['source']

    #for debug:
    # result = {"type": "update_system", "version": "1.0.0", "app": "system", "link": "https://s1-robotbase.s3.amazonaws.com/system/smartdesk3213.2.1_62.zip"}
    # source = ''
    # result = {"link": "https://s3.amazonaws.com/robotbase-cloud/system/PersonalRobot1.0.11.0.1_62.zip",
    #           "app": "PersonalRobot1.0.1", "version": "1.0.1", "type": "firmware_update"}

    # result = {"app": "system", "version": "1.0.5", "link": "https://s3.amazonaws.com/robotbase-cloud/system/firmware1.0.51.0.5_62.zip"}
    #
    #
    UpdateOnline(result, source=source).run()


