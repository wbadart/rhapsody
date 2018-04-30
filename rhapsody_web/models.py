from django.db import models

class Artist(models.Model):
    spotify_id = models.CharField(max_length=22, primary_key=True)
    popularity = models.IntegerField(null=True)
    name = models.CharField(max_length=30, default="")
    # albums - ManyToManyField included in Album
    # songs - ManyToManyField included in Song
    #concerts = models.ManyToManyField(Concert)

class Genre(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    artists = models.ManyToManyField(Artist)
    # albums - ManyToManyField included in Album
    # songs -
    #   In the spotify data, individual songs don't have genre
    #   data. We could extrapolate this from the album or artist genre
    #   data later though

class Album(models.Model):
    ALBUM = "A"
    SINGLE = "S"
    COMPILATION = "C"
    ALBUM_TYPE_CHOICES = (
        (ALBUM, "album"),
        (SINGLE, "single"),
        (COMPILATION, "compilation")
    )
    album_type = models.CharField(max_length=1, choices=ALBUM_TYPE_CHOICES, default=ALBUM)
    artists = models.ManyToManyField(Artist)
    spotify_id = models.CharField(max_length=22, primary_key=True)
    genres = models.ManyToManyField(Genre)
    label = models.CharField(max_length=30, default="")
    name = models.CharField(max_length=30, default="")
    release_date = models.DateField(null=True)  # Note this is going to come in
                                       # as a string from the spotify
                                       # API, so some conversion will
                                       # have to be done

class Song(models.Model):
    spotify_id = models.CharField(max_length=22, primary_key=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, default="")

class Playlist(models.Model):
    spotify_id = models.CharField(max_length=22, primary_key=True)
    owner = models.ForeignKey('User', null=True, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song)
    collaborative = models.BooleanField(default=False)
    description = models.CharField(max_length=5000, default="")
    # followers - see ManyToManyField in User
    name = models.CharField(max_length=30, default="")
    public = models.BooleanField(default=True)

class RadioStation(models.Model):
    pass

class Concert(models.Model):
    pass

class User(models.Model):
    #abstract = True

    username = models.CharField(max_length=30, unique=True)
    spotify_id = models.CharField(max_length=22, primary_key=True)
    artist = models.ManyToManyField(Artist)
    genre = models.ManyToManyField(Genre)
    album = models.ManyToManyField(Album)
    song = models.ManyToManyField(Song)
    playlist_followed = models.ManyToManyField(Playlist)
    radio_station = models.ManyToManyField(RadioStation)
    friends = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)

class Admin(User):
    pass

class Regular(User):
    pass

class Song_Graph(models.Model):
    song1_id = models.CharField(max_length=22, null=True)
    song2_id = models.CharField(max_length=22, null=True)
    edge_weight = models.IntegerField(null=True)

    class Meta:
        unique_together = ("song1_id", "song2_id")
