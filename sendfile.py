# -*- coding: utf-8 -*-
import os
import urllib

FILENAME = "temperature"

BASE_URL = "http://cryptic-bayou-3624.herokuapp.com/api/"

DEVICE_IP = "192.168.1.7"

with open(FILENAME) as f:
    lines = f.readlines()
    parameters = {}
    for line in lines:
        values = line.strip('\n').split(',')
        parameters[values[0]] = values[1]
    parameters["ip_address"] = DEVICE_IP
    url = BASE_URL + "send_data?"+urllib.urlencode(parameters)
    print url
    os.system("curl " + url)
