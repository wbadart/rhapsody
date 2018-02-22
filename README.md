# rhapsody

[Repo] | [Stage 2]

Rhapsody will enable users to visualize their music in new ways. We
will generate and show a dynamic graph showing connections between
a user’s favorite songs, artists, and genres, and use that to help
them discover new music.

The website “[music-map.com][music-map]” (see
[next section](#Usefulness) provides a simple visual analog for
what we hope to accomplish, but we also want to incorporate the
music that a user actually listens to, and we want to include
individual songs. We plan to enable this feature by integrating
with the user’s Spotify account.


## Usefulness

[Music-map.com][music-map] has done a very similar
thing in terms of the visualization they provide. Rhapsody will
build on this functionality by incorporating social features and
advanced recommendation tools. If you are friends with someone on
Rhapsody, their music data points will help inform recommendations
for you as well as your own data points.


## Realness

Our data will come from The Echo Nest database, which is owned by
Spotify and available through a public API. See [this][echo nest]
and [this][spotify dev]. The Echo Nest contains over a billion data
points about more than 38 million songs. Before we deploy the
application, we will construct our own database containing
information from the API; **the application will not talk to the
API during runtime, only to our own database.**


## Features

The core feature of our project will be the advanced graph
traversal function (see [below](#graph)).

We will have two kinds of users: admins and regular users. Admins
will have the ability to insert, update, and delete songs from the
database.  Regular users will have the ability to submit a request
to insert/update/delete songs in case they find some information
that is incorrect, or they release a new song and want to add it to
the database.  This way, we can leverage the community of users to
make sure the database is accurate, but also prevent the average
user from messing everything up.

Any user will have the ability to search and view results in a
graph (or list).  They will be able to search based on song title,
artist, genre, key, etc.

Another planned feature is the **party playlist**, a shared
playlist based on the combined recommendations for a group of
users.

### Advanced Functions

#### Song recommendations

This feature can suggest songs based on other songs, albums,
artists, genres, playlists, or the songs in the user’s library.
The feature will implement a distance function to rate the
similarity of songs and use the nearest neighbors as the
recommendations.

#### Visual graph exploration<a name="graph"></a>

This feature is the core value proposition of our project. By
allowing users to explore (traverse) their network of music
preferences in a visual and dynamic way, we introduce an exciting
and modern genre of music discovery.


## Database Design

![ER Diagram][diagram]

[Full sized image][diagram]


## Collaborators

- Andrew Munch
- Madeline Kusters
- Mark Pruitt
- Will Badart


*Read the project proposal [here][proposal].*


[Repo]: https://github.com/wbadart/rhapsody
[Stage 2]: https://wbadart.github.io/rhapsody/docs/plan

[music-map]: https://www.music-map.com "music-map.com"
[echo nest]: https://developer.spotify.com/spotify-echo-nest-api
[spotify dev]: https://developer.spotify.com/web-api/get-recommendations
[diagram]: ./docs/RhapsodyER.jpg
[proposal]: https://docs.google.com/document/u/1/d/e/2PACX-1vQNxzjD-FGfpvWqVDfiONowMLfyproNbusEhafd4aMpwSxZKjiSYF4N-kvraaIjSR4bJArAKajUoDUF/pub
