import os
import cv2 as cv
import numpy as np
import tempfile
import subprocess
import time

def remove_background(vid: str, N: int, progress_elements) -> str:
    """Process video and remove background."""
    cap = cv.VideoCapture(vid)
    if progress_elements is not None:
        progress_bar, progress_text = progress_elements
    else:
        progress_bar, progress_text = None, None

    # Get video properties
    w, h = int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv.CAP_PROP_FPS)
    length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

    # Read first N frames for background estimation
    bg_frames = []
    for _ in range(N):
        ret, frame = cap.read()
        if not ret:
            break
        bg_frames.append(frame)

    # Check if bg_frames is empty
    if not bg_frames:
        cap.release()
        return None  # No valid background frames, return early
    # Save to a temporary file
    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    output_path = temp_output.name
    temp_output.close()  # Close temp file to allow writing

    # Compute median background
    try:
        median_background = np.median(bg_frames, axis=0).astype(np.uint8)
    except Exception as e:
        print("Error computing median background:", e)
        cap.release()
        return None
    
    cap.release()


    # Set up video writer
    fourcc = cv.VideoWriter_fourcc(*'MP4V')
    out = cv.VideoWriter(output_path, fourcc, fps, (w, h))
    cap = cv.VideoCapture(vid)
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

    # encode the video
    encoded_vid = output_path.replace(".mp4", "_encoded.mp4")
    ffmpeg_cmd = f"ffmpeg -i {output_path} -c:v libx264 -crf 23 -preset veryfast -c:a copy {encoded_vid} -y"
    subprocess.run(ffmpeg_cmd, shell=True)
    os.remove(output_path)  # Remove unencoded video


    return encoded_vid