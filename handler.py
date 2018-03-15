#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
from devices import lametric, audio


def play_music(track):
    audio.search_and_play_video(track)
    return 'lets play \'{}\''.format(track)


def stop_music(_):
    audio.stop_player()
    return 'silence'


def send_message(message):
    lametric.send_notification(message)
    return 'send lametric message \'{}\''.format(message)


def set_timer(duration):
    lametric.set_timer(duration)
    return 'set lametric timer \'{}\''.format(duration)


def handle(intent, value):
    """ handle the messages for different intents """
    this_mod = sys.modules[__name__]
    func = getattr(this_mod, intent)
    return func(value)
