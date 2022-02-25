import re
import requests
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth


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


    def get_featured_spotify_playlists_ids(self, genres:list):
        """
        Function to get playlists from spotify
        This function will use the spotify api to search spotify for playlists. We will use the
        function `category_playlists` which will give us playlists that are a certain category.
        This will return a bunch of data but all we need is the id of the playlist which we will
        add to a list of ids and return. To read more about `category_playlists` here is a link:
        https://developer.spotify.com/documentation/web-api/reference/#/operations/get-a-categories-playlists

        Parameters
        ----------
        genres : list
            A list of genres to search spotify playlits for

        Returns
        -------
        list
        """
        # Search for featured spotify playlists with the genres we want
        playlist_data = [self.spotify_client.category_playlists(category_id=i, country='US', limit=20, offset=0) for i in genres]
        # to hold playlists ids
        playlist_ids = []
        for j in range(len(playlist_data)):
            for i in range(len(playlist_data[j]['playlists']['items'])):
                id_ = playlist_data[j]['playlists']['items'][i]['id']
                playlist_ids.append(id_)
        return playlist_ids

    def get_playlist_data(self, playlist_ids:list):
        """
        Function to get spotify playlist data. 
        We will use the spotify api to search for each playlist by its id. This will return some
        data such as tracks,name,artitsts,album. This data will be put into a list that we will
        return that to use later.

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
                if not song_name or not artist_name or not artist_genre:
                    continue

                data_dictionary['track_name'].append(song_name)
                data_dictionary['artist_name'].append(artist_name)
                data_dictionary['artist_genre'].append(' '.join(artist_genre))

                data_dictionary['preview'].append(f'./other_data/{song_name}')
                if not preview:
                    continue
                doc = requests.get(preview)
                song_name = re.sub(r'[\\/*?:"<>|]',"", song_name)
                if doc == None or doc.content == None:
                    continue
                f = open(f'./other_data/{song_name}.wav', 'wb')
                f.write(doc.content)
                f.close()
        return data_dictionary


    def set_data_frame(self, data):
        """
        Function to set variable `data_frame` as a pandas dataframe

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
        This function will save our dataframe into a csv file.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.data_frame.to_csv('other_dataset.csv', index=False)
        return 0

sp = GetSpotifyPlaylistData()
# ids = sp.get_featured_spotify_playlists_ids(['pop', 'rock'])
ids = ['008G1BbvK1NQvbAV8MHvDz',
'68PjCnmfHOdWHNt2szkwiD',
'4A6gaLrq8RU5uRsUWFNnBZ',
'3PH11VjYTf55GzJ5kzeoOY',
'2eVuLoCP74cegyax11zgEf',
'6EZcQiAcgBb5CQaVMQVdVS',
'3QTkC28jlrBnbulDEBhldH',
'5SxaM0HGm9nfYfSxcbh4cG',
'2CuHEVcJRiBfFYlFscPX7c',
'6BunFlKoYIMFummSVTcWkQ',
'3Da3yokTjSupbEd7QSE3Kg',
'5qNHuEyfs4QHR8NI4oNaxE',
'2VCUG2HWlEeq1zvUvRkN80',
'7zVuuDwQ816JxMimuTGFjG',
'6gUFdcGzKAHyDXY9TKC6cP',
'4i4HEyLcpaSnMdI6XikFsY',
'5e1bpazQUEHijFhcJobkAp',
'2uYCFYN7H4JUOEI7N4dLHN',
'3za8xUPaO5ng9AC7rpbMNB',
'6TeyryiZ2UEf3CbLXyztFA']
playlist_data = sp.get_playlist_data(ids)
data = sp.get_track_data(playlist_data)
sp.set_data_frame(data)
sp.write_data_to_csv()
