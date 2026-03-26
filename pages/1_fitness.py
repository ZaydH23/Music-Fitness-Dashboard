import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Fitness Dashboard", layout="wide")

def get_connection():
    return sqlite3.connect("data/personal.db")

@st.cache_data
def load_health():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM health", conn)
    conn.close()
    df["date"] = pd.to_datetime(df["date"])
    return df

st.title("💪 Fitness Dashboard")
st.markdown("Insights from your Apple Watch data")

health_df = load_health()

# Split into separate dataframes by type
steps_df = health_df[health_df["type"] == "steps"]
heart_df = health_df[health_df["type"] == "heart_rate"]
exercise_df = health_df[health_df["type"] == "exercise_minutes"]

# --- Row 1: Key numbers ---
col1, col2, col3 = st.columns(3)

with col1:
    avg_steps = steps_df.groupby("date")["value"].sum().mean()
    st.metric("Avg Daily Steps", f"{avg_steps:,.0f}")

with col2:
    avg_heart = heart_df["value"].mean()
    st.metric("Avg Heart Rate", f"{avg_heart:.0f} bpm")

with col3:
    avg_exercise = exercise_df.groupby("date")["value"].sum().mean()
    st.metric("Avg Daily Exercise", f"{avg_exercise:.0f} mins")

# --- Charts ---
st.subheader("Daily Steps Over Time")
daily_steps = steps_df.groupby("date")["value"].sum().reset_index()
daily_steps.columns = ["date", "steps"]
fig1 = px.line(daily_steps, x="date", y="steps", color_discrete_sequence=["#7F77DD"])
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Heart Rate Over Time")
daily_hr = heart_df.groupby("date")["value"].mean().reset_index()
daily_hr.columns = ["date", "heart_rate"]
fig2 = px.line(daily_hr, x="date", y="heart_rate", color_discrete_sequence=["#D85A30"])
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Exercise Minutes Over Time")
daily_ex = exercise_df.groupby("date")["value"].sum().reset_index()
daily_ex.columns = ["date", "exercise_minutes"]
fig3 = px.bar(daily_ex, x="date", y="exercise_minutes", color_discrete_sequence=["#1D9E75"])
st.plotly_chart(fig3, use_container_width=True)