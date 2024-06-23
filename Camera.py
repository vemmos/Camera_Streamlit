import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import cv2
import numpy as np
from openai import OpenAI
import os
import json

OPENAI_API_KEY = ""
MODEL = "gpt-3.5-turbo"
client = OpenAI(api_key=OPENAI_API_KEY)

#This function gets the ChatGPT response
def askCHATGPT(food, diet):
  response = client.chat.completions.create(
      model=MODEL,
      messages=[
          {"role": "system", "content": "What are the ingredients in "+ food + "?"},
      ],
      temperature=0,
  )

  responseJSON = json.dumps(json.loads(response.model_dump_json()), indent=4)
  response_dict = json.loads(responseJSON)
  answer = response_dict["choices"][0]["message"]["content"]

  response = client.chat.completions.create(
      model=MODEL,
      messages=[
          {"role": "system", "content": "Can I eat " + food + " if I have " + diet + "? Answer in under 20 words."},
      ],
      temperature=0,
  )
  responseJSON = json.dumps(json.loads(response.model_dump_json()), indent=4)
  response_dict = json.loads(responseJSON)
  answer = response_dict["choices"][0]["message"]["content"]
  return answer

class VideoProcessor(VideoTransformerBase):
    def __init__(self) -> None:
        self.image = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        self.image = img
        return img

def classify_image(image):
    return "Sample Classification Result"

def main():
    st.title('Briefly tell us about your dietary restrictions or how you would like to eat healthier')

    # Initialize or increment a form counter
    if 'form_counter' not in st.session_state:
        st.session_state.form_counter = 0

    form_key = f"diet_form_{st.session_state.form_counter}"

    # Manage the state to see if the form has been submitted
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    # Display the form if it hasn't been submitted
    if not st.session_state.submitted:
        with st.form(key=form_key):
            user_query = st.text_input("")

            submitted = st.form_submit_button("Submit and take a pic")
            if submitted:
                st.session_state.submitted = True
                st.session_state.form_counter += 1  # Increment the counter after submission

    # Display camera and image
    if st.session_state.submitted:
        st.header("Camera Feed")
        ctx = webrtc_streamer(key="example", video_processor_factory=VideoProcessor)
        if ctx.video_processor:
            if st.button("Take a pic"):
                if ctx.video_processor.image is not None:
                    st.session_state.captured_image = ctx.video_processor.image
                    classification_result = classify_image(ctx.video_processor.image)


        if 'captured_image' in st.session_state and st.session_state.captured_image is not None:
            col1, col2 = st.columns(2)
            with col1:
                st.image(st.session_state.captured_image, channels="BGR", caption="Chocolate Croissant")
            with col2:
                st.write("", askCHATGPT("Chocolate Croissant","Vegan"))

                

if __name__ == "__main__":
    main()
