from utils import *
import os

def start_main_download_process(linksToDownload, savePath):
    totalTracks = 0
    totalTracksDownloaded = 0

    for link in linksToDownload:
        playlist_id = extract_playlist_id(link)
        tracks = get_playlist_tracks(playlist_id, type=get_type(link))
        totalTracks += len(tracks)

    print(f"downloading {totalTracks} tracks")

    for link in linksToDownload:
        
        playlist_id = extract_playlist_id(link)
        tracks = get_playlist_tracks(playlist_id, type=get_type(link))
        type = get_type(link)
        formatted_array = format_for_yt(type, playlist_id, tracks)


        for i in formatted_array:
            
            filename1 = "".join([c for c in i if c.isalpha() or c.isdigit() or c == ' ' or c == '-']).rstrip()
            file_path = os.path.join(savePath, f"{filename1}.mp3")
            if os.path.exists(file_path):
        
                totalTracksDownloaded += 1
                print(f"{(totalTracksDownloaded/totalTracks)*100:.2f}% complete", end='\r', flush=True)
                continue
            else:
                try:
                    filename = "".join([c for c in i if c.isalpha() or c.isdigit() or c == ' ' or c == '-']).rstrip()
                    file_path = os.path.join(savePath, f"{filename}.mp3")
                    
                    video_id = fetch_yt_results(str(i), 1)[0]
                    download_youtube_audio(video_id=video_id, output_path=savePath, filename=str(i))
                except:
                    print(f"error while downloading: {i}")
                    pass
            totalTracksDownloaded += 1
            print(f"{(totalTracksDownloaded/totalTracks)*100:.2f}% complete", end='\r', flush=True)




def main():
    linksToDownload = []
    savePath = askSaveFolder()
    
    while True:
        link = input("Enter a Spotify playlist link (or 'done' to finish): ")
        if link.lower() == 'done':
            break
        linksToDownload.append(link)
    
    if not savePath:
        savePath = os.getcwd()

    start_main_download_process(linksToDownload, savePath)
        

if __name__ == "__main__":
    main()

