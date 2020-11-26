from hashtable import HashTable
from spotipy.oauth2 import SpotifyClientCredentials
import requests, shelve, spotipy

# returns a list of all track objects from a playlist
def getTracks(playlist_url, sp):
    allTracks = []
    if 'https://open.spotify.com/user/' in playlist_url:

        playlist_user = playlist_url.split('user/')[1].split('/')[0]
        playlist_id = playlist_url.split('playlist/')[1]

    else:
        playlist_user = playlist_url.split(':')[0]
        playlist_id = playlist_url.split(':')[-1]
    
    playlist = sp.user_playlist(playlist_user, playlist_id)

    results = sp.user_playlist(playlist_user, playlist['id'], fields="tracks,next")
    tracks = results['tracks']
    for track in tracks['items']:
        allTracks.append(Song(track['track']))

    while tracks['next']:
        tracks = sp.next(tracks)
        for track in tracks['items']:
            allTracks.append(Song(track['track']))

    return allTracks, playlist['name']

#class for spotify track
class Song():
    def __init__(self, track):
        self.track = track
        self.name = track['name']
        self.name_file = track['name'].replace(':','').replace('?','').replace(';','').replace('<','').replace('>','').replace('*','').replace('|','').replace('/','').replace('\\','').replace('"','').replace('‘','\'').replace('á','a').replace('à','a').replace('ù','u').replace('Ä','A').replace("’","'")
        self.artists = [artist['name'] for artist in track['artists']]
        self.duration = int(track['duration_ms']/1000)
        dur_mins = str(float(track['duration_ms']/1000/60)).split('.')
        self.duration_mins = dur_mins[0] + ':' + str(float('0.'+ dur_mins[1])*60).split('.')[0]
        self.album = track['album']['name']
        self.art_urls = [art['url'] for art in track['album']['images']]
        self.uri = track['uri']

info_file = "spotify_api.txt"
f = open(info_file)
client_id = f.readline().split(':')[1].strip()
client_secret = f.readline().split(':')[1].strip()
f.close()

# spotify verification
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_file = "playlists.txt"
f = open(playlist_file)
playlist_urls = [line.split('#')[0].strip() for line in f.read().split('\n')]
key_value_pairs = []
for url in playlist_urls:
    tracks, playlist_name = getTracks(url, sp)
    for track in tracks:
        key = track.name.lower().replace(' ','') + '_' + track.artists[0].lower().replace(' ','')
        value = playlist_name
        key_value_pairs.append((key, value))

shelf = shelve.open("hashtable", "n")
tablesize = int(len(key_value_pairs)/0.5)
hashtable = HashTable(tablesize)

for pair in key_value_pairs:
    hashtable.store_pair(pair[0],pair[1])

shelf['hashtable'] = hashtable
shelf.close()
print(hashtable)
print('Done')

