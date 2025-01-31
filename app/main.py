import streamlit as st
from bg_removal import remove_background
import tempfile
import os
import cv2 as cv
import shutil
import time
import subprocess
from dotenv import load_dotenv

def video_upload():
    uploaded_file = st.file_uploader("Choose a video...", type=['mp4'])
    if uploaded_file is not None:
        st.session_state.processing_done = False
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            tmp_file.write(uploaded_file.read())
            cap = cv.VideoCapture(tmp_file.name)
            length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
            # encode the video
            # avi / mov -> mp4
        if not os.path.exists("temp"):
            os.mkdir("temp")
        shutil.move(tmp_file.name, "temp/temp.mp4")
        ffmpeg_cmd = f"ffmpeg -i temp/temp.mp4 -c:v libx264 -crf 23 -c:a aac -b:a 128k temp/temp_encoded.mp4"
        subprocess.run(ffmpeg_cmd, shell=True)
        shutil.move("temp/temp_encoded.mp4", "temp/temp.mp4")
        return "temp/temp.mp4", uploaded_file, length
    return None, None, None
        
load_dotenv()

LAB_LOGO = os.environ.get("LAB_LOGO")
UNI_LOGO = os.environ.get("UNI_LOGO")
INS_LOGO = os.environ.get("INS_LOGO")

st.set_page_config(
    page_title="LarvaTrackAI",
    page_icon="🐛",
    layout="wide",
    initial_sidebar_state="collapsed"
)

col_left, _ = st.columns([1, 3])  # Left for logos, right for spacing
with col_left:
    with st.container():
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center; 
                        gap: 20px; background-color: white; padding: 10px; 
                        border-radius: 10px; width: 100%;">
                <img src="{UNI_LOGO}" width="100">
                <img src="{LAB_LOGO}" width="100">
                <img src="{INS_LOGO}" width="100">
            </div>
            """,
            unsafe_allow_html=True
        )

st.title("🐛 Larvae Processing App")

# Upload a video
min_rep, max_rep, def_rep = os.environ.get("MIN_REP"), os.environ.get("MAX_REP"), os.environ.get("DEF_REP")
min_rep, max_rep, def_rep = int(min_rep), int(max_rep), int(def_rep)
temp_path, uploaded_file, length = video_upload()

# Initialize session state
if "processing_done" not in st.session_state:
    st.session_state.processing_done = False

if uploaded_file is not None:
    col_left, col_right = st.columns(2)  # Equal width columns

    # Left Side: Video Preview & Processing Controls
    with col_left:
        st.subheader("📹 Video Preview & Processing")

        # Show video preview only before processing
        if not st.session_state.processing_done:
            st.video(temp_path)

        # Processing Controls (only before processing)
        if not st.session_state.processing_done:
            with st.expander("⚙️ Processing Parameters"):
                # Slider for number of background frames
                N = st.slider("Number of Background Frames", length // 2, length, length, length // 20)
                repetitions = st.slider("Number of Repetitions", min_rep, max_rep, def_rep)

            # Button Centering Trick
            col1, col2, col3 = st.columns([1, 2, 1])  # Middle column is wider
            with col2:  
                if st.button("🚀 Process Video", use_container_width=True):
                    success = st.empty()
                    progress_bar = st.progress(0)
                    time_display = st.info("⏳ Processing Video...")

                    start_time = time.time()  # Start timer

                    for i in range(repetitions):
                        iter_start_time = time.time()  # Start time for this iteration

                        if repetitions > 1:
                            processed = remove_background(temp_path if i == 0 else processed, N, None)
                            progress_bar.progress((i + 1) / repetitions)
                        else:
                            processed = remove_background(temp_path, N, (progress_bar, time_display))

                        # Estimate remaining time
                        elapsed_time = time.time() - start_time
                        time_display.info(f"⏳ Processing Video... Elapsed Time: {elapsed_time:.2f}s")
                    
                    progress_bar.empty()  # Remove old progress bar
                    time_display.empty()
                    success.success("✅ Processing Complete!")

                    # Move processed file
                    if processed:
                        os.makedirs("temp", exist_ok=True)
                        shutil.move(processed, "temp/processed.mp4")
                    os.remove(temp_path)

                    # Update session state
                    st.session_state.processing_done = True

    # Right Side: Processed Video (only after processing)
    with col_right:
        if st.session_state.processing_done:
            st.subheader("🎥 Processed Video")
            st.video("temp/processed.mp4")