# Intel RealSense D435i — RGB Camera Calibration

Intrinsic calibration of the Intel RealSense D435i RGB color stream
using OpenCV's checkerboard method on Windows 10/11.

## Hardware Used
- Intel RealSense D435i
- Printed 10x7 checkerboard, 26.5mm squares
- Mounted flat on rigid cardboard backing

---

## D435i vs D455 — Key Differences

| | D435i | D455 |
|---|---|---|
| Baseline | 50mm | 95mm |
| RGB Shutter | Rolling | Global |
| Depth Range | Up to 3m | Up to 4m |
| IMU | Yes | Yes |
| FOV | Narrower | Wider |

The rolling shutter on the D435i means the board must be held
completely still before each capture to avoid motion blur artifacts.

---

## Calibration Results

| Metric | Value |
|---|---|
| Mean Reprojection Error | 0.0457 px |
| Max Reprojection Error | 0.0921 px |
| Valid Images | 50 / 50 |
| Resolution | 1280 x 720 |
| Grade | EXCELLENT |

### Camera Matrix (K)
| Parameter | Value |
|---|---|
| fx | 906.12 px |
| fy | 907.23 px |
| cx | 645.79 px |
| cy | 353.69 px |

> The higher focal length (906 vs 634 on the D455) reflects the
> D435i's narrower field of view — expected behaviour.

Full output: [calibration_output/d435i_calibration.yaml](calibration_output/d435i_calibration.yaml)

---

## Setup

### 1. Install Intel RealSense SDK
Download the Windows installer from:
[https://github.com/realsenseai/librealsense/releases](https://github.com/realsenseai/librealsense/releases)

Download and run: `RealSense.SDK-WIN10-x.xx.x.exe`

### 2. Install Python dependencies
```bash