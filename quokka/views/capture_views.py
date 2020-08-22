from flask import request

from quokka import app
from quokka.controller.utils import log_console
from quokka.models.apis import get_device


@app.route("/capture/register", methods=["GET", "POST"])
def capture_register():

    registration_info = request.get_json()
    if not registration_info:
        return "Must provide registration information in JSON body", 404
    if "serial" not in registration_info:
        return "Must provide 'serial' in registration information", 404
    if "name" not in registration_info:
        return "Must provide 'name' in registration information", 404

    result, device = get_device(device_name=registration_info["name"])
    if result != "success":
        return "Unknown device name in registration information", 404
    if registration_info["serial"] != device["serial"]:
        return "Serial number in registration information does not match device serial", 404

    log_console(
        f"Received registration request from {registration_info['name']}, serial no: {registration_info['serial']}"
    )

    return {}, 200


@app.route("/capture/store", methods=["POST"])
def capture_store():

    capture_info = request.get_json()
    if not capture_info:
        return "Must provide capture information in JSON body", 404
    if "serial" not in capture_info:
        return "Must provide 'serial' in capture information", 404
    if "name" not in capture_info:
        return "Must provide 'name' in capture information", 404
    if "packets" not in capture_info:
        return "Must include 'packets' in capture information", 404

    # result, device = get_device(device_name=capture_info["name"])
    # if result != "success":
    #     return "Unknown device name in capture information", 404
    # if capture_info["serial"] != device["serial"]:
    #     return "Serial number in capture information does not match device serial", 404

    for packet in capture_info["packets"]:
        print(f"Received captured packet from {capture_info['name']}: {packet}")

    log_console(
        f"Received capture store request from {capture_info['name']}, info={capture_info}"
    )

    return {}, 200
