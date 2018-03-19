from django.db import models


class Artist(models.Model):
    pass


class Song(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    spotify_id = models.CharField(max_length=22)
