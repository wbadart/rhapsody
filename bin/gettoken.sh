#!/bin/sh

##
# bootstrap.sh
#
# Request a new Spotify auth token via the Client Credentials auth flow.
#
# Will Badart <netid:wbadart>
# created: MAR 2018
##

AUTH_URI='https://accounts.spotify.com/api/token'


usage() {
    echo "usage: $0 [OPTIONS]"
    echo "    Request a new access token from Spotify."
    echo
    echo "OPTIONS:"
    echo "    -h        show this help message and exit"
    exit ${1:-0}
}


while getopts 'h' arg; do
    case $arg in
        h)  usage;;
        ?)  usage 1;;
    esac
done

auth_str=`echo "$CLIENT_ID:$SPOTIFY_SECRET" | base64 | tr -d '\n'`
curl --http1.1 -X 'POST' \
    -H "Authorization: Basic ${auth_str::-1}=" \
    -d 'grant_type=client_credentials' \
    $AUTH_URI
