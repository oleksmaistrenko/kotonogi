#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pafy
import subprocess

player = None


def download_and_play_youtube(video_id):
    global player
    youtube_video = pafy.new(video_id)
    filename = youtube_video.getbestaudio().download(quiet=True)
    player = subprocess.Popen(['mplayer', '-ao', 'pulse::bluez_sink.A0_2C_36_77_25_96.a2dp_sink', '-volume', '50', filename],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def stop_player():
    player.terminate()
