#!/usr/bin/env python3

'''
bin/getArtistData.py

Use starting artist ids to get a bunch of songs for the database
Mark Pruitt <netid:mpruitt1>
created: 04 2018
'''

import requests as r
from requests.exceptions import ConnectionError
from base64 import b64encode as b64
from functools import partial
import json
import time
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

    def album_info(self,album_id):
        return self.request('albums/{0}/'.format(album_id)).json()

    def artist_info(self,artist_id):
        return self.request('artists/{0}/'.format(artist_id)).json()

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

# save some space by making sure we do not repeat albums
def checkRepeatAlbum(name,album_list):
    for album in album_list:
        if album['name'] == name:
           return False
    return True

#remove the artists we already completed
def completedArtists():
    with open('completed_artist.txt','r+') as f:
         a_list = set()
         for line in f:
             a_list.add(line.rstrip())
    return a_list

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
        path='../data/artist_data16.json',
        encode=partial(dumps, indent=0)) as result:
        all_artists = artists
        num_related = 3 # number of times to get related artist
        for i in range(0,num_related):
            for artist in all_artists:
                if artist in completed_artists: # already found them
                    continue
                all_artists.append(artist)
                completed_artists.add(artist)
                # get the related artists (unique)
                for related_artists in ids(spotify.related_artists(artist)):
                    if related_artists not in completed_artists:
                        all_artists.append(related_artists)
                        completed_artists.add(related_artists)
        completed_artists = completedArtists()
        print("Number of Artists: "+str(len(all_artists)))
        with open('completed_artist.txt','a') as f:
            for artist in all_artists: # for each artists in our "queue"
                try:
                    if artist in completed_artists: # already done
                        continue
                    completed_artists.add(artist) # add to done set
                    print("Progress: "+str((len(completed_artists)/len(all_artists))*100.0)+"%")
                    # HANDLE ARTIST INFO
                    result[artist] = {}
                    artist_json = spotify.artist_info(artist)
                    result[artist]['id'] = artist
                    result[artist]['genres'] = artist_json['genres']
                    result[artist]['name'] = artist_json['name']
                    result[artist]['popularity'] = artist_json['popularity']
                    result[artist]['albums'] = []
                    # END ARTIST INFO
                    for albums in ids(spotify.albums_by_artists(artist)): # each album of artist
                        # HANDLE ALBUM INFO
                        full_albums = spotify.album_info(albums)
                        if checkRepeatAlbum(full_albums['name'],result[artist]['albums']):
                            new_dict = {}
                            new_dict['id'] = albums
                            new_dict['images'] = full_albums['images']
                            new_dict['name'] = full_albums['name']
                            new_dict['release_date'] = full_albums['release_date']
                            new_dict['tracks'] = []
                            # END ALBUM INFO
                            for song in ids(spotify.songs_by_album(albums)): # each song for album
                                # HANDLE TRACK INFO
                                track = spotify.track_details(song)
                                track_info = {}
                                track_info['id'] = song
                                track_info['explicit'] = track['explicit']
                                track_info['name'] = track['name']
                                track_info['popularity'] = track['popularity']
                                track_info['release_date'] = full_albums['release_date']
                                new_dict['tracks'].append(track_info)
                            result[artist]['albums'].append(new_dict)
                    f.write(str(artist)+'\n')
                except KeyError as e2:
                    print(e2)
                    time.sleep(90)
                    continue
                except ConnectionError as e:
                    print(e)
                    f.write(str(artist)+'\n')
    print("COMPLETE")


if __name__ == '__main__':
    from sys import exit
    exit(main())
