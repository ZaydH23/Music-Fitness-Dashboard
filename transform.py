import pandas as pd
from datetime import datetime

def transform_tracks(tracks):
    print("Transforming tracks...")
    
    # Convert the list of track dictionaries into a DataFrame
    # A DataFrame is like a spreadsheet — rows and columns
    df = pd.DataFrame(tracks)
    
    # Convert played_at from a string to a proper datetime object
    df["played_at"] = pd.to_datetime(df["played_at"])
    
    # Extract useful time components
    df["hour_of_day"] = df["played_at"].dt.hour
    df["day_of_week"] = df["played_at"].dt.day_name()
    df["date"] = df["played_at"].dt.date
    
    # Convert duration from milliseconds to minutes
    df["duration_minutes"] = (df["duration_ms"] / 60000).round(2)
    
    # Drop the original columns we no longer need
    df = df.drop(columns=["duration_ms"])
    
    print(f"Transformed {len(df)} tracks")
    return df

def transform_artists(artists):
    print("Transforming artists...")
    
    df = pd.DataFrame(artists)
    
    # Genres comes in as a list e.g. ['hip hop', 'rap']
    # Convert it to a simple comma separated string e.g. 'hip hop, rap'
    df["genres"] = df["genres"].apply(lambda x: ", ".join(x) if x else "unknown")
    
    # Add a rank column based on position in the list
    # Position 0 = your #1 top artist
    df["rank"] = range(1, len(df) + 1)
    
    print(f"Transformed {len(df)} artists")
    return df

def transform_health(records):
    print("Transforming health data...")
    
    df = pd.DataFrame(records)
    
    # Clean up the date format (remove the timezone offset like -0400)
    df["start_date"] = df["start_date"].str.replace(r' [+-]\d{4}$', '', regex=True)
    df["start_date"] = pd.to_datetime(df["start_date"])
    
    # Extract date components
    df["date"] = df["start_date"].dt.date
    df["hour"] = df["start_date"].dt.hour
    df["month"] = df["start_date"].dt.month
    df["year"] = df["start_date"].dt.year
    
    # Round values to 1 decimal place
    df["value"] = df["value"].round(1)
    
    print(f"Transformed {len(df)} health records")
    return df

