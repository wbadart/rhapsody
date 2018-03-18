#!/bin/sh

##
# bootstrap.sh
#
# Start to pull down Spotify metadata.
#
# Will Badart <netid:wbadart>
# created: MAR 2018
##

API_URI="https://api.spotify.com/v1"
OUTPUT_DIR='./data'


usage() {
    echo "usage: $0 [OPTIONS] ARTIST [ARTIST ...]"
    echo "    Query the Spotify web API for metadata on the given list of seed"
    echo "    artists. Please set SPOTIFY_TOKEN before running."
    echo
    echo "ARGUMENTS:"
    echo "    ARTIST            artist name(s) to seed graph with"
    echo
    echo "OPTIONS:"
    echo "    -o OUTPUT_DIR     location to save JSON responses (default:./data)"
    echo "    -h                show this help message and exit"
    exit ${1:-0}
}


spotify_search_artist() {
    artist=`echo $1 | tr ' ' '+'`
    curl --http1.1 \
        -H "Authorization: Bearer $SPOTIFY_TOKEN" \
        "$API_URI/search?q=$artist&type=artist" 2> /dev/null
}


while getopts 'o:h' arg; do
    case $arg in
        o)  OUTPUT_DIR="$OPTARG";;
        h)  usage;;
        ?)  usage 1;;
    esac
done

mkdir -p "$OUTPUT_DIR" || exit 1
while [ ! -z "$1" ]; do
    echo "Searching for '$1'..."
    spotify_search_artist "$1" > "$OUTPUT_DIR/$1.json"
    shift
done
