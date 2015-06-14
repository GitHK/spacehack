# -*- coding: utf-8 -*-
import APIAccessor
import argparse
from constants import ALARMED_DEVICE, ERROR_MOCK_FILE
from device_data_builder import build_device_list,  DeviceNetwork
import time
from device_interface import RealDeviceInterfaceThread, generate_real_device_event


device_network = DeviceNetwork(build_device_list())
#RealDeviceInterfaceThread(device_network)

while True:
    data = raw_input("W (warining event) R (reset network) S (generate real device alarm)")
    if data.upper() == "W":
        device_network.set_alarm_status_and_warn_near_devices(ALARMED_DEVICE)
    if data.upper() == "R":
        device_network.reset_network_status_to_normal()

    if data.upper() == "S":
        generate_real_device_event(ERROR_MOCK_FILE)

    device_network.print_network_status()