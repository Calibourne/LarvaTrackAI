import os
import time
import cv2 as cv
import subprocess
import numpy as np

def calc_agg_background(vid: str, N: int, method: str) -> np.ndarray:
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
        if method.lower() == "mean":
            agg_bg = np.mean(bg_frames, axis=0).astype(np.uint8)
        elif method.lower() == "median":
            agg_bg = np.median(bg_frames, axis=0).astype(np.uint8)
        else:
            raise ValueError(f"Invalid method: {method}")
    except Exception as e:
        print(f"Error: {e}")
        return None
    return agg_bg

def write_bgless(
        vid: str, median_background: np.ndarray, 
        progress_elements=None, output_path: str = 'temp/processed_1.mp4') -> None:
    """Write video without background to output_path."""
    cap = cv.VideoCapture(vid)
    w, h = int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv.CAP_PROP_FPS)
    length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

    

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

def threshold(vid, lower, upper, output_path: str = 'temp/processed_2.mp4') -> str:
    cap = cv.VideoCapture(vid)
    fps = cap.get(cv.CAP_PROP_FPS)
    w, h = int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    out = cv.VideoWriter(output_path, cv.VideoWriter_fourcc(*'MP4V'), fps, (w, h))
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        mask = cv.threshold(cv.cvtColor(frame, cv.COLOR_BGR2GRAY), lower, upper, cv.THRESH_OTSU)[1]
        n_frame = np.zeros_like(frame)
        # find contours
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        max_contour = max(contours, key=cv.contourArea)
        cv.drawContours(n_frame, [max_contour], -1, (255, 255, 255), -1)

        out.write(n_frame)
    
    cap.release()
    out.release()

    return output_path

def remove_background(vid: str, N: int, method: str, progress_elements) -> str:
    """Process video and remove background."""

    agg_background = calc_agg_background(vid, N, method)
    output_path_1 = write_bgless(vid, agg_background, progress_elements)
    output_path_2 = threshold(output_path_1, 50, 255)
    os.remove(output_path_1)
    
    # encode the video
    encoded_vid = output_path_2.replace(".mp4", "_encoded.mp4")
    ffmpeg_cmd = f"ffmpeg -i {output_path_2} -c:v libx264 -crf 23 -preset veryfast -c:a copy {encoded_vid} -y"
    subprocess.run(ffmpeg_cmd, shell=True)
    os.remove(output_path_2)  # Remove unencoded video

    return encoded_vid