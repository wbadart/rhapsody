import rhapsody_web.models as models

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from random import sample

import sys

import bin.crawl as crawl

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def index(req):
    songs = sample(list(models.Song.objects.all()), k=10)
    return render(req, 'rhapsody_web/index.html', {'songs': songs})


def rand_songs(req, n):
    from itertools import product
    songs = [s.title for s in sample(list(models.Song.objects.all()), k=n)]
    pairs = sample(list(product(songs, repeat=2)), k=n)
    return JsonResponse([[s for s in songs], pairs], safe=False)

def random_walk(req, id):
    spotify = crawl.Spotify('BQD3aEb1QpWDYzYFLio2snslfTgJ_WictCNpZE4ojRnBbgrWPjP1l6YYad6A8lRzJDeOi6XAEhUT8XHklUY')
    return JsonResponse(spotify.track_recommendations(id))
#    return JsonResponse(d)
