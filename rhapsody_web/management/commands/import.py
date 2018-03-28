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
from rhapsody_web.models import Artist


class Command(BaseCommand):
    help = "Imports seed data from data/starting_tracks.json."

    DATA_PATH = "data/starting_tracks.json"

    def handle(self, *args, **options):
        data = json.load(open(self.DATA_PATH))

        for playlist in data['toplists']:
            for s in data['toplists'][playlist]:
                for art in s['artists']:
                    artist_obj = Artist(spotify_id=art['id'],  popularity=None, name=art['name'])
                    artist_obj.save()
