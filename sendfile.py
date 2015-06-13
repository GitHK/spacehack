# -*- coding: utf-8 -*-
import os
import urllib

FILENAME = "temperature"

BASE_URL = "http://cryptic-bayou-3624.herokuapp.com/api/"

with open(FILENAME) as f:
    lines = f.readlines()
    parameters = {}
    for line in lines:
        values = line.strip('\n').split(',')
        parameters[values[0]] = values[1]
    url = BASE_URL + "send_data?"+urllib.urlencode(parameters)
    print url
    os.system("curl " + url)
