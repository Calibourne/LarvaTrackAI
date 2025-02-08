import streamlit as st
import subprocess
import cv2 as cv
import tempfile
import shutil
import os

def video_upload():
    uploaded_file = st.file_uploader("Choose a video...", type=['mp4'])
    if uploaded_file is not None:
        # st.session_state.processing_done = False
        # with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
        #     tmp_file.write(uploaded_file.read())
        #     cap = cv.VideoCapture(tmp_file.name)
        #     length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
        #     # encode the video
        #     # avi / mov -> mp4
        # if not os.path.exists("temp"):
        #     os.mkdir("temp")
        # shutil.move(tmp_file.name, "temp/temp.mp4")
        # ffmpeg_cmd = f"ffmpeg -i temp/temp.mp4 -c:v libx264 -crf 23 -c:a aac -b:a 128k temp/temp_encoded.mp4"
        # subprocess.run(ffmpeg_cmd, shell=True)
        # shutil.move("temp/temp_encoded.mp4", "temp/temp.mp4")
        return "temp/temp.mp4", uploaded_file, None # length
    return None, None, None