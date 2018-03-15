#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# communication with the local lametric
#
import requests
import json
import time

""" this parameter contains a lametric password """
from settings import lametric_pass

headers = {'Content-Type': 'application/json'}
URL = 'http://192.168.1.155:8080/api/v2/{}'


def send_notification_with_cat_sound(text):
    """ sending a notification to lametric with a cat sound """
    # TODO setup a correct timing between the API calls
    volume = get_volume()
    set_volume(100)
    time.sleep(1)
    send_notification(text)
    time.sleep(5)
    set_volume(volume)


def send_notification(text):
    data = {'model': {'frames': [{'text': text}], 'sound': {'category': 'notifications', 'id': 'cat', 'repeat': 1}}}
    requests.post(url=URL.format('device/notifications'), data=json.dumps(data), auth=('dev', lametric_pass),
                  headers=headers)


def set_timer(duration):
    # TODO implement
    pass


def get_volume():
    response = requests.get(url=URL.format('device/audio'), auth=('dev', lametric_pass))
    return response.json().get('volume')


def set_volume(volume):
    data = {'volume': volume}
    requests.put(url=URL.format('device/audio'), data=json.dumps(data), auth=('dev', lametric_pass),
                 headers=headers)
