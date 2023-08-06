from spotifylib import Spotify
import os
import logging

from pprint import pprint


logging.basicConfig(level=logging.DEBUG)

spotify = Spotify(client_id=os.environ.get('CLIENT_ID'),
                  client_secret=os.environ.get('CLIENT_SECRET'),
                  username=os.environ.get('USERNAME'),
                  password=os.environ.get('PASSWORD'),
                  callback=os.environ.get('CALLBACK_URL'),
                  scope=os.environ.get('SCOPE'))

playlists = spotify.user_playlists(os.environ.get('USERNAME'))
for playlist in playlists.get('items'):
    pprint(spotify.user_playlist_tracks(user=os.environ.get('USERNAME'),
                                        playlist_id=playlist.get('id')))

