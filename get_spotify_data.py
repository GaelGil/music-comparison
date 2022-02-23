import os
import csv
import re
import numpy as np
import pandas as pd
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pathvalidate import sanitize_filename





class GetSpotifyPlaylistData:
    """
    A class used to communicate with the Spotify api.
    Attributes
    ----------
    popular_tracks : list
        A list of popular tracks on spotify
    Methods
    -------
    get_spotify_playlists(self, query:str)
        Searches spotify for playlists
    get_popular_songs(self, spotify_playlist_id:str):
        Gets most popular songs from spotify playlist
    create_spotify_playlist(self, playlist_name:str, for_user:str)
        Creates a new spotify playlists using a name and a users name
    add_tracks_to_playlist(self, playlist_id:str)
        Adds song to a spotify playlists
    """

    def __init__(self):
        """
        This function will call the class function `auth_spotify` and create a list for later use.
        Parameters
        ----------
        None
        Returns
        -------
        None
        """
        self.spotify_client = self.auth_spotify()
        self.data_frame = 0


    @classmethod
    def auth_spotify(cls):
        """
        Function to authenticate spotify
        This function will get the spotify client so we can use the api by authenticating. It will
        also set the scopes so we are able to use the tools that we need such as
        `playlist-modify-public` to create public spotify playlist
        Parameters
        ----------
        Returns
        -------
        str
            The spotify client
        """
        scope = "user-library-read,user-top-read,playlist-modify-public"
        spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        return spotify_client


    def get_spotify_playlists_ids(self, genres:list):
        """
        Function to get playlists from spotify
        This function will use the spotify api to search spotify for playlists. We will get
        a bunch of data in return but all we need is the uri (ID). We will then append those
        ID's to a list.

        Parameters
        ----------
        genres : list
            A list of genres to search spotify playlits for

        Returns
        -------
        list
        """
        # We will search spotify for the genres listed in  the variable `genres`. This will
        # return playlists ids
        playlists_data = [self.spotify_client.search(q=i, type='playlist', limit=50) for i in genres]
        # to hold playlists ids
        playlists_ids = []
        for i in range(len(playlists_data[0]['playlists']['items'])):
            # add eacj playlist ids to the list
            playlists_ids.append(playlists_data[0]['playlists']['items'][i]['uri'])
        return playlists_ids

    def get_playlist_data(self, playlist_ids:list):
        """
        Function to get spotify playlist data. 
        We will use the spotify api to search for each playlist by its id. This will return some
        data such as tracks,name,artitsts,album. This data will be put into a list that we will
        return. 

        Parameters
        ----------
        playlist_ids : str
            A list of spotify playlists ids

        Returns
        -------
        list
        """
        # get playlist data
        playlists_data  = [self.spotify_client.playlist(playlist_id=i) for i in playlist_ids]
        return playlists_data


    def get_track_data(self, playlists:list):
        """
        Function to get data from a spotify track.
        This function will

        Parameters
        ----------
        playlists : str
            A list of spotify playlist data

        Returns
        -------
        None
        """
        tracks_list = []
        data_dictionary = {'track_name': [], 'artist_name': [], 'preview': [], 'artist_genre': []}
        # for every playlists
        for i in range(len(playlists)):
            tracks = playlists[i]
            # for every track in every playlist
            for track in tracks['tracks']['items']:
                # select the data we need
                song_name = track['track']['name']
                artist_name = track['track']['artists'][0]['name']
                artist_id = track['track']['artists'][0]['id']
                preview = track['track']['preview_url']
                artist_information = self.spotify_client.artist(artist_id)
                artist_genre = artist_information['genres']
                # add to dataframe
                data_dictionary['track_name'].append(song_name)
                data_dictionary['artist_name'].append(artist_name)
                data_dictionary['artist_genre'].append(artist_genre)

                data_dictionary['preview'].append(f'./data/{song_name}')
                if preview == None:
                    continue
                doc = requests.get(preview)
                song_name = re.sub(r'[\\/*?:"<>|]',"", song_name)
                if doc == None or doc.content == None:
                    continue
                f = open(f'./data/{song_name}.mp3', 'wb')
                f.write(doc.content)
                f.close()
        return data_dictionary

    def set_data_as_pd(self, data):
        """
        Function to set variable `data_frame` as a dataframe

        Parameters
        ----------
        playlists : str
            A list of spotify playlist data

        Returns
        -------
        None
        """
        self.data_frame = pd.DataFrame(data=data)
        return 0

    def write_data_to_csv(self):
        """
        Function to write the dataframe to a csv file.
        This function will save our dataframe into a csv file

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.data_frame.to_csv('data.csv', index=False)
        return 0

# f = open("pop_data.csv", "x")


sp = GetSpotifyPlaylistData()
# tracks = sp.spotify_client.playlist(playlist_id='37i9dQZF1DWZQaaqNMbbXa')
# ids = sp.get_spotify_playlists_ids(['pop', 'jazz'])
# playlist_data = sp.get_playlist_data(ids)
# data = sp.get_track_data(playlist_data)
# sp.set_data_as_pd(data)
# sp.write_data_to_csv()
# featured_playlist = sp.spotify_client.featured_playlists(locale='en-us_US', country='US', timestamp=None, limit=50, offset=0)
searched_playlists = sp.spotify_client.search(q='pop', type='playlist', limit=10, market='US')
# print(searched_playlists)

# print(sp.spotify_client.available_markets())

print(sp.spotify_client.categories(country='US', locale='en-us_US', limit=50, offset=0)['categories']['items'][16])
# print(data)
# print(data.keys())
# print(data['playlists'])
# print(data['playlists']['items'])
# print(sp.spotifpyy_client.playlist(playlist_id='37i9dQZF1DXafb0IuPwJy'))
# print(tracks)
# print(type(tracks))
# tracks_list = []
# for track in tracks['tracks']['items']:
#     if track['track']:
#         popularity = track['track']['popularity'] # get popularity value (str)
#         uri = track['track']['uri'] # get uri for the track (str)
#         name = track['track']['artists'][0]['name'] # get name of the track
#         tracks_list.append(uri)


# for i in tracks_list:
#     # song information
#     song = sp.spotify_client.track(i)
#     # artist of song (id)
#     artist = song['artists'][0]['id']
#     # artist information
#     artist_information = sp.spotify_client.artist(artist)
#     # artist genre
#     artist_genre = artist_information['genres']
#     # artist name
#     artist_name = song['artists'][0]['name']
#     # song name
#     song_name = song['name']
#     preview = song['preview_url']
#     print(f'Artist Genre: {artist_genre}')
#     print(f'Artist Name: {artist_name}')
#     print(f'Song Name: {song_name}')
#     print(f'Preview: {preview}')
#     doc = requests.get(preview)
#     if preview == None or doc == None or doc.content == None:
#         pass

#     f = open(f'./data/{song_name}.mp3', 'wb')
#     f.write(doc.content)
#     f.close()
#     print()





