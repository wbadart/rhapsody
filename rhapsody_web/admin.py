from django.contrib import admin

from .models import Artist, Song, Genre, Album, Playlist, RadioStation, Concert, User, Regular, Admin


admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(Genre)
admin.site.register(Album)
admin.site.register(Playlist)
admin.site.register(RadioStation)
admin.site.register(Concert)
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Regular)
