
from os import path


def post_file(aos, filepath):
    url = aos.api.url + "/devpi/packages"
    data = open(filepath, 'rb').read()

    headers = dict()
    headers["Filename"] = path.basename(filepath)
    headers["Content-Type"] = "application/octet-stream"

    return aos.api.requests.post(url, data=data, headers=headers)


def launch_remote_device_agent(aos, username, password, host,
                               platform, location=None, device_id=None):
    api = aos.api.requests
    url = aos.api.url + "/systems/offbox"
    launch_data = {
        "user_config": {
            "device_id": device_id,
            "admin_state": "normal",
            "platform": platform,
            "location": location or "demo",
            "management_ip": host,
            "username": username,
            "password": password
        }
    }

    return api.post(url, json=launch_data)


def test_1(aos):
    return launch_remote_device_agent(
        aos, platform='eos',
        device_id='MOCKCORE1MAHWAH',
        username="mock_data/core1-mahwah", password='admin', host='1.1.1.1')
