import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv("AustraliaWildfires.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month_name()
    df['Year'] = df['Date'].dt.year
    return df

df = load_data()

st.title("🔥 Australia Wildfire Dashboard")

st.sidebar.header("Filter options")
region = st.sidebar.radio("Select Region", options=df["Region"].unique(), index=0)
year = st.sidebar.selectbox("Select Year", options=sorted(df["Year"].unique()))

filtered = df[(df['Region'] == region) & (df['Year'] == year)]

avg_fire_area = filtered.groupby("Month")["Estimated_fire_area"].mean().reset_index()
fig1 = px.pie(avg_fire_area, names="Month", values="Estimated_fire_area",
              title=f"{region} - Monthly Avg Estimated Fire Area ({year})")

avg_pixel_count = filtered.groupby("Month")["Count"].mean().reset_index()
fig2 = px.bar(avg_pixel_count, x="Month", y="Count",
              title=f"{region} - Monthly Avg Pixel Count ({year})")

st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
