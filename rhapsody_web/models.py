from django.db import models


class Artist(models.Model):
    pass

class Genre(models.Model):
    pass

class Album(models.Model):
    pass

class Song(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    spotify_id = models.CharField(max_length=22)

class Playlist(models.Model):
    pass

class RadioStation(models.Model):
    pass

class Concert(models.Model):
    pass

class User(models.Model):
    username = models.CharField(max_length=30, primary_key=True)

class Admin(User):
    pass

class Regular(User):
    pass
