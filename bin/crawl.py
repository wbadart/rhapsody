#!/usr/bin/env python3

'''
bin/crawl.py

Use the Spotify browse endpoints to iteratively generate a core dataset.

Will Badart <netid:wbadart>
created: MAR 2018
'''

import requests as r
from functools import partial
from json import dumps
from wbutil import PersistentDict

API_URI_FMT = 'https://api.spotify.com/v1/{0}'


def spotify_request(token, endpoint):
    '''
    '''
    res = r.get(API_URI_FMT.format(endpoint), headers={
        'Authorization': 'Bearer {0}'.format(token).strip()})
    if res.status_code == 401 \
            and res.json()['message'] == 'The access token expired':
        raise RuntimeError('You probably need a fresh token')
    return res


def category_playlists(token, category_id):
    '''
    '''
    return spotify_request(
        token,
        'browse/categories/{0}/playlists'.format(
            category_id)).json()['playlists']['items']


def playlist_tracks(token, playlist_id):
    '''
    '''
    return [item['track'] for item in spotify_request(
        token,
        'playlists/{0}/tracks'.format(playlist_id)).json()['items']]


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description='Use the Spotify browse endpoints to iteratively generate '
        'a core dataset.')
    parser.add_argument('token', metavar='TOKEN', help='Spotify access token')
    args = parser.parse_args()

    req = partial(spotify_request, args.token)

    categories = (category['id'] for category in req(
        'browse/categories').json()['categories']['items'])

    with PersistentDict(
            path='data/starting_tracks.json',
            encode=partial(dumps, indent=2)) as result:
        for category in categories:
            result[category] = {}
            playlists = category_playlists(args.token, category)
            for playlist in playlists:
                result[category][playlist['id']] = []
                tracks = playlist_tracks(args.token, playlist['id'])
                for track in tracks:
                    track_details = spotify_request(
                        args.token, 'tracks/{0}'.format(track['id'])).json()
                    result[category][playlist['id']].append(track_details)


if __name__ == '__main__':
    from sys import exit
    exit(main())
