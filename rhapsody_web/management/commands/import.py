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

    DATA_PATH = "data/starting_tracks.json"

    def handle(self, *args, **options):
        data = json.load(open(self.DATA_PATH))

        for playlist in data['toplists']:
            playlist_obj = Playlist(spotify_id=playlist, owner=None, \
                                    collaborative=1, description='', \
                                    name='', public=1)
            playlist_obj.save()  

            for s in data['toplists'][playlist]:
                alb_data = s['album']
                if alb_data['release_date_precision'] == 'day':
                    r_date = alb_data['release_date']
                else:
                    r_date = None
                alb = Album(album_type=alb_type_dict[alb_data['album_type']], \
                            spotify_id = alb_data['id'], name=alb_data['name'][0:30], \
                            release_date=r_date)
                alb.save()
                
                for art in s['artists']:
                    artist_obj = Artist(spotify_id=art['id'],  popularity=None, name=art['name'])
                    artist_obj.save()
                    alb.artists.add(artist_obj)

                so = Song(spotify_id=s['id'], title=s['name'][0:30], artist=artist_obj, \
                            album=alb)
                try:
                    so.save()  
                    playlist_obj.songs.add(so)             
                except:
                    pass
