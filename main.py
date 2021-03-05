import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


SPOTIFY_ID = os.environ["SPOTIFY_ID"]
SPOTIFY_SECRET = os.environ["SPOTIFY_SECRET"]
REDIRECT_UR_SPOTIFY = "http://example.com"


year_travel = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

# _________________________________________________ TOP 100 MUSIC _________________________________________________ #

url = f"https://www.billboard.com/charts/hot-100/{year_travel}"

response = requests.get(url=url)
response.raise_for_status()
website_date = response.text

soup = BeautifulSoup(website_date, "html.parser")
songs = [song.get_text() for song in soup.find_all(
    name="span",
    class_="chart-element__information__song text--truncate color--primary"
)]

# _________________________________________________ SPOTIFY MACHINE _________________________________________________ #

# Authentication:

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_ID,
                                               client_secret=SPOTIFY_SECRET,
                                               redirect_uri=REDIRECT_UR_SPOTIFY,
                                               scope="playlist-modify-public"
                                               ))
user_id = sp.me()["id"]

# Get the URIS of the songs:

song_uris = []

for song in songs:
    search_song = sp.search(q=f"track: {song} year: {int(year_travel[:4])}")

    for index in range(len(search_song["tracks"]["items"])):
        track = search_song["tracks"]["items"][index]["name"]
        if track == song:
            uri = search_song["tracks"]["items"][index]["uri"]
            song_uris.append(uri)
            break

# Create Playlist
create_playlist = sp.user_playlist_create(user_id, name=f"{year_travel} Billboard 100")
playlist_id = create_playlist["id"]

# Add Tracks
add_track = sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)

print(add_track)
print(create_playlist)

