import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import numpy as np
import av

st.title("OpenCV Filters on Video Stream")

# You had 'filter = "none"' but it is not being used, so it can be removed
# unless you plan to add filtering options later.

def transform(frame: av.VideoFrame):
    img = frame.to_ndarray(format="bgr24")
    # Here you can apply any transformations or filters to the img
    return av.VideoFrame.from_ndarray(img, format="bgr24")

# Initialize the webcam streamer
webrtc_streamer(
    key="streamer",
    video_frame_callback=transform,
    sendback_audio=False  # Audio is not sent back to the browser
)
