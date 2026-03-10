# capture.py
# -------------------------------------------------------
# This script opens a live feed from your D455 and lets
# you press SPACE to save frames to the images/ folder.
# Press Q when you have 35-50 images saved.
# -------------------------------------------------------

import pyrealsense2 as rs
import numpy as np
import cv2
import os

SAVE_DIR = "images"
os.makedirs(SAVE_DIR, exist_ok=True)

# Start the D455 pipeline
pipeline = rs.pipeline()
config   = rs.config()

# Enable the RGB color stream at 1280x720 resolution, 30fps
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
pipeline.start(config)

count = 0
print("========================================")
print("  D455 Calibration Image Capture Tool")
print("========================================")
print("  SPACE bar = save current frame")
print("  Q         = quit when done")
print(f" Target: save 35 to 50 images")
print("========================================\n")

try:
    while True:
        # Grab the latest frame from the camera
        frames      = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue

        # Convert to numpy array
        img = np.frombuffer(color_frame.get_data(), dtype=np.uint8).copy()
        img = img.reshape((720, 1280, 3))

        # Make a display copy with instructions overlaid
        display = img.copy()

        # Green counter in top left
        cv2.putText(display,
                    f"Saved: {count} / 40 images",
                    (20, 45),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.3,
                    (0, 255, 0),
                    2)

        # Instruction reminder
        cv2.putText(display,
                    "SPACE = capture    Q = quit",
                    (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.85,
                    (0, 200, 255),
                    2)

        # Warning if below target
        if count < 35:
            cv2.putText(display,
                        f"Need {35 - count} more",
                        (20, 135),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.85,
                        (0, 100, 255),
                        2)
        else:
            cv2.putText(display,
                        "Good! Press Q when ready",
                        (20, 135),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.85,
                        (0, 255, 100),
                        2)

        cv2.imshow("D455 Capture — Move the board around!", display)

        key = cv2.waitKey(1)

        if key == ord(' '):
            # Save the raw frame (not the display copy with text)
            path = os.path.join(SAVE_DIR, f"frame_{count:03d}.png")
            cv2.imwrite(path, img)
            print(f"  [{count:02d}] Saved → {path}")
            count += 1

        elif key == ord('q') or key == 27:  # Q or ESC
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()
    print(f"\n Capture complete — {count} images saved to images/")
    if count < 20:
        print(" WARNING: You have fewer than 20 images — calibration may be poor")
    elif count < 35:
        print(" You have enough but more variety would help")
    else:
        print(" Great number of images — proceed to calibrate.py")