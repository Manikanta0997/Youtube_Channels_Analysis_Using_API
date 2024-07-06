import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from googleapiclient.discovery import build

st.title("Enter Youtube Channel Id's")
st.write("To find the channel Id's use this https://www.streamweasels.com/tools/youtube-channel-id-and-user-id-convertor/ link")

num_fields = st.number_input(
    "How many input fields do you want to add?", min_value=1, max_value=100, value=1
)

input_values = []


def get_channel_info(youtube, channels_list):
    df = []
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics", id=",".join(channels_list)
    )
    request = request.execute()
    for i in range(len(request["items"])):
        x = dict(
            title=request["items"][i]["snippet"]["title"],
            video_count=request["items"][i]["statistics"]["videoCount"],
            subscriber_count=request["items"][i]["statistics"]["subscriberCount"],
            view_counts=request["items"][i]["statistics"]["viewCount"],
            channel_id=request["items"][i]["contentDetails"]["relatedPlaylists"][
                "uploads"
            ],
        )
        df.append(x)
    return pd.DataFrame(df)


for i in range(num_fields):
    input_values.append(st.text_input(f"Input field {i+1}"))

if st.button("Submit"):
    input_values = [value for value in input_values if value]

    st.write("List of inputs:", input_values)

    my_api_key = "AIzaSyDcDiUUGYzt9qPU3k8MKsTfmgjEY2G1fnQ"

    channels_list = input_values

    youtube = build("youtube", "v3", developerKey=my_api_key)

    x = get_channel_info(youtube, channels_list)

    numeric_cols = ["video_count", "subscriber_count", "view_counts"]

    x[numeric_cols] = x[numeric_cols].apply(pd.to_numeric, errors="coerce")

    st.write(x)

    st.header("Visualizations")

    # Bar chart of video counts
    st.subheader("Bar Chart of Video Counts")
    plt.figure(figsize=(10, 6))
    sns.barplot(x="title", y="video_count", data=x)
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Bar chart of subscriber counts
    st.subheader("Bar Chart of Subscriber Counts")
    plt.figure(figsize=(10, 6))
    sns.barplot(x="title", y="subscriber_count", data=x)
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Bar chart of view counts
    st.subheader("Bar Chart of View Counts")
    plt.figure(figsize=(10, 6))
    sns.barplot(x="title", y="view_counts", data=x)
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Scatter plot of subscriber counts vs. view counts
    st.subheader("Scatter Plot of Subscriber Counts vs. View Counts")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="subscriber_count", y="view_counts", data=x, hue="title")
    plt.xlabel("Subscriber Count")
    plt.ylabel("View Counts")
    st.pyplot(plt)

    # Pie chart of video counts distribution
    st.subheader("Pie Chart of Video Counts Distribution")
    plt.figure(figsize=(8, 8))
    plt.pie(x["video_count"], labels=x["title"], autopct="%1.1f%%", startangle=140)
    plt.axis("equal")
    st.pyplot(plt)

    # Correlation heatmap
    st.subheader("Correlation Heatmap")
    plt.figure(figsize=(10, 6))
    sns.heatmap(x[numeric_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f")
    st.pyplot(plt)
