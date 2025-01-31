import os
import cv2 as cv
import numpy as np
import tempfile
import subprocess
import time

def calc_median_background(vid: str, N: int) -> np.ndarray:
    """Calculate median background from first N frames of video."""
    cap = cv.VideoCapture(vid)
    bg_frames = []
    for _ in range(N):
        ret, frame = cap.read()
        if not ret:
            break
        bg_frames.append(frame)
    cap.release()
    try:
        median_bg = np.median(bg_frames, axis=0).astype(np.uint8)
    except Exception as e:
        raise ValueError(f"Error computing median background: {e}")
    return median_bg

def write_bgless(vid: str, median_background: np.ndarray, progress_elements=None) -> None:
    """Write video without background to output_path."""
    cap = cv.VideoCapture(vid)
    w, h = int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv.CAP_PROP_FPS)
    length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    output_path = temp_output.name
    temp_output.close()  # Close temp file to allow writing

    # Set up video writer
    fourcc = cv.VideoWriter_fourcc(*'MP4V')
    out = cv.VideoWriter(output_path, fourcc, fps, (w, h))

    if progress_elements is not None:
        progress_bar, progress_text = progress_elements
    else:
        progress_bar, progress_text = None, None

    start_time = time.time()
    for _ in range(length):
        ret, frame = cap.read()
        if not ret:
            break

        # Subtract the background
        diff = cv.absdiff(frame, median_background)

        # Convert to HSV and extract value channel
        hsv = cv.cvtColor(diff, cv.COLOR_BGR2HSV)
        value_channel = hsv[:, :, 2]

        # Convert back to BGR (needed for VideoWriter)
        out.write(cv.cvtColor(value_channel, cv.COLOR_GRAY2BGR))
        if progress_bar:
            progress_bar.progress(int(cap.get(cv.CAP_PROP_POS_FRAMES) / length * 100))
            progress_text.text(f"⏱️ Time Elapsed: {time.time() - start_time:.2f}s")

    cap.release()
    out.release()

    return output_path

def remove_background(vid: str, N: int, progress_elements) -> str:
    """Process video and remove background."""

    median_background = calc_median_background(vid, N)
    output_path = write_bgless(vid, median_background, progress_elements)
    
    # encode the video
    encoded_vid = output_path.replace(".mp4", "_encoded.mp4")
    ffmpeg_cmd = f"ffmpeg -i {output_path} -c:v libx264 -crf 23 -preset veryfast -c:a copy {encoded_vid} -y"
    subprocess.run(ffmpeg_cmd, shell=True)
    os.remove(output_path)  # Remove unencoded video

    return encoded_vid