# -*- coding: utf-8 -*-
import os

import random
import time
import threading
from math import sin, cos, sqrt, atan2, radians

from constants import STATUS, REAL_DEVICE_INDEX, REAL_DEVICE_IP, OK_MOCK_FILE, ERROR_MOCK_FILE, ALARMED_DEVICE
from device_interface import remove_real_device_event, generate_real_device_event


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

device_names = [
    "Knife Running",
    "Lone Plastic",
    "Reborn Dagger",
    "Sleepy Emerald",
    "Timely Hammer",
    "Skilled Balcony",
    "Homeless Shower",
    "Aggressive Crayon",
    "Swift Clown",
    "Quality Barbaric Neutron",
    "Intrepid",
    "Needless Rocky Comic",
    "Subtle Coffin",
    "Rainbow Mustard",
    "Indigo Mercury,"
    "Tidy Canal",
    "Unique Lobster",
]

assert len(device_names) == len(device_positions)

# device_positions[10] #real device id



def buid_device(position, name):
    return dict(
        latitude=position[0],
        longitude=position[1],
        status=STATUS[0],
        acceleration_x=random.uniform(-0.1, 0.1),
        acceleration_y=random.uniform(-0.1, 0.1),
        tdr=random.uniform(0, 50),
        tilt=random.uniform(0, 180),
        name=name
    )



def build_device_list():
    devices = []

    for (name,position,index) in zip(device_names, device_positions, range(0,len(device_names))):
        device = buid_device(position, name)
        devices.append(device)
        import APIAccessor
        APIAccessor.new_or_update_device(
            device['latitude'],
            device['longitude'],
            device['status'],
            device['acceleration_x'],
            device['acceleration_y'],
            device['tdr'],
            device['tilt'],
            device['name'])
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
        os.system(
            'sshpass -p "intrepid" ssh root@{ip} touch {command} 2>/dev/null'.format(ip=REAL_DEVICE_IP,
                                                                                     command=command_name))

    def server_set_status_in_node_from_index(self, node_index, status_index):
        self.devices[node_index]['status'] = STATUS[status_index]
        import APIAccessor
        APIAccessor.update_status(self.devices[node_index]['name'], self.devices[node_index]['status'])

    def set_alarm_status_and_warn_near_devices(self, alarmed_device):
        for device in self.get_nodes_in_range(alarmed_device, 400):
            self.server_set_status_in_node_from_index(self.devices.index(device), 1)
            self.set_real_device_status("alert_on")

        self.server_set_status_in_node_from_index(self.devices.index(alarmed_device), 2)

    def reset_network_status_to_normal(self):
        for device in self.devices:
            self.server_set_status_in_node_from_index(self.devices.index(device), 0)
            if device == REAL_DEVICE_INDEX:
                remove_real_device_event(OK_MOCK_FILE)
                self.set_real_device_status("alert_off")