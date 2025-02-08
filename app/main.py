import pandas as pd
import streamlit as st
from bg_removal import remove_background
from utils import video_upload
import os
import shutil
import time
from dotenv import load_dotenv
from extract import extract_larva

def init_session():
    load_dotenv()
    
    if "processing_done" not in st.session_state:
        st.session_state.processing_done = False

    # Logos
    st.session_state.lab_logo = os.getenv("LAB_LOGO", "")
    st.session_state.uni_logo = os.getenv("UNI_LOGO", "")
    st.session_state.ins_logo = os.getenv("INS_LOGO", "")

    # Processing settings
    st.session_state.min_rep = int(os.getenv("MIN_REP", 1))
    st.session_state.max_rep = int(os.getenv("MAX_REP", 10))
    st.session_state.def_rep = int(os.getenv("DEF_REP", 5))

    # Postprocessing settings persistence
    if "threshold_range" not in st.session_state:
        st.session_state.threshold_range = (30, 180)
    if "segment_num" not in st.session_state:
        st.session_state.segment_num = 5

def show_logos():
    st.set_page_config(
        page_title="LarvaTrackAI",
        page_icon="🐛",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    col_left, _ = st.columns([1, 3])
    with col_left:
        with st.container():
            cols = st.columns(3)
            for i, logo in enumerate([st.session_state.uni_logo, st.session_state.lab_logo, st.session_state.ins_logo]):
                if logo:
                    cols[i].image(logo, width=100)

def initialize_app():
    """Initialize session state and display logos."""
    init_session()
    show_logos()
    st.title("🐛 Larvae Processing App")
    st.markdown("Efficiently preprocess and analyze larva videos with AI-powered background removal.")

def handle_video_upload():
    """Handle video upload with metadata extraction."""
    st.subheader("📂 Upload Your Video")
    temp_path, uploaded_file, length = video_upload()

    if uploaded_file:
        st.success(f"✅ Uploaded `{uploaded_file.name}` - {length} frames")
    
    return temp_path, uploaded_file, length

def display_video_preview(temp_path):
    """Display uploaded video before processing."""
    if temp_path and not st.session_state.processing_done:
        st.video(temp_path)

def configure_processing_controls(length):
    """Create dynamic sliders and processing parameters."""
    with st.expander("⚙️ Background Removal Settings"):
        st.info("Adjust settings for background removal.")
        N = st.slider("📸 Number of Background Frames", 1, length, length)
        method = st.selectbox("🔬 Method", ["Median", "Mean"])
        repetitions = st.slider("🔄 Repetitions", st.session_state.min_rep, st.session_state.max_rep, st.session_state.def_rep)
        # threshold_range = st.slider("Threshold Range", 0, 255, (30, 180), 5)
    return N, repetitions, method, (None, None)

def process_video(temp_path, N, repetitions, method):
    """Run the background removal processing pipeline."""
    success_msg = st.empty()
    progress_bar = st.progress(0)
    time_display = st.info("⏳ Processing...")

    start_time = time.time()

    for i in range(repetitions):
        processed = remove_background(temp_path if i == 0 else processed, N, method, None)
        progress_bar.progress((i + 1) / repetitions)
        elapsed_time = time.time() - start_time
        time_display.info(f"⏳ Elapsed Time: {elapsed_time:.2f}s")

    progress_bar.empty()
    time_display.empty()
    success_msg.success("✅ Processing Complete!")

    if processed:
        os.makedirs("temp", exist_ok=True)
        shutil.move(processed, "temp/processed.mp4")
    os.remove(temp_path)

    # ✅ Ensure session state is updated **once**
    st.session_state.processing_done = True
    st.rerun()  # ✅ Forces UI update while keeping processing state

def display_processed_video():
    """Show the processed video."""
    with st.expander("🎥 Processed Video"):
        st.video("temp/processed.mp4")

def thresholding_controls():
    """Add real-time thresholding controls with session state persistence."""
    st.subheader("🐛 Larva Extraction Parameters")

    with st.expander("📏 Threshold Adjustment"):
        # st.session_state.threshold_range = st.slider(
        #     "Threshold Range", 0, 255, st.session_state.threshold_range, 5
        # )
        st.session_state.segment_num = st.slider(
            "Number of Segments", 1, 10, st.session_state.segment_num
        )
        st.text(f"Threshold: {st.session_state.threshold_range}, Segments: {st.session_state.segment_num}")

    if st.button("🔍 Extract Larvae", use_container_width=True):
        st.session_state.larvae = extract_larva("temp/processed.mp4", st.session_state.threshold_range[0], st.session_state.threshold_range[1], st.session_state.segment_num)

    if "larvae" in st.session_state:
        st.dataframe(pd.DataFrame(st.session_state.larvae, columns=["X", "Y"]))


def main():
    """Structure the Streamlit app."""
    initialize_app()
    # temp_path, uploaded_file, length = handle_video_upload()

    temp_path, uploaded_file, length = None, None, None
    handle_video_upload()


    if uploaded_file:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📹 Video Preview")
            display_video_preview(temp_path)

            if not st.session_state.processing_done:
                N, repetitions, method, (lower, upper) = configure_processing_controls(length)
                if st.button("🚀 Start Processing", use_container_width=True):
                    process_video(temp_path, N, repetitions, method)

        with col2:
            st.subheader("🛠️ Postprocessing")
            
            # ✅ Always show postprocessing controls if a video was processed
            if st.session_state.processing_done or os.path.exists("temp/processed.mp4"):
                display_processed_video()
                thresholding_controls()

if __name__ == "__main__":
    main()