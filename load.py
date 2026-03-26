import sqlite3
import pandas as pd
import os

def get_connection():
    # Connect to SQLite database (creates the file if it doesn't exist)
    conn = sqlite3.connect("data/personal.db")
    return conn

def load_tracks(df):
    print("Loading tracks into database...")
    conn = get_connection()
    
    # Write the DataFrame to a table called "tracks"
    # if_exists="replace" means wipe and rewrite the table each time
    df.to_sql("tracks", conn, if_exists="replace", index=False)
    
    print(f"Loaded {len(df)} tracks into 'tracks' table")
    conn.close()

def load_artists(df):
    print("Loading artists into database...")
    conn = get_connection()
    
    df.to_sql("artists", conn, if_exists="replace", index=False)
    
    print(f"Loaded {len(df)} artists into 'artists' table")
    conn.close()

def load_health(df):
    print("Loading health data into database...")
    conn = get_connection()
    
    df.to_sql("health", conn, if_exists="replace", index=False)
    
    print(f"Loaded {len(df)} health records into 'health' table")
    conn.close()

def verify_load():
    print("\nVerifying database contents...")
    conn = get_connection()
    
    tracks_count = pd.read_sql("SELECT COUNT(*) as count FROM tracks", conn)
    artists_count = pd.read_sql("SELECT COUNT(*) as count FROM artists", conn)
    health_count = pd.read_sql("SELECT COUNT(*) as count FROM health", conn)
    
    print(f"Tracks table: {tracks_count['count'][0]} rows")
    print(f"Artists table: {artists_count['count'][0]} rows")
    print(f"Health table: {health_count['count'][0]} rows")
    conn.close()

from extract import get_recently_played, get_top_artists, get_health_data
from transform import transform_tracks, transform_artists, transform_health

tracks = get_recently_played()
artists = get_top_artists()
health = get_health_data()

tracks_df = transform_tracks(tracks)
artists_df = transform_artists(artists)
health_df = transform_health(health)

load_tracks(tracks_df)
load_artists(artists_df)
load_health(health_df)

verify_load()