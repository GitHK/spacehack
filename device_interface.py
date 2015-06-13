# -*- coding: utf-8 -*-
import os

import time
import threading
import APIAccessor
from device_data_builder import REAL_DEVICE_INDEX, STATUS

FILENAME = "output.csv"

REAL_DEVICE_IP = "192.168.1.105"

ERROR_FILE_DATA = """acceleration_y 45.460341
acceleration_x 17.866871
tdr 17.957764
tilt 59.170946
"""

OK_MOCK_FILE = """
acceleration_y 45.460341
acceleration_x 17.866871
tdr 17.957764
tilt 59.170946
"""


def get_parameters_from_file(filename):
    os.system('sshpass -p "intrepid" scp root@{ip}:~/{file} .'.format(ip=REAL_DEVICE_IP,file=filename))
    with open(filename) as f:
        lines = f.readlines()
        parameters = {}
        for line in lines:
            values = line.strip('\n').split(',')
            parameters[values[0]] = values[1]
    return parameters


def _write_mock_file(data):
    os.system('sshpass -p "intrepid" ssh root@{ip} echo {content} > ~/mock'.format(ip=REAL_DEVICE_IP,content=data))

def generate_real_device_event(data):
    _write_mock_file(data)

def remove_real_device_event(data):
    _write_mock_file(data)


class RealDeviceInterfaceThread(object):
    def __init__(self, device_network, interval=1):
        self.interval = interval
        self.device_network = device_network

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            parameters = get_parameters_from_file(FILENAME)
            APIAccessor.new_or_update_device(
                parameters['latitude'],
                parameters['longitude'],
                parameters['status'],
                parameters['acceleration_x'],
                parameters['acceleration_y'],
                parameters['tdr'],
                parameters['tilt'],
                parameters['name'])

            APIAccessor.update_status(parameters['name'], parameters['status'])

            if parameters['status'] == STATUS[2]:
                self.device_network.set_alarm_status_and_warn_near_devices(REAL_DEVICE_INDEX)

            if parameters['status'] == STATUS[0]:
                self.device_network.reset_network_status_to_normal()

            time.sleep(self.interval)