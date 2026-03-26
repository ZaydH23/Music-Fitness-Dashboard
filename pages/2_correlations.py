import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Correlations", layout="wide")

def get_connection():
    return sqlite3.connect("data/personal.db")

@st.cache_data
def load_data():
    conn = get_connection()
    tracks_df = pd.read_sql("SELECT * FROM tracks", conn)
    health_df = pd.read_sql("SELECT * FROM health", conn)
    conn.close()
    
    tracks_df["date"] = pd.to_datetime(tracks_df["date"])
    health_df["date"] = pd.to_datetime(health_df["date"])
    return tracks_df, health_df

st.title("🔍 Correlations")
st.markdown("Finding patterns between your music and fitness data")

tracks_df, health_df = load_data()

# --- Build a daily summary combining both datasets ---

# Music: count plays and total minutes per day
daily_music = tracks_df.groupby("date").agg(
    plays=("track_name", "count"),
    listening_minutes=("duration_minutes", "sum")
).reset_index()

# Steps: total per day
daily_steps = health_df[health_df["type"] == "steps"].groupby("date")["value"].sum().reset_index()
daily_steps.columns = ["date", "steps"]

# Heart rate: average per day
daily_hr = health_df[health_df["type"] == "heart_rate"].groupby("date")["value"].mean().reset_index()
daily_hr.columns = ["date", "avg_heart_rate"]

# Exercise: total per day
daily_ex = health_df[health_df["type"] == "exercise_minutes"].groupby("date")["value"].sum().reset_index()
daily_ex.columns = ["date", "exercise_minutes"]

# Merge everything into one daily summary dataframe
daily = daily_music.merge(daily_steps, on="date", how="inner")
daily = daily.merge(daily_hr, on="date", how="inner")
daily = daily.merge(daily_ex, on="date", how="inner")

st.subheader(f"Combined daily data: {len(daily)} days")

# --- Correlation heatmap ---
st.subheader("Correlation Matrix")
st.markdown("Shows how strongly each metric relates to the others. Closer to 1 or -1 = stronger relationship.")

corr = daily[["plays", "listening_minutes", "steps", "avg_heart_rate", "exercise_minutes"]].corr()
fig1 = px.imshow(corr, 
                 color_continuous_scale="RdBu",
                 zmin=-1, zmax=1,
                 text_auto=".2f")
st.plotly_chart(fig1, use_container_width=True)

# --- Scatter plots ---
st.subheader("Steps vs Listening Time")
fig2 = px.scatter(daily, x="listening_minutes", y="steps",
                  trendline="ols",
                  color_discrete_sequence=["#7F77DD"])
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Exercise Minutes vs Listening Time")
fig3 = px.scatter(daily, x="listening_minutes", y="exercise_minutes",
                  trendline="ols",
                  color_discrete_sequence=["#1D9E75"])
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Heart Rate vs Steps")
fig4 = px.scatter(daily, x="steps", y="avg_heart_rate",
                  trendline="ols",
                  color_discrete_sequence=["#D85A30"])
st.plotly_chart(fig4, use_container_width=True)