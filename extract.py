import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="user-read-recently-played user-top-read"
))

def get_recently_played():
    print("Fetching recently played tracks...")
    results = sp.current_user_recently_played(limit=50)
    
    tracks = []
    for item in results["items"]:
        track = {
            "track_name": item["track"]["name"],
            "artist": item["track"]["artists"][0]["name"],
            "album": item["track"]["album"]["name"],
            "played_at": item["played_at"],
            "duration_ms": item["track"]["duration_ms"]
        }
        tracks.append(track)
    
    print(f"Got {len(tracks)} tracks")
    return tracks

def get_top_artists():
    print("Fetching top artists...")
    results = sp.current_user_top_artists(limit=20, time_range="medium_term")
    
    artists = []
    for item in results["items"]:
        artist = {
            "name": item.get("name", "Unknown"),
            "genres": item.get("genres", []),
            "popularity": item.get("popularity", 0),
            "followers": item.get("followers", {}).get("total", 0)
        }
        artists.append(artist)
    
    print(f"Got {len(artists)} artists")
    return artists

import xml.etree.ElementTree as ET

def get_health_data():
    print("Parsing Apple Health data...")
    
    tree = ET.parse("data/export.xml")
    root = tree.getroot()
    
    # The types we want to extract
    wanted_types = {
        "HKQuantityTypeIdentifierStepCount": "steps",
        "HKQuantityTypeIdentifierHeartRate": "heart_rate",
        "HKQuantityTypeIdentifierAppleExerciseTime": "exercise_minutes"
    }
    
    records = []
    for record in root.findall("Record"):
        record_type = record.get("type")
        
        if record_type in wanted_types:
            records.append({
                "type": wanted_types[record_type],
                "start_date": record.get("startDate"),
                "value": float(record.get("value", 0))
            })
    
    print(f"Found {len(records)} health records")
    return records
