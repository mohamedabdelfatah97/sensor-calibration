import pyrealsense2 as rs
import numpy as np
import cv2
import os

SAVE_DIR = "images"
os.makedirs(SAVE_DIR, exist_ok=True)

pipeline = rs.pipeline()
config   = rs.config()
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
pipeline.start(config)

count = 0
print("========================================")
print("  D435i Calibration Image Capture Tool")
print("========================================")
print("  SPACE = save frame")
print("  Q     = quit when done")
print("  Target: 40-50 images")
print("  NOTE: D435i has rolling shutter")
print("  Move the board SLOWLY to avoid blur")
print("========================================")

try:
    while True:
        frames      = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        img = np.frombuffer(color_frame.get_data(), dtype=np.uint8).copy()
        img = img.reshape((720, 1280, 3))

        display = img.copy()
        cv2.putText(display, f"Saved: {count} / 40",
                    (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0,255,0), 2)
        cv2.putText(display, "SPACE=capture  Q=quit",
                    (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0,200,255), 2)
        cv2.putText(display, "Move SLOWLY — rolling shutter",
                    (20, 135), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0,100,255), 2)

        if count >= 40:
            cv2.putText(display, "Done! Press Q to finish",
                        (20, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0,255,100), 2)

        cv2.imshow("D435i Capture", display)
        key = cv2.waitKey(1)

        if key == ord(' '):
            path = os.path.join(SAVE_DIR, f"frame_{count:03d}.png")
            cv2.imwrite(path, img)
            print(f"  [{count:02d}] Saved -> {path}")
            count += 1
        elif key == ord('q') or key == 27:
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()
    print(f"\nDone. {count} images saved to images\\")