# use.py
import numpy as np
import cv2
import pyrealsense2 as rs

# Load your calibration results
K = np.load("calibration_output/camera_matrix.npy")
D = np.load("calibration_output/dist_coeffs.npy")

# Start the D455
pipeline = rs.pipeline()
config   = rs.config()
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
pipeline.start(config)

print("Showing undistorted feed — press Q to quit")

try:
    while True:
        frames      = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # Get raw frame
        raw_frame = np.frombuffer(color_frame.get_data(), dtype=np.uint8).copy()
        raw_frame = raw_frame.reshape((720, 1280, 3))

        # Apply calibration — remove lens distortion
        undistorted_frame = cv2.undistort(raw_frame, K, D)

        # Show both side by side so you can see the difference
        combined = np.hstack((raw_frame, undistorted_frame))
        cv2.putText(combined, "RAW",         (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 2)
        cv2.putText(combined, "UNDISTORTED", (1300, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 2)

        cv2.imshow("D455 — Raw vs Undistorted", combined)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()