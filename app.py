import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Connect to the database
def get_connection():
    return sqlite3.connect("data/personal.db")

# Load data from database
@st.cache_data
def load_tracks():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM tracks", conn)
    conn.close()
    return df

@st.cache_data
def load_artists():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM artists", conn)
    conn.close()
    return df

# Page config
st.set_page_config(page_title="Personal Dashboard", layout="wide")

# Title
st.title("🎵 Music Dashboard")
st.markdown("Insights from your Spotify listening history")

# Load data
tracks_df = load_tracks()
artists_df = load_artists()

# --- Row 1: Key numbers ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Plays", len(tracks_df))

with col2:
    total_minutes = tracks_df["duration_minutes"].sum().round(1)
    st.metric("Total Listening Time", f"{total_minutes} mins")

with col3:
    unique_artists = tracks_df["artist"].nunique()
    st.metric("Unique Artists", unique_artists)

# --- Row 2: Charts ---
st.subheader("Your Top Artists")
top_artists = tracks_df["artist"].value_counts().head(10).reset_index()
top_artists.columns = ["artist", "plays"]
fig1 = px.bar(top_artists, x="plays", y="artist", orientation="h",
              color="plays", color_continuous_scale="purples")
fig1.update_layout(yaxis=dict(autorange="reversed"))
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Listening by Hour of Day")
hourly = tracks_df["hour_of_day"].value_counts().sort_index().reset_index()
hourly.columns = ["hour", "plays"]
fig2 = px.bar(hourly, x="hour", y="plays", color="plays",
              color_continuous_scale="purples")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Listening by Day of Week")
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
daily = tracks_df["day_of_week"].value_counts().reindex(day_order).reset_index()
daily.columns = ["day", "plays"]
fig3 = px.bar(daily, x="day", y="plays", color="plays",
              color_continuous_scale="purples")
st.plotly_chart(fig3, use_container_width=True)