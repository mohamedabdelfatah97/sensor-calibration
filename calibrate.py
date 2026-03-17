import cv2
import numpy as np
import glob
import os
import yaml

# ── CHANGE THIS after measuring your printed squares ──
SQUARE_SIZE_METERS = 0.0265
# ─────────────────────────────────────────────────────

CHECKERBOARD = (6, 9)
IMAGE_GLOB   = "images/*.png"
OUTPUT_DIR   = "calibration_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0],
                        0:CHECKERBOARD[1]].T.reshape(-1, 2)
objp *= SQUARE_SIZE_METERS

objpoints = []
imgpoints = []
img_size  = None
valid     = []
failed    = []

all_images = sorted(glob.glob(IMAGE_GLOB))
print(f"\nFound {len(all_images)} images\n")

for fname in all_images:
    img  = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_size = gray.shape[::-1]

    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret:
        refined = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        objpoints.append(objp)
        imgpoints.append(refined)
        valid.append(fname)
        print(f"  OK  {os.path.basename(fname)}")
    else:
        failed.append(fname)
        print(f"  --  {os.path.basename(fname)}  skipped")

print(f"\n  Valid   : {len(valid)}")
print(f"  Skipped : {len(failed)}")

if len(valid) < 10:
    print("\nERROR: Not enough valid images. Capture more and try again.")
    exit(1)

print("\nRunning calibration...")

ret, K, D, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, img_size, None, None
)

errors = []
for i in range(len(objpoints)):
    proj, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], K, D)
    err = cv2.norm(imgpoints[i], proj, cv2.NORM_L2) / len(proj)
    errors.append(err)

mean_err = float(np.mean(errors))
max_err  = float(np.max(errors))

print(f"\n{'='*50}")
print(f"  CALIBRATION RESULTS")
print(f"{'='*50}")
print(f"  fx = {K[0,0]:.4f} px")
print(f"  fy = {K[1,1]:.4f} px")
print(f"  cx = {K[0,2]:.4f} px")
print(f"  cy = {K[1,2]:.4f} px")
print(f"  Distortion: {D.flatten().tolist()}")
print(f"  Mean Error : {mean_err:.4f} px")
print(f"  Max Error  : {max_err:.4f} px")

if mean_err < 0.3:
    print("  Grade: EXCELLENT")
elif mean_err < 0.5:
    print("  Grade: GOOD")
elif mean_err < 1.0:
    print("  Grade: FAIR - try more varied images")
else:
    print("  Grade: POOR - recapture from scratch")
print(f"{'='*50}\n")

np.save(f"{OUTPUT_DIR}/camera_matrix.npy", K)
np.save(f"{OUTPUT_DIR}/dist_coeffs.npy",   D)

yaml_data = {
    "image_width":  img_size[0],
    "image_height": img_size[1],
    "camera_name":  "d435i",
    "camera_matrix": {
        "rows": 3, "cols": 3,
        "data": K.flatten().tolist()
    },
    "distortion_model": "plumb_bob",
    "distortion_coefficients": {
        "rows": 1, "cols": 5,
        "data": D.flatten().tolist()
    }
}

with open(f"{OUTPUT_DIR}/d435i_calibration.yaml", "w") as f:
    yaml.dump(yaml_data, f, default_flow_style=False)

print("Saved to calibration_output:")
print("  camera_matrix.npy")
print("  dist_coeffs.npy")
print("  d435i_calibration.yaml")