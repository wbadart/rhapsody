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
import json
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

    def request(self, endpoint, optional_args=None):
        '''
        Generic Spotify API GET request to `endpoint' (excludes leading slash).
        '''
        if optional_args == None:
            res = r.get(API_URI_FMT.format(endpoint), headers={
                'Authorization': 'Bearer {0}'.format(self._token).strip()})
        else:
            res = r.get(API_URI_FMT.format(endpoint), params=optional_args, headers={
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

    def related_artists(self,artists_id):
        return self.request('artists/{0}/related-artists/'.format(artists_id)).json()['artists']

    def albums_by_artists(self,artists_id):
        '''Request albums from artist.'''
        return self.request('artists/{0}/albums/'.format(artists_id),{'limit':50}).json()['items']
        
    def songs_by_album(self,album_id):
       '''Requst the songs from an album'''
       return self.request('albums/{0}/tracks/'.format(album_id)).json()['items']

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
    return_list = json_data['toplists']#['album']['artists']['id']
    artist_list = []
    for r in return_list:
        playlist_list = return_list[r]
        for p in playlist_list:
            album_list = p["album"]["artists"]
            for a in album_list:
                artist_list.append(a["id"])
    return artist_list


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description='Use the Spotify browse endpoints to iteratively generate '
        'a core dataset.')
    parser.add_argument('token', metavar='TOKEN', help='Spotify access token')
    args = parser.parse_args()

    spotify = Spotify(args.token)
    ids = partial(map, itemgetter('id'))
    artists = getStartingArtist('../data/core_data.json')
    #track_set = set()
    completed_artists = set()
    with PersistentDict(
        path='../data/artist_data.json',
        encode=partial(dumps, indent=2)) as result:
        count = 0
        all_artists = []
        for artist in artists:
            if artist in completed_artists:
                continue
            all_artists.append(artist)
            completed_artists.add(artist)
            for related_artists in ids(spotify.related_artists(artist)):
                all_artists.append(related_artists)
                completed_artists.add(related_artists)
        completed_artists = set()
        print("Number of Artists: "+str(len(all_artists)))
        for artist in all_artists: # for each artists in our "queue"
            if artist in completed_artists: # already done
                continue
            completed_artists.add(artist) # add to done set
            count = count+1
            print("Progress: "+str(count/len(artists)*100.0)+"%")
            result[artist] = {}
            for albums in ids(spotify.albums_by_artists(artist)): # each album of artist
                result[artist][albums] = []
                #print(albums)
                for song in ids(spotify.songs_by_album(albums)): # each song for album
                    track = spotify.track_details(song)
                    result[artist][albums].append(track)
    print("COMPLETE")


if __name__ == '__main__':
    from sys import exit
    exit(main())
