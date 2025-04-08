# Spotify Downloader

A simple Python tool to download music from Spotify playlists and albums.

## Description

This program allows you to download tracks from Spotify playlists and albums by finding and downloading the same tracks from YouTube. It's a straightforward utility for personal use.

## Features

- Download tracks from Spotify playlists and albums
- Automatic YouTube search and download
- Progress tracking
- Skips already downloaded tracks
- User-friendly GUI interface
- Batch download support

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the program:
```
python main.py
```

The GUI interface will allow you to:
1. Enter Spotify playlist or album URLs
2. Select a folder to save the downloaded tracks
3. Monitor download progress in real-time
4. Manage multiple download tasks

## Requirements

- Python 3.x
- Dependencies listed in requirements.txt

## API Configuration

To use this Spotify downloader, you need to set up API keys for Spotify. Follow these steps:

1. **Spotify API**:
   - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
   - Create an application or use an existing one.
   - Note down the `Client ID` and `Client Secret`.
   - Add a redirect URI (e.g., http://localhost:8888/callback).

2. **Configure API Keys as Environment Variables**:
   - Set the following environment variables on your system:
     ```
     SPOTIFY_CLIENT_ID=your_spotify_client_id
     SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
     ```
   - Replace `your_spotify_client_id` and `your_spotify_client_secret` with your actual API keys.

   **On Linux/macOS**:
   ```bash
   export SPOTIFY_CLIENT_ID="your_spotify_client_id"
   export SPOTIFY_CLIENT_SECRET="your_spotify_client_secret"
   ```

   **On Windows (Command Prompt)**:
   ```cmd
   set SPOTIFY_CLIENT_ID=your_spotify_client_id
   set SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   ```

   **On Windows (PowerShell)**:
   ```powershell
   $env:SPOTIFY_CLIENT_ID="your_spotify_client_id"
   $env:SPOTIFY_CLIENT_SECRET="your_spotify_client_secret"
   ```

   To make these environment variables permanent, add them to your shell profile or system environment variables.

## Note

This is a simple utility that may be updated or modified in the future. Use responsibly and in accordance with applicable terms of service.
