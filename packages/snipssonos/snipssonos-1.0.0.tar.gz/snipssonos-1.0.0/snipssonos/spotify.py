# -*-: coding utf-8 -*-
""" Sonos skill for Snips. """

import codecs
import os
import json
import requests

class SpotifyClient():

    def __init__(self, spotify_client_id, spotify_client_secret, spotify_refresh_token):
        self.client_id = spotify_client_id
        self.client_secret = spotify_client_secret
        self.refresh_token = spotify_refresh_token
        self.get_user_playlists()
        self.get_user_id()

    def refresh_access_token(self):
        _r = requests.post(
            "https://accounts.spotify.com/api/token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token
            })
        self.access_token = _r.json()['access_token']

    def get_user_id(self):
        _r = requests.get(
            "https://api.spotify.com/v1/me",
            headers={
                "Authorization": "Bearer {}".format(self.access_token),
            })
        self.user_id = _r.json()['id']

    def get_user_playlists(self):
        # TODO: get all playlists if there are more than 50 by looping
        # and using the offset parameters
        self.refresh_access_token()
        _r = requests.get(
            "https://api.spotify.com/v1/me/playlists",
            params={
                'limit': 50
            },
            headers={
                "Authorization": "Bearer {}".format(self.access_token),
            })
        self.user_playlists = {
            playlist['name'].lower(): playlist for
            playlist in _r.json()['items']}

    def get_tracks_from_playlist(self, name):
        self.refresh_access_token()
        try:
            _r = requests.get(
                self.user_playlists[name]['tracks']['href'],
                params={
                    'limit': 100
                },
                headers={
                    "Authorization": "Bearer {}".format(self.access_token),
                })
        except KeyError:
            print "Unknown playlist {}".format(name)
            return None
        return _r.json()['items']

    def _dump_favorite_artists(self, n_artists, output_name):
        self.refresh_access_token()
        all_artists_names = []
        n_found_artists = 0
        while n_found_artists < n_artists:
            _r = requests.get(
                'https://api.spotify.com/v1/me/top/artists',
                params={
                    'limit': min(50, n_artists - n_found_artists),
                    # 50 is the maximum
                    'offset': n_found_artists
                },
                headers={
                    "Authorization": "Bearer {}".format(self.access_token),
                }
            )
            all_artists_names.extend(
                [item['name'] for item in _r.json()['items']])
            if len(all_artists_names) == n_found_artists:
                print "Maximum number of artists reached: {}".format(
                    n_found_artists)
                break
            n_found_artists = len(all_artists_names)
        with codecs.open(output_name, 'w', 'utf-8') as f:
            f.write(u"\n".join(all_artists_names))

    def get_top_tracks_from_artist(self, artist):
        self.refresh_access_token()
        # First get artist id
        try:
            _r = requests.get(
                'https://api.spotify.com/v1/search',
                params={
                    'q': artist,
                    'type': 'artist'
                },
                headers={
                    "Authorization": "Bearer {}".format(self.access_token)
                }
            )
            _id = _r.json()['artists']['items'][0]['id']
            # Get list of top tracks from artist
            _r = requests.get(
                'https://api.spotify.com/v1/artists/{}/top-tracks'.format(_id),
                params={
                    'country': 'fr'
                },
                headers={
                    "Authorization": "Bearer {}".format(self.access_token)
                }
            )
            return _r.json()['tracks']
        except Exception:
            return None
