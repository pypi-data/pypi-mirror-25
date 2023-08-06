# -*-: coding utf-8 -*-
""" Sonos skill for Snips. """

import datetime
import soco

from soco.music_services import MusicService
from soco.alarms import Alarm
from random import shuffle
from sonos_radio.handler.spotify.spotify import SpotifyClient

MAX_VOLUME = 70
GAIN = 4
ALARM_DURATION = datetime.time(second=20) # in secondes

MAP_TO_INT = {
    None: 1,
    'un': 1,
    'deux': 2,
    'trois': 3,
    'quatre': 4,
    'cinq': 5,
    'six': 6,
    'sept': 7,
    'huit': 8,
    'neuf': 9,
    'dix': 10
}

class SnipsSonos:
    """ Sonos skill for Snips. """
    
    def __init__(self, spotify_client_id, spotify_client_secret, spotify_refresh_token):
        # find the device
        self.device = list(soco.discover())[0]
        self.tunein = MusicService('TuneIn')
        self.max_volume = MAX_VOLUME
        self.spotify = SpotifyClient(spotify_client_id, spotify_client_secret, spotify_refresh_token)

    def pause_sonos(self):
        self.device.pause()

    def volume_up(self, level):
        level = MAP_TO_INT[level]
        current_volume = self.device.volume
        self.device.volume = min(
            current_volume + GAIN * level,
            self.max_volume)
        self.device.play()

    def volume_down(self, level):
        level = MAP_TO_INT[level]
        self.device.volume -= GAIN * level
        self.device.play()
        print self.device.volume

    def set_volume(self, volume_value):
        self.device.volume = volume_value
        self.device.play()

    def stop_sonos(self):
        self.device.stop()

    def turn_on_radio(self, radio_name):
        res = self.tunein.search('stations', term=radio_name)
        if 'mediaMetadata' not in res:
            return "radio not found"
        if isinstance(res['mediaMetadata'], list):
            radio_id = res['mediaMetadata'][0]['id']
        elif isinstance(res['mediaMetadata'], dict):
            radio_id = res['mediaMetadata']['id']
        else:
            raise TypeError("Unknown type for tune in search metadata")
        radio_uri = self.tunein.get_media_uri(radio_id)
        # queue = self.device.get_queue()
        self.device.play_uri(radio_uri.replace('http', 'x-rincon-mp3radio'))

    # def turn_on_playlist(self, playlist_name):
    #     res = self.spotify.search('playlists', term=playlist_name)
    #     if 'mediaMetadata' not in res:
    #         return "playlist not found"
    #     if isinstance(res['mediaMetadata'], list):
    #         playlist_id = res['mediaMetadata'][0]['id']
    #     elif isinstance(res['mediaMetadata'], dict):
    #         playlist_id = res['mediaMetadata']['id']
    #     else:
    #         raise TypeError("Unknown type for spotify search metadata")
    #     playlist_uri = self.tunein.get_media_uri(playlist_id)
    #     self.device.play_uri(playlist_uri.replace('http', 'x-rincon-mp3radio'))

    def set_alarm(self, alarm_time):
        n_seconds = alarm_time['hours'] * 3600 + \
                    alarm_time['minutes'] * 60 + \
                    alarm_time['seconds']
        print ALARM_DURATION
        alarm = Alarm(
            self.device,
            start_time=datetime.datetime.now() + datetime.timedelta(
                seconds=n_seconds),
            duration=ALARM_DURATION,
            recurrence="ONCE")
        alarm.save()

    def format_uri_spotify(self, uri):
        return 'x-sonos-spotify:' + uri.replace(':', '%3a') + \
            "?sid=9"

    def play_playlist(self, name, _shuffle=False):
        tracks = self.spotify.get_tracks_from_playlist(name)
        if tracks is None:
            return None
        self.device.stop()
        self.device.clear_queue()
        if _shuffle:
            shuffle(tracks)
        # self.device.play_uri(
        #     self.format_uri_spotify(tracks[0]['track']['uri']))
        for track in tracks:
            self.device.add_uri_to_queue(
                self.format_uri_spotify(track['track']['uri'])
            )
        self.device.play_from_queue(0)
        # queue = self.device.get_queue()
        # self.device.play_uri(
        #     "x-sonos-spotify:" + self.spotify.user_playlists[name]['uri']
        # )

    def play_artist(self, name):
        tracks = self.spotify.get_top_tracks_from_artist(name)
        if tracks is None:
            return None
        self.device.stop()
        self.device.clear_queue()
        for track in tracks:
            self.device.add_uri_to_queue(
                self.format_uri_spotify(track['uri'])
            )
        self.device.play_from_queue(0)

    def play_next_item_in_queue(self):
        try:
            self.device.next()
        except Exception:
            print "Failed to play next item, maybe last song?"

    def play_previous_item_in_queue(self):
        try:
            self.device.previous()
        except Exception:
            print "Failed to play previous item, maybe first song?"
