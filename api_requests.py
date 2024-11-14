from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import json

def normalize_title(title):
    """
    Normalize the title by removing commas and extra spaces.
    """
    # Remove commas, dots, parentheses, and other unwanted characters
    for char in [',', '.', '(', ')', '?', "'", ':', '&', '’', '%', '!']:
        title = title.replace(char, '')
    # Replace multiple spaces with a single space
    title = ' '.join(title.split())
    return title.strip()

def get_track_stats(sp, track_id, name):
    """
    Get audio features for a track.
    """
    try:
        audio_features = sp.audio_features(track_id)[0]
        features = {
            "tempo": audio_features.get('tempo', 'Unknown'),
            "valence": audio_features.get('valence', 'Unknown'),
            "liveness": audio_features.get('liveness', 'Unknown'),
            "acousticness": audio_features.get('acousticness', 'Unknown'),
            "danceability": audio_features.get('danceability', 'Unknown'),
            "energy": audio_features.get('energy', 'Unknown'),
            "speechiness": audio_features.get('speechiness', 'Unknown'),
            "instrumentalness": audio_features.get('instrumentalness', 'Unknown'),
            "loudness": audio_features.get('loudness', 'Unknown'),
            "key": audio_features.get('key', 'Unknown'),
            "mode": audio_features.get('mode', 'Unknown'),
            "time_signature": audio_features.get('time_signature', 'Unknown')
        }
    except Exception as e:
        print(f"Error fetching track stats for {name}: {e}")
        features = {
            "tempo": 'Unknown',
            "valence": 'Unknown',
            "liveness": 'Unknown',
            "acousticness": 'Unknown',
            "danceability": 'Unknown',
            "energy": 'Unknown',
            "speechiness": 'Unknown',
            "instrumentalness": 'Unknown',
            "loudness": 'Unknown',
            "key": 'Unknown',
            "mode": 'Unknown',
            "time_signature": 'Unknown'
        }
    return features

def get_user_playlists(sp):
    """
    Get the current user's playlists.
    """
    return sp.current_user_playlists()

def get_artist_genre(sp, artist_id):
    """
    Get the genres for an artist using their Spotify artist ID.
    """
    try:
        artist_info = sp.artist(artist_id)
        genres = artist_info.get('genres', [])
        return genres if genres else ['Unknown']
    except Exception as e:
        print(f"Error fetching artist genre: {e}")
        return ['Unknown']

def get_playlist_tracks(sp, playlist_id):
    """
    Get all tracks from a given playlist.
    """
    tracks = []
    offset = 0
    limit = 100  # Number of tracks per request
    
    while True:
        # Fetch tracks with pagination
        results = sp.playlist_tracks(playlist_id, limit=limit, offset=offset)
        
        # Check if there are no more tracks
        if not results['items']:
            break
        
        for item in results['items']:
            track = item['track']
            artist_id = track['artists'][0]['id']
            song_id = track['id']
            
            print(song_id)
            
            track_info = get_track_stats(sp, str(song_id), track['name'])
            artist_genres = get_artist_genre(sp, artist_id)
            
            tracks.append({
                'name': normalize_title(track['name']),
                'artist': normalize_title(track['artists'][0]['name']),
                'id': track['id'],
                'genre': artist_genres[0] if artist_genres else 'Unknown',
                'tempo': track_info['tempo'],
                'valence': track_info['valence'],
                'liveness': track_info['liveness'],
                'acousticness': track_info['acousticness'],
                'danceability': track_info['danceability'],
                'energy': track_info['energy'],
                'speechiness': track_info['speechiness'],
                'instrumentalness': track_info['instrumentalness'],
                'loudness': track_info['loudness'],
                'key': track_info['key'], 
                'mode': track_info['mode'],
                'time_signature': track_info['time_signature']
            })
        
        # Move to the next page
        offset += limit
    
    return tracks
