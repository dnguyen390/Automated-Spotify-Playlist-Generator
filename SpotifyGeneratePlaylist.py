import json
import requests
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import youtube_dl
from exceptions import ResponseException
from secrets import spotify_user_id
class CreatePlaylist:

    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token =spotify.token
        self.youtube_client = self.get youtube client()
        self.all_song_info = {}
    # Step 1: Log Into YouTube   
    def get_youtube_client(self):
        # copied from YouTube data API
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client


    # Step 2: Open Liked Videos Tab
    def get_liked_videos(self):
        request = self.youtube_client.videos().list(
        part ="snippet,contentDetails,statistics",
        myRating="like"
        )
        response = request.execute()

        # collect each video and get important information
        for item in response["items"]:
            video_title = item["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(item["id"])

            # use youtube_dl to collect the song name & artist name
            video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=false)
            song_name = video["track"]
            artist = video["artist"]

            # save all important info
            self.all_song_info [video_title]={
                "youtube_url":youtube_url,
                "song_name":song_name
                "artist":artist,

                #add the uri, easy to get song to put into playlist
                "spotify_uri":self.get_spotify_uri(song_name,artist)
            }


    # Step 3: Create A New Playlist
    def create_playlist(self):
        request_body = json.dumps({
            "name":"YouTube Liked Videos",
            "description": "All liked YouTube Videos",
            "public":true
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format()
        response = requests.post (
            query,
            data=request_body,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json
        # playlist id
        return response_json["id"]

    # Step 4: Search for Song on Spotify
    def get_spotify_uri(self, song_name, track, artist):
        
        query ="https://api.spotify.com/v1/search?query=track%3A{}&track&offset=0&limit=20".format(
            song name,
            artist

        )
        response = request.get(
            query,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json
        songs = response.json["tracks"]["items"]
        # only use the first song
        url = songs[0]["url"]

    # Step 5: Add the song into the new Spotify playlist
    def add_song_to_playlist(self):
        # populate out songs dictionary
        self.get_liked_videos()
        
        # collect all of uri
        uri = []
        for song,info in self.all_song_info.items():
            uri.append(info["spotify_uri"])

        #create a new playlist
        playlist_id = self.create_playlist()


        #add all of songs into new playlist

        request_data = json.dumps(uris)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

        response= request.post(
            query,
            data=request_data,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()
        return response_json