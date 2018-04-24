#!/usr/bin/env python3

'''
bin/getArtistData.py

Use starting artist ids to get a bunch of songs for the database
Mark Pruitt <netid:mpruitt1>
created: 04 2018
'''

from functools import partial
from json import dumps, load
from operator import itemgetter
from wbutil import PersistentDict

from crawl import Spotify

API_URI_FMT = 'https://api.spotify.com/v1/{0}'
AUTH_URI = 'https://accounts.spotify.com/api/token'
CLIENT_ID = '2f444881b6034fd59ca98950a2466e5a'


class SpotifyArtists(Spotify):
    '''
    Class which simplifies sending requests to the Spotify API on behalf of the
    rhapsody application. Focus on artists.
    '''

    def albums_by_artists(self, artists_id):
        '''Request albums from artist.'''
        return [self.request('artist/{0}/albums/'.format(
            artists_id)).json()['items']]

    def songs_by_album(self, album_id):
        '''Requst the songs from an album'''
        return [self.request('albums/{0}/tracks/'.format(
            album_id)).json()['items']]


def getStartingArtists(filename):
    with open(filename) as fs:
        json_data = load(fs)
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

    spotify = SpotifyArtists(args.token)
    ids = partial(map, itemgetter('id'))

    track_set = set()

    with PersistentDict(
            path='../data/artist_data.json',
            encode=partial(dumps, indent=2)) as result:
        artists = getStartingArtists('../data/core_data.json')
        track_set = set()
        for artist in artists:
            result[artist] = {}
            for albums in ids(spotify.albums_by_artists(artist)):
                for song in ids(spotify.songs_by_album(albums)):
                    if song not in track_set:
                        # track_set.add(song)
                        # track_info = spotify.track_details(song)
                        # result[artist][albums].append(song)
                        pass


if __name__ == '__main__':
    from sys import exit
    exit(main())

# vim: set expandtab ts=4
