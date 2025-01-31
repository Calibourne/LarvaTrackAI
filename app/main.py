import streamlit as st
from bg_removal import remove_background
from utils import video_upload
import os
import shutil
import time
from dotenv import load_dotenv

def init_session():
    load_dotenv()
    st.session_state.processing_done = False
    
    st.session_state.lab_logo = os.environ.get("LAB_LOGO")
    st.session_state.uni_logo = os.environ.get("UNI_LOGO")
    st.session_state.ins_logo = os.environ.get("INS_LOGO")
    
    st.session_state.min_rep = int(os.environ.get("MIN_REP"))
    st.session_state.max_rep = int(os.environ.get("MAX_REP"))
    st.session_state.def_rep = int(os.environ.get("DEF_REP"))


def show_logos():
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
                    <img src="{st.session_state.uni_logo}" width="100">
                    <img src="{st.session_state.lab_logo}" width="100">
                    <img src="{st.session_state.ins_logo}" width="100">
                </div>
                """,
                unsafe_allow_html=True
            )


if __name__ == "__main__":
    
    init_session()
    show_logos()
    
    st.title("🐛 Larvae Processing App")
    temp_path, uploaded_file, length = video_upload()

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
                with st.expander("⚙️ Background Removal Settings"):
                    # Slider for number of background frames
                    N = st.slider("Number of Background Frames", length // 2, length, length, length // 20)
                    min_rep, max_rep, def_rep = st.session_state.min_rep, st.session_state.max_rep, st.session_state.def_rep
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