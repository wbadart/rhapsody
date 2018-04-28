#!/usr/bin/env python3

'''
management/commands/import.py

Import initial Spotify data into Django databases.

Usage: ./manage.py import

Andrew Munch <netid:amunch>
created: MAR 2018
'''

import json

from django.core.management.base import BaseCommand
from rhapsody_web.models import Artist, Album, Playlist, Song


alb_type_dict = {
    'album': 'A',
    'single': 'S',
    'compilation': 'C'
}

class Command(BaseCommand):
    help = "Imports seed data from data/starting_tracks.json."

    DATA_PATH = "data/artist_data0.json"

    def handle(self, *args, **options):
        data = json.load(open(self.DATA_PATH))

        for artist in data:
            artist_data = data[artist]
            artist_obj = Artist(spotify_id=artist_data['id'], popularity= artist_data['popularity'], name = artist_data['name'])
            try:
                artist_obj.save()
            except:
                continue
            for album in artist_data['albums']:
                album_obj = Album(album_type=None, spotify_id = album['id'], name= album['name'], release_date = album['release_date'], artists= artist_obj);
                #album_obj.artists.add(artist_obj)
                try:
                    album_obj.save()
                except:
                    continue
                for track in album['tracks']:
                    track_obj = Song(spotify_id = track['id'], title=track['name'][0:30], artist= artist_obj, album=album_obj)
                    try:
                        track_obj.save()
                    except:
                        pass
