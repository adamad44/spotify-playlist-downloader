import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytubefix import YouTube
from tkinter import filedialog
import os
import time

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

if not client_id or not client_secret:
    raise EnvironmentError("SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET must be set as environment variables.")

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def fetch_yt_results(query, limit=5):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
        video_ids = [entry['id'] for entry in search_results['entries']]
        return video_ids


def extract_playlist_id(playlist_url):
    if 'spotify.com/playlist/' in playlist_url:
        playlist_id = playlist_url.split('playlist/')[1].split('?')[0]
        return playlist_id
    elif 'spotify.com/album/' in playlist_url:
        playlist_id = playlist_url.split("album/")[1].split("?")[0]
        return playlist_id


def get_type(playlist_url):
    if 'spotify.com/playlist/' in playlist_url:
        return "playlist"
        
    elif 'spotify.com/album/' in playlist_url:
        return "album"


def get_playlist_tracks(playlist_id, type):
    tracks = []

    if type == "playlist":

        results = sp.playlist_items(playlist_id, limit=100)
        

        for item in results['items']:
            if item['track']:
                name = item['track']['name']
                artist = [artist['name'] for artist in item['track']['artists']]
                tracks.append({'name': name, 'artist': ', '.join(artist)})
        
        while results['next']:
            results = sp.next(results)
            for item in results['items']:
                if item['track']:
                    name = item['track']['name']
                    artist = [artist['name'] for artist in item['track']['artists']]
                    tracks.append({'name': name, 'artist': ', '.join(artist)})

    elif type == "album":

        results = sp.album_tracks(playlist_id, limit=50)
     
        for item in results['items']:
            name = item['name']
            artist = [artist['name'] for artist in item['artists']]
            tracks.append({'name': name, 'artist': ', '.join(artist)})
   
        while results['next']:
            results = sp.next(results)
            for item in results['items']:
                name = item['name']
                artist = [artist['name'] for artist in item['artists']]
                tracks.append({'name': name, 'artist': ', '.join(artist)})
    
    return tracks


def format_for_yt(type, id, raw):
    formatted_search_query = []
    
    if type == "playlist":        
        for i in get_playlist_tracks(id, type):
            formatted_search_query.append(f"{i['name']} by {i['artist']}")

        return formatted_search_query


    elif type == "album":
        for i in get_playlist_tracks(id, type):
            formatted_search_query.append(f"{i['name']} by {i['artist']}")

        return formatted_search_query


def download_youtube_audio(video_id, output_path=None, filename=None):
    try:
     
        filename = "".join([c for c in filename if c.isalpha() or c.isdigit() or c == ' ' or c == '-']).rstrip()
        
        if output_path is None:
            output_path = os.getcwd()
            
        
        file_path = os.path.join(output_path, f"{filename}.mp3")
        if os.path.exists(file_path):
            return None
            
        url = f"https://www.youtube.com/watch?v={video_id}"
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        
        if filename is None:
            filename = yt.title
        
        audio_file = audio_stream.download(output_path=output_path, filename=f"{filename}.mp3")
        return audio_file
    
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"Error downloading audio: {str(e)}")


def askSaveFolder():
    folder = filedialog.askdirectory()
    if folder:
        return folder
    else:
        return os.getcwd()
