import cv2 as cv
import numpy as np
from scipy.interpolate import splprep, splev
from skimage.morphology import thin
import streamlit as st
def get_spline(segmented_img, smoothing_factor=100, segments_num=100):
    if segments_num < 1:
        raise ValueError("segments_num must be greater than 0")
    
    thinned_image = segmented_img.copy()
    thinned_image = thin(thinned_image)
    
    coords = np.column_stack(np.where(thinned_image == 1))

    if len(coords) < 4:  # ✅ Ensure we have at least 4 points for a cubic spline
        raise ValueError(f"Not enough points for spline fitting: found {len(coords)}, need at least 4")

    coords = coords[np.argsort(coords[:, 0])]

    x = coords[:, 0]
    y = coords[:, 1]

    tck, u = splprep([x, y], s=smoothing_factor)

    u_fine = np.linspace(0, 1, num=segments_num+1)
    y_smooth, x_smooth = splev(u_fine, tck)

    return np.stack([x_smooth, y_smooth], axis=1)

def threshold(image, lower, upper):
    return cv.inRange(image, lower, upper)

def extract_larva(vid, lower, upper, smoothing_factor=100, segments_num=100):
    
    # mask_preview = st.empty()
    splines = []
    progress_bar = st.empty()
    progress_text = st.empty()

    cap = cv.VideoCapture(vid)
    while True:
        if progress_bar is not None:
            progress_bar.progress(cap.get(cv.CAP_PROP_POS_FRAMES) / cap.get(cv.CAP_PROP_FRAME_COUNT))
            progress_text.info(f"Processing frame {cap.get(cv.CAP_PROP_POS_FRAMES)}")
        ret, image = cap.read()
        if not ret:
            break
        mask = threshold(cv.cvtColor(image, cv.COLOR_BGR2GRAY), lower, upper)
        # mask_preview.image(mask, use_container_width=True)
        thinned_image = thin(mask)
        splines.append(get_spline(thinned_image, smoothing_factor, segments_num))
    cap.release()
    return splines