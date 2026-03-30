# Personal Analytics Dashboard

An end-to-end personal analytics dashboard built with Python, Streamlit, and SQLite — combining Spotify listening history and Apple Health data into a single interactive dashboard.

## What it does

This project pulls data from two sources, runs it through a custom ETL pipeline, stores it in a local database, and visualizes it across three pages:

- **Music Dashboard** — top artists, listening patterns by hour and day of week, total listening time
- **Fitness Dashboard** — daily steps, heart rate trends, and exercise minutes over time from Apple Watch data
- **Correlations** — cross-dataset analysis merging both sources to find patterns between music habits and fitness metrics

## Tech Stack

- **Python** — core language
- **Pandas** — data transformation and analysis
- **Streamlit** — interactive dashboard
- **Plotly** — charts and visualizations
- **SQLite** — local data warehouse
- **Spotify Web API** — listening history and top artists (via spotipy)
- **Apple Health XML** — fitness data export parser

## ETL Pipeline

The pipeline is split into three modular files:

- `extract.py` — pulls from the Spotify API (OAuth2) and parses Apple Health XML exports
- `transform.py` — cleans timestamps, converts units, reshapes data into structured DataFrames
- `load.py` — loads all data into a SQLite database for persistent storage

## Setup

1. Clone the repo
2. Install dependencies:
```
   pip install -r requirements.txt
```
3. Create a `.env` file with your Spotify credentials:
```
   SPOTIFY_CLIENT_ID=your_id
   SPOTIFY_CLIENT_SECRET=your_secret
   SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
```
4. Export your Apple Health data from the iPhone Health app and place `export.xml` in the `data/` folder
5. Run the pipeline:
```
   python load.py
```
6. Launch the dashboard:
```
   python -m streamlit run app.py
```

## Project Structure
```
personal-dashboard/
├── extract.py        # Data extraction from Spotify API + Apple Health XML
├── transform.py      # Data cleaning and transformation
├── load.py           # Loads cleaned data into SQLite
├── app.py            # Main Streamlit dashboard (Music page)
├── pages/
│   ├── 1_fitness.py        # Fitness trends page
│   └── 2_correlations.py   # Cross-dataset correlation analysis
├── data/             # SQLite database (gitignored)
├── .env              # Spotify credentials (gitignored)
└── requirements.txt
```
