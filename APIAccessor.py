# -*- coding: utf-8 -*-
from Queue import Queue
from threading import Thread
import threading
import time
import requests

BASE_URL = "http://cryptic-bayou-3624.herokuapp.com/api/"


def _post_request(request, parameters):
    ExecuteConnectionOnThread(BASE_URL + request, parameters)
    #print requests.post(BASE_URL + request, parameters).text


def new_or_update_device(latitude, longitude, status, accelerometer_x, accelerometer_y, tdr, tilt, name):
    parameters = dict(
        latitude=latitude,
        longitude=longitude,
        status=status,
        accelerometer_x=accelerometer_x,
        accelerometer_y=accelerometer_y,
        tdr=tdr,
        tilt=tilt,
        name=name
    )
    return _post_request('new_or_update_device', parameters)


def update_status(name, status):
    parameters = dict(name=name, status=status)
    return _post_request('update_status', parameters)


class ExecuteConnectionOnThread(object):
    def __init__(self, url, parameters, interval=1):
        self.interval = interval
        self.url = url
        self.parameters = parameters

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        print requests.post(self.url, self.parameters).text