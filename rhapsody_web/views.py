import rhapsody_web.models as models

from django.http import HttpResponse
from django.shortcuts import render

from random import sample


def index(req):
    songs = sample(list(models.Song.objects.all()), k=10)
    return render(req, 'rhapsody_web/index.html', {'songs': songs})
