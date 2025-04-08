from utils import *
import os

def start_main_download_process(linksToDownload, savePath):
    all_tracks = []
    for link in linksToDownload:
        playlist_id = extract_playlist_id(link)
        playlist_type = get_type(link)
        tracks = get_playlist_tracks(playlist_id, type=playlist_type)
        
        for track in tracks:
            all_tracks.append({
                'track': track,
                'playlist_id': playlist_id,
                'playlist_type': playlist_type
            })

    totalTracks = len(all_tracks)
    print(f"downloading {totalTracks} tracks")

    for i, track_info in enumerate(all_tracks):
        track = track_info['track']
        playlist_id = track_info['playlist_id']
        playlist_type = track_info['playlist_type']
        
        filename1 = "".join([c for c in track if c.isalpha() or c.isdigit() or c == ' ' or c == '-']).rstrip()
        file_path = os.path.join(savePath, f"{filename1}.mp3")
        if os.path.exists(file_path):
            print(f"{(i+1)/totalTracks*100:.2f}% complete", end='\r', flush=True)
            continue
        else:
            try:
                filename = "".join([c for c in track if c.isalpha() or c.isdigit() or c == ' ' or c == '-']).rstrip()
                file_path = os.path.join(savePath, f"{filename}.mp3")
                
                video_id = fetch_yt_results(str(track), 1)[0]
                download_youtube_audio(video_id=video_id, output_path=savePath, filename=str(track))
            except:
                print(f"error while downloading: {track}")
                pass
        print(f"{(i+1)/totalTracks*100:.2f}% complete", end='\r', flush=True)


def main():
    linksToDownload = []
    savePath = askSaveFolder()
    
    while True:
        link = input("Enter an album/playlist link (or 'done' to finish): ")

        if link.lower() == 'done':
            break
    
        if not ("album" in link.lower() or "playlist" in link.lower()) and link.lower() != "done":
            print("invalid URL.")
        else:
            linksToDownload.append(link)



    
    if not savePath:
        savePath = os.getcwd()

    start_main_download_process(linksToDownload, savePath)
        

if __name__ == "__main__":
    main()

