# Intel RealSense D455 — RGB Camera Calibration

Intrinsic calibration of the Intel RealSense D455 RGB color stream
using OpenCV's checkerboard method on Windows 10/11.

## Hardware Used
- Intel RealSense D455
- Printed 10x7 checkerboard, 26.5mm squares
- Mounted flat on rigid cardboard backing

## Calibration Results

| Metric | Value |
|---|---|
| Mean Reprojection Error | 0.0226 px |
| Max Reprojection Error | 0.0488 px |
| Valid Images | 50 / 50 |
| Resolution | 1280 x 720 |
| Grade | EXCELLENT |

### Camera Matrix (K)
| Parameter | Value |
|---|---|
| fx | 634.61 px |
| fy | 634.86 px |
| cx | 636.02 px |
| cy | 375.95 px |

Full output: [calibration_output/d455_calibration.yaml](calibration_output/d455_calibration.yaml)

## Setup

### 1. Install Intel RealSense SDK
Download the Windows installer from:
https://github.com/realsenseai/librealsense/releases
→ RealSense.SDK-WIN10-x.xx.x.exe

### 2. Install Python dependencies
pip install -r requirements.txt

## Workflow

### Step 1 — Generate checkerboard
python generate_board.py
# Prints checkerboard_PRINT_ME.png
# Print at 100% scale, no fit-to-page
# Mount flat on rigid surface

### Step 2 — Capture images
python capture.py
# SPACE = save frame
# Q     = quit
# Target: 40-50 images with varied angles and distances

### Step 3 — Update square size
# Open calibrate.py and set SQUARE_SIZE_METERS to your
# measured square size e.g. 0.0265 for 26.5mm

### Step 4 — Run calibration
python calibrate.py
# Outputs camera_matrix.npy, dist_coeffs.npy, d455_calibration.yaml

### Step 5 — Verify
python use.py
# Shows raw vs undistorted feed side by side

## Using the Calibration in ROS 2 / Nav2
camera_info_url: "f/Users/marcelo/dev/calibration/Intel_RealSense_D455/calibration_output/d455_calibration.yaml"
```

Open `Intel_RealSense_D455/requirements.txt` and paste:
```
opencv-python>=4.5.0
numpy>=1.21.0
pyrealsense2>=2.50.0
pyyaml>=5.4.0