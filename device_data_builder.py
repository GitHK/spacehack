# -*- coding: utf-8 -*-
import os

import random
import time
import threading
import uuid
from hashlib import sha256
from math import sin, cos, sqrt, atan2, radians
import APIAccessor
from constants import STATUS, REAL_DEVICE_INDEX, REAL_DEVICE_IP, OK_MOCK_FILE
from device_interface import remove_real_device_event


device_positions = [(45.057652, 7.711078),
                    (45.057652, 7.707602),
                    (45.057652, 7.704126),
                    (45.057652, 7.700649),
                    (45.055670, 7.711344),
                    (45.055483, 7.707952),
                    (45.055296, 7.704560),
                    (45.055109, 7.701168),
                    (45.053688, 7.711609),
                    (45.053314, 7.708301),
                    (45.052941, 7.704994),
                    (45.052567, 7.701686),
                    (45.051706, 7.711875),
                    (45.051146, 7.708651),
                    (45.050585, 7.705428),
                    (45.050024, 7.702204)]

# device_positions[10] #real device id



def buid_device(position):
    return dict(
        latitude=position[0],
        longitude=position[1],
        status=STATUS[0],
        acceleration_x=random.uniform(0, 100),
        acceleration_y=random.uniform(0, 100),
        tdr=random.uniform(0, 50),
        tilt=random.uniform(0, 180),
        name=sha256(uuid.uuid1().hex).hexdigest()
    )


def build_device_from_file(data, status, acceleration_x, acceleration_y, tdr, name):
    return dict(
        latitude=device_positions[REAL_DEVICE_INDEX][0],
        longitude=device_positions[REAL_DEVICE_INDEX][1],
        status=status,
        acceleration_x=acceleration_x,
        acceleration_y=acceleration_y,
        tdr=tdr,
        name=name
    )


def build_device_list():
    devices = []
    for position in device_positions[:8] + device_positions[8 + 1:]:
        device = buid_device(position)
        APIAccessor.new_or_update_device(
            device['latitude'],
            device['longitude'],
            device['status'],
            device['acceleration_x'],
            device['acceleration_y'],
            device['tdr'],
            device['tilt'],
            device['name'])
        devices.append(device)
    return devices


def get_real_device_position():
    return device_positions[REAL_DEVICE_INDEX]


EARTH_RADIUS = 6373.0


class DeviceNetwork:
    def __init__(self, devices):
        self.devices = devices


    def distance_between_nodes(self, first, second):
        lat1 = radians(first['latitude'])
        lon1 = radians(first['longitude'])
        lat2 = radians(second['latitude'])
        lon2 = radians(second['longitude'])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return EARTH_RADIUS * c * 1000


    def get_nodes_in_range(self, node_index, range):
        result = []
        for list_node in self.devices:
            if self.distance_between_nodes(self.devices[node_index], list_node) <= range:
                result.append(list_node)
        return result

    def print_network_status(self):
        print [dev['status'] for dev in self.devices]

    def set_real_device_status(self, command_name):
        os.system('sshpass -p "intrepid" ssh root@{ip} touch ~/{command}'.format(ip=REAL_DEVICE_IP,command=command_name))

    def set_status_in_node(self, node_index, status_index):
        self.devices[node_index]['status'] = STATUS[status_index]
        APIAccessor.update_status(self.devices[node_index]['name'], self.devices[node_index]['status'])

    def set_alarm_status_and_warn_near_devices(self, alarmed_device):
        for device in self.get_nodes_in_range(alarmed_device, 400):
            self.set_status_in_node(self.devices.index(device), 1)
            if self.devices.index(device) == REAL_DEVICE_INDEX:
                remove_real_device_event(OK_MOCK_FILE)
                self.set_real_device_status("alert_on")
        self.set_status_in_node(alarmed_device, 2)

    def reset_network_status_to_normal(self):
        for device in self.devices:
            self.set_status_in_node(self.devices.index(device), 0)
            if self.devices.index(device) == REAL_DEVICE_INDEX:
                self.set_real_device_status("alert_off")