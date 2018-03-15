#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# fetching music from youtube
#
import subprocess
import pafy

from settings import bluetooth_audio

player = None


def download_and_play_youtube(video_id):
    """ download the audio for the given youtube video id """
    global player
    youtube_video = pafy.new(video_id)
    url = youtube_video.getbestaudio().url
    player = subprocess.Popen(['mplayer', '-ao', bluetooth_audio, '-volume', '50', url],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def stop_player():
    """ terminate the player """
    player.terminate()


def generate_search_qs(term):
    """ Return query string. """
    qs = {
        'q': term,
        'maxResults': 50,
        'safeSearch': "none",
        'order': 'relevance',
        'part': 'id,snippet',
        'type': 'video',
        'videoDuration': 'any',
        'key': 'AIzaSyCIM4EzNqi1in22f4Z3Ru3iYvLaY8tc3bo'
    }
    return qs


def search_and_play_video(term):
    """ search for the youtube video and play the first one """
    search_results = pafy.call_gdata('search', qs=generate_search_qs(term=term))
    video_id = search_results['items'][0]['id']['videoId']
    download_and_play_youtube(video_id)
