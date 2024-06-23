import streamlit as st
from streamlit_webrtc import webrtc_streamer

st.title("Webcam Live Feed")

webrtc_streamer(key="example")
