import rhapsody_web.models as models

from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from json import loads, dumps
from random import sample, random, choice

import sys
import operator

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


def nearest_neighbors(req, spotify_id):
    node = _getobj(pk=spotify_id)
    DEPTH = 4
    edges = [[a.spotify_id, b.spotify_id] for a, b in node.edges(DEPTH)]
    vertices = {x for y in list(node.g.values()) for x in y}
    
    for node in list(node.g):
        vertices.add(node)

    nodes = loads(serialize('json', vertices))
    return JsonResponse([nodes, edges], safe=False)


def random_walk_n_recommendations(spotify_id):
    try:
        start_node = models.Song.objects.get(pk=spotify_id)
    except models.Song.DoesNotExist:
        try:
            start_node = models.Artist.objects.get(pk=spotify_id)
        except models.Artist.DoesNotExist:
            try:
                start_node = models.Album.objects.get(pk=spotify_id)
            except models.Album.DoesNotExist:
                pass

    prob_go_home = 0.5

    current_node = start_node

    visits = {}

    #    random.seed()

    for i in range(100):
        if current_node not in visits:
            visits[current_node] = 1
        else:
            visits[current_node] += 1

        if random() <= prob_go_home:
            current_node = start_node
        else:
            #randomly choose a node from the neighbors for the next node
            current_node = choice(list(current_node.neighbors()))

    #print(len(visits))

    sorted_visits = sorted(visits.items(), key=operator.itemgetter(1))
    print(start_node)
    if start_node in sorted_visits:
        print("removing start_node")
        sorted_visits.remove(start_node)

    print(len(sorted_visits))
    print(sorted_visits[0])
    return sorted_visits[0:5]


def recommend(req, name):
    node = _getobj(name=name)
    if node is None:
        return JsonResponse({'tracks': [{'name': 'No recommendations found', 'artist': ''}]})
    else:
        spotify = crawl.Spotify('BQCmCTrB2ilbLEQfOFgMTwlw_td7db30DXx3AgNnlQ4tFXBubuQJmE8iKOcdsdlOR_aUq3zVN7gSt2zR9LQ')
        return JsonResponse(spotify.track_recommendations(node.spotify_id, limit=5))


def search(request):
    q = request.GET.get('term', '')
    similar_songs = models.Song.objects.filter(title__icontains = q)[:10]
    results = []
    for s in similar_songs:
        s_json = {}
        s_json['id'] = s.spotify_id
        s_json['label'] = s.title
        s_json['value'] = s.title
        results.append(s_json)
    data = dumps(results)
    return HttpResponse(data, 'application/json')


def _getobj(**query):
    try:
        node = models.Album.objects.get(**query)
    except models.Album.DoesNotExist:
        try:
            node = models.Artist.objects.get(**query)
        except models.Artist.DoesNotExist:
            try:
                node = models.Song.objects.get(**query)
            except models.Song.DoesNotExist:
                node = None
    return node

