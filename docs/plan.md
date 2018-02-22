# Rhapsody Development Plan

## Relational Schema

Below is the planned relational schema for our database, as described by the ER diagram from the proposal document. Keys and functional dependencies are included.

```
Songs(**spotify_id**, title, lyrics, danceability, tempo, release_date, duration)
    S = { spotify_id -> title, lyrics, danceability, tempo, release_date, duration }

Albums(**name**, release_date)
    A1 = { **name** -> release_date }

Genres(**name**)

Albums(**spotify_id**, name, release_date)
    A2 = { spotify_id -> name, release_date}

Artists(**spotify_id**, name, age)
    A3 = { spotify_id -> name, age }

Concerts(**name**, **date**, **location**)

Playlists(**spotify_id**, num_songs, name)
    P = { spotify_id -> num_songs, name }

RadioStations(**spotify_id**)

Users(**username**)

Admins(**username**)

Regulars(**username**)
```


## Architecture and Software Stack

We will use MySQL, version 14.14 (which is available on `dsg1`) for our database. To interface between this database and our web-based application, we will implement a server-side API using the [Django] framework for Python. Facing the user will be a web-based client. We have identified a couple libraries which could drive our graph visualizations, and are primarily considering [D3.js].

Client routing will be handled by the server, but if it becomes evident by the end of the second milestone that this is an inappropriate architecture, we will factor routing into the client (supported by a SPA framework such as [Vue.js]).


## Data Sources

Our initial source of truth will be the Echo Nest API (web-based), as maintained by Spotify. During the early development stages, we intend to port a subset of this data into our own database, shaped in a way specifically tailored to our application. As stated in the proposal, the Echo Nest has over a trillion data points on more than 36 million songs. Even capturing a small subset of this data set would result in a rich baseline for our app. The app will interface with this database (not the Echo Nest) during runtime.
We do not expect to build an extensive user base before the end of the semester, but we do plan on building the pipes that would garnish usage data and leverage it for the app. This includes social features such as the *party playlist*.


## Group Roles

### Front End Application

- **UX/ Site Layout and Strategy Gurus:** Andrew & Mark
- **Graph Visualization Wizard:** Will

### Back End API and Database

- **DB Management and Query Poet:** Madeline
- **API Design Masters:** Andrew & Mark


## Project Timeline

| Milestone | Date |
|-----------|------|
| Data Collection | March |
| Admin Features (CRUD operations) | Late March |
| Basic User Features | Early April |
| Visual Graph Exploration | Late April |
| Song Recommendations | Late April |
| Party Playlist (nice to have) | Early May |


[Django]: https://www.djangoproject.com/
[D3.js]: https://d3js.org/
[Vue.js]: https://vuejs.org/
