import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytubefix import YouTube
from tkinter import filedialog
import os
import time
import logging
from pydub import AudioSegment
import subprocess


current_progress = 0

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler('errors.log')
    ]
)

logger = logging.getLogger("errors")

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

if not client_id or not client_secret:
    print("SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET must be set as environment variables.")
    exit()

try:
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
except Exception as ex:
    print("error in authentication, check log")
    logger.error(f"ERROR IN AUTHENTICATION, ENSURE CORRECT CREDS. ERROR: {ex}")
    exit()



def get_current_progress():
    return current_progress

def start_main_download_process(linksToDownload, savePath, output_callback=None):
    global current_progress
    current_progress = 0
    all_tracks = []
    

    def safe_output(msg):
        if output_callback:
            output_callback(msg)
        else:
            print(msg)
            
    safe_output(f"Processing {len(linksToDownload)} links")
    

    for link in linksToDownload:
        playlist_id = extract_playlist_id(link)
        playlist_type = get_type(link)
        safe_output(f"Getting tracks from {playlist_type} {playlist_id}")
        tracks = get_playlist_tracks(playlist_id, type=playlist_type)
        
        for track in tracks:
            all_tracks.append({
                'track': track,
                'playlist_id': playlist_id,
                'playlist_type': playlist_type
            })

    totalTracks = len(all_tracks)
    safe_output(f"Found {totalTracks} total tracks to process")


    for i, track_info in enumerate(all_tracks):
        track = track_info['track']
        
        track_name = track['name']
        artist_name = track['artist']
        display_name = f"{track_name} by {artist_name}"
        
        filename = "".join([c for c in display_name if c.isalpha() or c.isdigit() or c == ' ' or c == '-']).rstrip()
        file_path = os.path.join(savePath, f"{filename}")
        
        if os.path.exists(file_path):
            safe_output(f"File already exists, skipping: {display_name}")
        else:
            try:
                safe_output(f"Downloading: {display_name}")
                search_results = fetch_yt_results(f"{track_name} {artist_name} audio", limit=1)
                if search_results and len(search_results) > 0:
                    download_youtube_audio(search_results[0], savePath, filename, safe_output)
            except Exception as e:
                safe_output(f"Error downloading {display_name}: {str(e)}")

        current_progress = min(100, int((i+1)/totalTracks*100))

def fetch_yt_results(query, limit=5):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }
    
    try:
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
            video_ids = [entry['id'] for entry in search_results['entries']]
            return video_ids
    except Exception as ex:
        print("there was an error in yt_dlp search")
        logger.error(f"ERROR IN YT_DLP SEARCH: {ex}. check error log")
        exit()

def extract_playlist_id(playlist_url):
    if 'spotify.com/playlist/' in playlist_url:
        playlist_id = playlist_url.split('playlist/')[1].split('?')[0]
        return playlist_id
    elif 'spotify.com/album/' in playlist_url:
        playlist_id = playlist_url.split("album/")[1].split("?")[0]
        return playlist_id
    else:
        return None


def get_type(playlist_url):
    if 'spotify.com/playlist/' in playlist_url:
        return "playlist"
        
    elif 'spotify.com/album/' in playlist_url:
        return "album"

    else:
        return None

def get_playlist_tracks(playlist_id, type):
    tracks = []
    
    try:
        if type == "playlist":
            results = sp.playlist_items(playlist_id, limit=100)
            
            if results != None:
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
            else:
                print(f"no tracks in playlist {playlist_id}")
                logger.error("no results found")
                return []

        elif type == "album":

            results = sp.album_tracks(playlist_id, limit=50)
            if results != None:
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
            else:
                print(f"no tracks in album {playlist_id}")
                logger.error("no results found")
                return []
        return tracks
    except Exception as ex:
        

        print("there was an error while fetching playlist tracks from spotify API. check error log")
        logger.error(f"error in fetching tracks: {ex}")
        return []  

def format_for_yt(type, id, raw):
    formatted_search_query = []
    tracks = get_playlist_tracks(id, type)
    return [f"{track['name']} by {track['artist']}" for track in tracks]

def download_youtube_audio(video_id, output_path=None, filename=None, output_callback=None):
    try:
        filename = "".join([c for c in filename if c.isalpha() or c.isdigit() or c == ' ' or c == '-']).rstrip()
        
        if output_path is None:
            output_path = os.getcwd()
        
        file_path = os.path.join(output_path, f"{filename}")
        if os.path.exists(file_path):
            if output_callback:
                output_callback(f"File already exists: {file_path}")
            return None
        
        url = f"https://www.youtube.com/watch?v={video_id}"
        
       
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': file_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if output_callback:
            output_callback(f"Downloaded and saved as MP3: {file_path}")
        else:
            print(f"Downloaded and saved as MP3: {file_path}")
        
        return file_path
    
    except KeyboardInterrupt:
        print("Keyboard interrupt detected, exiting")
        exit()
    except Exception as ex:
        print(f"Error downloading audio. Check log.")
        logger.error(f"Error downloading: {ex}")

def askSaveFolder():
    folder = filedialog.askdirectory()
    if folder:
        return folder
    else:
        return os.getcwd()
