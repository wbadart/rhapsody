import rhapsody_web.models as models

from django.http import HttpResponse
from django.shortcuts import render


def index(req):
    songs = models.Song.objects.all()[:10]
    return render(req, 'rhapsody_web/index.html', {'songs': songs})
