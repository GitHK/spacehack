# -*- coding: utf-8 -*-
import threading
import time
import requests



def _post_request(request, parameters):
    from run import BASE_URL
    ExecuteConnectionOnThread(BASE_URL + request, parameters)
    #print request, requests.post(BASE_URL + request, parameters).text


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
        print self.url, requests.post(self.url, self.parameters).text