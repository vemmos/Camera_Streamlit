import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import av

# Streamlit page configuration
st.set_page_config(page_title='Dietary and Camera App', layout='wide')

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

class VideoTransformer(VideoTransformerBase):
    def transform(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        # Apply any OpenCV transformations or filters here
        return av.VideoFrame.from_ndarray(img, format="bgr24")

def main():
    st.title('Dietary Restrictions Form')
    if 'page' not in st.session_state:
        st.session_state.page = 'form'

    if st.session_state.page == 'form':
        with st.form("diet_form"):
            allergies = st.text_input("List any allergies")
            preferences = st.text_input("Dietary preferences (e.g., vegetarian, low-carb)")
            submitted = st.form_submit_button("Submit")

        if submitted:
            st.session_state.page = 'camera'
            st.rerun()

    elif st.session_state.page == 'camera':
        st.title("Live Camera Feed with OpenCV")
        webrtc_streamer(
            key="example",
            video_frame_callback=VideoTransformer(),
            rtc_configuration=RTC_CONFIGURATION,
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True
        )

if __name__ == "__main__":
    main()
