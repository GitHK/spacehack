# -*- coding: utf-8 -*-
import os

import time
import threading
import APIAccessor
from constants import FILENAME, REAL_DEVICE_IP, REAL_DEVICE_INDEX, STATUS


def get_parameters_from_file(filename):
    os.system('sshpass -p "intrepid" scp root@{ip}:{file} . 2>/dev/null'.format(ip=REAL_DEVICE_IP, file=filename))
    with open(filename) as f:
        lines = f.writelines()
        parameters = {}
        for line in lines:
            values = line.strip('\n').split(',')
            if len(values) == 2:
                parameters[values[0]] = values[1]
    return parameters


def _write_mock_file(data):
    filename = 'mock'
    with open(filename, 'w') as f:
        f.write(data)
        f.close()
        os.system('sshpass -p "intrepid" scp mock root@{ip}:mock 2>/dev/null'.format(ip=REAL_DEVICE_IP))


def generate_real_device_event(data):
    _write_mock_file(data)


def remove_real_device_event(data):
    _write_mock_file(data)


class RealDeviceInterfaceThread(object):
    def __init__(self, device_network, interval=1):
        self.interval = interval
        self.device_network = device_network
        self.last_status = None

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            parameters = get_parameters_from_file(FILENAME)
            if parameters == {}:
                time.sleep(self.interval)

            # Override data
            from device_data_builder import device_names, device_positions

            parameters['latitude'] = device_positions[REAL_DEVICE_INDEX][0]
            parameters['longitude'] = device_positions[REAL_DEVICE_INDEX][1]
            parameters['name'] = device_names[REAL_DEVICE_INDEX]

            APIAccessor.new_or_update_device(
                parameters['latitude'],
                parameters['longitude'],
                parameters['status'],
                parameters['accelerometer_x'],
                parameters['accelerometer_y'],
                parameters['tdr'],
                parameters['tilt'],
                parameters['name'])

            APIAccessor.update_status(parameters['name'], parameters['status'])

            current_status = parameters['status']

            if current_status == STATUS[2] and self.last_status != current_status:
                self.device_network.set_alarm_status_and_warn_near_devices(REAL_DEVICE_INDEX)
                print "status ALARMED"

            if current_status == STATUS[0] and self.last_status != current_status:
                self.device_network.reset_network_status_to_normal()
                print "status RUNNING"

            self.last_status = current_status
            time.sleep(self.interval)