#!/usr/bin/env python3

'''
bin/getArtistData.py

Use starting artist ids to get a bunch of songs for the database
Mark Pruitt <netid:mpruitt1>
created: 04 2018
'''

import requests as r
from base64 import b64encode as b64
from functools import partial
from json import dumps
from operator import itemgetter
from os import environ
from wbutil import PersistentDict

API_URI_FMT = 'https://api.spotify.com/v1/{0}'
AUTH_URI = 'https://accounts.spotify.com/api/token'
CLIENT_ID = '2f444881b6034fd59ca98950a2466e5a'


class Spotify(object):
    '''
    Class which simplifies sending requests to the Spotify API on behalf of the
    rhapsody application.
    '''

    def __init__(self, token, secret=environ.get('SPOTIFY_SECRET')):
        '''
        token:  Spotify access token granted by Client Credentials flow
        secret: rhapsody client secret (only needed if you want to
                  automatically refresh the access token when it expires
        '''
        self._token = token
        self._secret = secret

    def request(self, endpoint):
        '''
        Generic Spotify API GET request to `endpoint' (excludes leading slash).
        '''
        res = r.get(API_URI_FMT.format(endpoint), headers={
            'Authorization': 'Bearer {0}'.format(self._token).strip()})
        if self._expired(res):
            self._refresh_token()
            return self.request(endpoint)
        else:
            return res

    @property
    def categories(self):
        '''Query Spotify for the complete list of category IDs.'''
        return self.request('browse/categories').json()['categories']['items']

    def albums_by_artists(self,artists_id):
        '''Request albums from artist.'''
        return [self.request('artist/{0}/albums/'.format(artists_id)).json()['items']]

    def songs_by_album(self,album_id):
       '''Requst the songs from an album'''
       return [self.request('albums/{0}/tracks/'.format(album_id)).json()['items']]

    def playlists_by_category(self, category_id):
        '''Request the list of playlists for the given category.'''
        return self.request('browse/categories/{0}/playlists'.format(
            category_id)).json()['playlists']['items']

    def tracks_by_playlist(self, playlist_id):
        '''
        Request track IDs for every track on playlist of the given id.
        '''
        return [item['track'] for item in self.request(
            'playlists/{0}/tracks'.format(playlist_id)).json()['items']]

    def track_details(self, track_id):
        '''Request the details for track of given track_id.'''
        return self.request('tracks/{0}'.format(track_id)).json()

    def _refresh_token(self):
        '''Update self's access token with a new access token from Spotify.'''
        if self._secret is None:
            raise RuntimeError(
                'Client secret not provided. Please request a new token')
        auth_str = (CLIENT_ID + ':' + self._secret).encode()
        res = r.post(AUTH_URI, headers={
            'Authorization': 'Basic {0}'.format(b64(auth_str).decode())},
            data={'grant_type': 'client_credentials'})
        self._token = res.json()['access_token']

    @staticmethod
    def _expired(res):
        '''Determine if the request is reporting an expired access token.'''
        return res.status_code == 401 \
            and res.json()['error']['message'] == 'The access token expired'


def getStartingArtist(filename):
    json_data = json.load(open(filename))
    return_list = json_data['toplists']['album']['artists']['id']
    print(return_list)
    return return_list


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description='Use the Spotify browse endpoints to iteratively generate '
        'a core dataset.')
    parser.add_argument('token', metavar='TOKEN', help='Spotify access token')
    args = parser.parse_args()

    spotify = Spotify(args.token)
    ids = partial(map, itemgetter('id'))

    track_set = set()

    with PersistentDict(
            path='../data/artist_data.json',
            encode=partial(dumps, indent=2)) as result:
            artists = getStartingArtist('../data/core_data.json')
            track_set = set()
            '''for artist in artists:
                    result[artist] = {}
                    for albums in id(spotify.albums_by_artists(artist)):
                           for song in id(sportify.songs_by_album(albums)):
                                   if song not in track_set:
                                           track_set.add(song)
                                           track_info = spotify.track_details(track)
                                           result[artist][albums].append(track)'''


if __name__ == '__main__':
    from sys import exit
    exit(main())
