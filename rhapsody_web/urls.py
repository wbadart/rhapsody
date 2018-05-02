from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('test/<int:n>', views.rand_songs, name='test'),
    path('api/<str:spotify_id>', views.nearest_neighbors, name='walk'),
    path('recommend/<str:name>', views.recommend, name='recommend'),
]
