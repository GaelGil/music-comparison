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
    data_frame : list
        A pandas dataframe
    Methods
    -------
    get_spotify_playlist(self, genres:list, limit:int, type:str)
        Get spotify featured playlists or not featured 

    get_spotify_playlist_ids(self, playlist_data:list, genres:list):
        Get the ID's of spotify playlists with the spotify api

    get_playlist_data(self, playlist_ids:list)
        Get the data of a spotify playlist using the spotify api

    add_set_data_frame(self)
        Set the class variable data_frame

    write_data_to_csv(self)
        Write the class varible data_frame to a csv file
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


    def get_spotify_playlists(self, genres:list, limit:int, type=None):
        """
        Function to get playlists from spotify
        This function will use the spotify api to search spotify for playlists. We will use the
        function `category_playlists` or 'search' which will give us playlists data. To read more
        about `category_playlists`or `search` functions here is a link:
        https://developer.spotify.com/documentation/web-api/reference/#/operations/get-a-categories-playlists

        Parameters
        ----------
        genres : list
            A list of genres to search spotify playlits for

        limist : int
            A integer that can be used to limit how many items we get in our spotify reqest

        type : list
            A string to differentiate what type of playlist data we want from spotify

        Returns
        -------
        list
            A list of dictionaries where every item in the list is a dictionary containing
            data to a single playlist.
        """
        # Get spotify playlists by searching or getting featured playlists
        if type == 'search':
            # if we only want searched playlists 
            playlist_data = [self.spotify_client.search(q=i, limit=limit, offset=0, type='playlist', market='US') for i in genres]
        if type == 'featured':
            # if we only want featured playlists
            playlist_data = [self.spotify_client.category_playlists(category_id=i, country='US', limit=limit, offset=0) for i in genres]
        if not type:
            # if we want both
            featured_data = [self.spotify_client.category_playlists(category_id=i, country='US', limit=limit, offset=0) for i in genres]
            search_data = [self.spotify_client.search(q=i, limit=limit, offset=0, type='playlist', market='US') for i in genres]
            playlist_data = featured_data + search_data
        return playlist_data


    def get_spotify_playlist_ids(self, playlist_data:list, genres:list):
        """
        Function to get spotify playlist ids.
        This function will extract the spotify playlist ids from the data we recived in `get_spotify_playlists`.
        We get the ids so that we can search it up later to get all the data that is inside the playlist. We
        need to do this because in our initial search using `category_playlists` and `search` all the data we
        need is not included. We iterate thorugh `playlist_data` and look for the id of the playlist. Once we
        have it we add it to a list `playlist_ids` which we then return.

        Parameters
        ----------
        playlist_data : list
            A list containing spotify playlists data

        Returns
        -------
        list
            A list of spotify playlist ids and their genres
        """
        playlist_ids = []
        for j in range(len(playlist_data)):
            # contains where we got out data from ie what general genre
            request_sent = playlist_data[j]['playlists']['next']
            data_genre = 0
            # When we search things we want to know what we searched and what data we got from that.
            # For example if we searched 'pop' then we want to know which playlists came from that search
            # This here will help us find it
            for i in genres:
                if i in request_sent:
                    data_genre = i
            # get the ID and append to a list along with the genre
            for i in range(len(playlist_data[j]['playlists']['items'])):
                id_ = playlist_data[j]['playlists']['items'][i]['id']
                playlist_ids.append([id_, data_genre])
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
            a list of dictionaries where every item in the list is a dictionary containing
            data to a single playlist.
        """
        playlist_data = []
        for i in range(len(playlist_ids)):
            playlist_data.append([self.spotify_client.playlist(playlist_id=playlist_ids[i][0]), playlist_ids[i][1]])
        return playlist_data


    def format_data(self, track, wav=True):
        """
        Parameters
        ----------
        track : dict
            A dictionary
        
        wav: bool
            A bool

        Returns
        -------
        """
        song = track['track']['name']
        artist = track['track']['artists'][0]['name']
        artist_id = track['track']['artists'][0]['id']
        preview_url = track['track']['preview_url']
        artist_data = self.spotify_client.artist(artist_id=artist_id)
        artist_genre = artist_data['genres']
        if wav:            
            if not preview_url:
                return
            else:
                doc = requests.get(preview_url) 
                song_clean = re.sub(r'[\\/*?:"<>|]',"", song) # clean the song name
                path_to_wav = f'./audio_data/mp3_data/{song_clean}.mp3' # create a path to the song
                if not doc or not doc.content:
                    return False
                f = open(path_to_wav, 'wb') 
                f.write(doc.content) # write the content of doc to a file
                f.close()                
                return [song, path_to_wav, artist, ''.join(artist_genre)]
        if not wav:
            current_playlist = []
            song_and_artist  = f'{song} {artist} {artist_genre}'
            current_playlist.append(song_and_artist)
            return current_playlist, artist_genre


        
            

    def extract_data(self, playlists:list, wav=True):
        """
        Function to get playlists from spotify
        This function will use the spotify api to search spotify for playlists. We will use the
        function `category_playlists` or 'search' which will give us playlists data. To read more
        about `category_playlists`or `search` functions here is a link:
        https://developer.spotify.com/documentation/web-api/reference/#/operations/get-a-categories-playlists

        Parameters
        ----------
        playlists : list
            A list of

        wav : bool
            A bool

        Returns
        -------
        dict
            A dictionary
        """
        playlist_data = {'playlist_id': [], 'playlist': [], 'genre': [], 'artist_genre': [], 'genre': []}
        data_list = []
        wav_data = {'song': [], 'path_to_wav': [], 'artist': [], 'artist_genre': [], 'genre': []}
        # for every playlists
        for i in range(len(playlists)):
            tracks = playlists[i][0]
            genre = playlists[i][1]
            id_ = playlists[i][0]['id']
            # for every track in every playlist
            for track in tracks['tracks']['items']:
                # if we have a track
                if track['track']:
                    # if we want wav data
                    if wav:
                        data = self.format_data(track, wav)
                        if data:
                            wav_data['song'].append(data[0])
                            wav_data['path_to_wav'].append(data[1])
                            wav_data['artist'].append(data[2])
                            wav_data['artist_genre'].append(data[3])
                            wav_data['genre'].append(genre)
                        else:    
                            continue
                # if we want playlists data
                if not wav:
                    current_playlist, artist_genre = self.format_data(track, False)
                    data_list.append([id_, current_playlist, artist_genre, genre])
        for i in range(len(data_list)):
            playlist_data['playlist_id'].append(data_list[i][0])
            playlist_data['playlist'].append(data_list[i][1])
            playlist_data['artist_genre'].append(data_list[i][2])
            playlist_data['genre'].append(data_list[i][3])

        if not wav:
            return playlist_data
        return wav_data


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


    def write_data_to_csv(self, name:str):
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
        self.data_frame.to_csv(name, index=False)
        return 0

sp = GetSpotifyPlaylistData()
# get spotify playlists
data = sp.get_spotify_playlists(genres=['pop', 'rock'], limit=10)
# get a ids for all the playlists we have
ids = sp.get_spotify_playlist_ids(data, genres=['pop', 'rock'])
# get the data that we go back from searching a playlist by id
playlist_data = sp.get_playlist_data(ids)
# extract the data in a format we want
to_csv = sp.extract_data(playlist_data)
# set our class dataframe equal to our data
sp.set_data_frame(to_csv)
# write the dataframe to csv
sp.write_data_to_csv('./audio_data/csv/song_wav_data.csv')

# ids = ['008G1BbvK1NQvbAV8MHvDz',
# '68PjCnmfHOdWHNt2szkwiD',
# '4A6gaLrq8RU5uRsUWFNnBZ',
# '3PH11VjYTf55GzJ5kzeoOY',
# '2eVuLoCP74cegyax11zgEf',
# '6EZcQiAcgBb5CQaVMQVdVS',
# '3QTkC28jlrBnbulDEBhldH',
# '5SxaM0HGm9nfYfSxcbh4cG',
# '2CuHEVcJRiBfFYlFscPX7c',
# '6BunFlKoYIMFummSVTcWkQ',
# '3Da3yokTjSupbEd7QSE3Kg',
# '5qNHuEyfs4QHR8NI4oNaxE',
# '2VCUG2HWlEeq1zvUvRkN80',
# '7zVuuDwQ816JxMimuTGFjG',
# '6gUFdcGzKAHyDXY9TKC6cP',
# '4i4HEyLcpaSnMdI6XikFsY',
# '5e1bpazQUEHijFhcJobkAp',
# '2uYCFYN7H4JUOEI7N4dLHN',
# '3za8xUPaO5ng9AC7rpbMNB',
# '6TeyryiZ2UEf3CbLXyztFA']
# playlist_data = sp.get_playlist_data(ids)
# data = sp.get_track_data(playlist_data)
# sp.set_data_frame(data)
# sp.write_data_to_csv()

