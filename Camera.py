import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoHTMLAttributes
import numpy as np
import av

st.title("OpenCV Filters on Video Stream")

filter = "none"


def transform(frame: av.VideoFrame):
    img = frame.to_ndarray(format="bgr24")

    return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="streamer",
    video_frame_callback=transform,
    sendback_audio=False
    )
