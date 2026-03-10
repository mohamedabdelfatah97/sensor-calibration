# calibrate.py
# -------------------------------------------------------
# Reads all images in images/, detects the checkerboard
# corners, runs OpenCV calibration, and saves results
# to calibration_output/
# -------------------------------------------------------

import cv2
import numpy as np
import glob
import os
import yaml

# =============================================
#  EDIT THIS — your measured square size in meters
#  Example: 25mm = 0.025 | 27mm = 0.027
SQUARE_SIZE_METERS = 0.0265
# =============================================

# Inner corners of the checkerboard
# (total squares per row minus 1, total squares per col minus 1)
# so inner corners = (6, 9)
CHECKERBOARD = (6, 9)

IMAGE_GLOB = "images/*.png"
OUTPUT_DIR = "calibration_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Termination criteria for corner refinement
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Build the 3D object point template (flat board so Z=0)
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0],
                        0:CHECKERBOARD[1]].T.reshape(-1, 2)
objp *= SQUARE_SIZE_METERS

objpoints = []   # list of 3D points for each valid image
imgpoints = []   # list of 2D points for each valid image
img_size  = None
valid     = []
failed    = []

all_images = sorted(glob.glob(IMAGE_GLOB))
print(f"\nFound {len(all_images)} images in images/\n")

for fname in all_images:
    img  = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_size = gray.shape[::-1]  # (width, height)

    # Try to find checkerboard corners
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret:
        # Refine corner locations to sub-pixel accuracy
        refined = cv2.cornerSubPix(
            gray, corners, (11, 11), (-1, -1), criteria
        )
        objpoints.append(objp)
        imgpoints.append(refined)
        valid.append(fname)
        print(f"  ✓  {os.path.basename(fname)}")
    else:
        failed.append(fname)
        print(f"  ✗  {os.path.basename(fname)}  — corners not detected, skipping")

print(f"\n{'─'*50}")
print(f"  Valid images   : {len(valid)}")
print(f"  Skipped images : {len(failed)}")
print(f"{'─'*50}")

if len(valid) < 10:
    print("\nERROR: Not enough valid images to calibrate.")
    print("Go back and capture more images with better coverage.")
    exit(1)

print("\nRunning calibration — this takes a few seconds...")

ret, K, D, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, img_size, None, None
)

# ── Compute mean reprojection error ──────────────────────
errors = []
for i in range(len(objpoints)):
    proj, _ = cv2.projectPoints(
        objpoints[i], rvecs[i], tvecs[i], K, D
    )
    err = cv2.norm(imgpoints[i], proj, cv2.NORM_L2) / len(proj)
    errors.append(err)

mean_err = float(np.mean(errors))
max_err  = float(np.max(errors))

# ── Print results ─────────────────────────────────────────
print(f"\n{'='*50}")
print(f"  CALIBRATION RESULTS")
print(f"{'='*50}")
print(f"\n  Camera Matrix (K):")
print(f"    fx = {K[0,0]:.4f}  px")
print(f"    fy = {K[1,1]:.4f}  px")
print(f"    cx = {K[0,2]:.4f}  px  (principal point X)")
print(f"    cy = {K[1,2]:.4f}  px  (principal point Y)")
print(f"\n  Distortion Coefficients (k1 k2 p1 p2 k3):")
print(f"    {D.flatten().tolist()}")
print(f"\n  Reprojection Error:")
print(f"    Mean : {mean_err:.4f} px")
print(f"    Max  : {max_err:.4f} px")

if mean_err < 0.3:
    grade = "EXCELLENT ✓ — ready to use"
elif mean_err < 0.5:
    grade = "GOOD ✓ — acceptable for most applications"
elif mean_err < 1.0:
    grade = "FAIR — consider recapturing with more varied angles"
else:
    grade = "POOR ✗ — recapture images, something went wrong"

print(f"    Grade: {grade}")
print(f"{'='*50}\n")

# ── Save results ──────────────────────────────────────────
np.save(f"{OUTPUT_DIR}/camera_matrix.npy", K)
np.save(f"{OUTPUT_DIR}/dist_coeffs.npy",   D)
print(f"  Saved: camera_matrix.npy")
print(f"  Saved: dist_coeffs.npy")

# ROS 2 compatible YAML
yaml_data = {
    "image_width":  img_size[0],
    "image_height": img_size[1],
    "camera_name":  "d455",
    "camera_matrix": {
        "rows": 3,
        "cols": 3,
        "data": K.flatten().tolist()
    },
    "distortion_model": "plumb_bob",
    "distortion_coefficients": {
        "rows": 1,
        "cols": 5,
        "data": D.flatten().tolist()
    }
}

yaml_path = f"{OUTPUT_DIR}/d455_calibration.yaml"
with open(yaml_path, "w") as f:
    yaml.dump(yaml_data, f, default_flow_style=False)

print(f"  Saved: d455_calibration.yaml  ← use this in ROS 2 / Nav2")
print(f"\nAll files saved to {OUTPUT_DIR}/\n")