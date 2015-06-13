# -*- coding: utf-8 -*-
import os
import urllib

BASE_URL = "http://cryptic-bayou-3624.herokuapp.com/api/"


def _post_request(request, parameters):
    url = BASE_URL + request + "?" + urllib.urlencode(parameters)
    #return os.system("curl " + url)


def set_data(parameters):
    return _post_request('set_data', parameters)


def new_or_update_device(latitude, longitude, status, acceleration_x, acceleration_y, tdr, tilt, name):
    parameters = dict(
        latitude=latitude,
        longitude=longitude,
        status=status,
        acceleration_x=acceleration_x,
        acceleration_y=acceleration_y,
        tdr=tdr,
        tilt=tilt,
        name=name
    )
    return _post_request('new_or_update_device', parameters)


def update_status(name, status):
    parameters = dict(name=name,status=status)
    return _post_request('update_status', parameters)