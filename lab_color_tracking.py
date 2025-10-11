# lab_color_tracking.py
# Sophia Beninati
# References: OpenCV Tutorials (https://docs.opencv.org/)
# Improvements: Added HSV filtering, Gaussian blur, and K-Means dominant color detection.

import cv2
import numpy as np

# --- PARAMETERS ---
# HSV range for your object (adjust as needed)
lower_hsv = np.array([30, 100, 100])
upper_hsv = np.array([90, 255, 255])

# K-Means parameters
k = 1  # dominant color
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # --- Preprocessing ---
    blurred = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # --- Threshold for object tracking ---
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding box around largest contour
    if contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # --- Dominant color in central rectangle ---
    h_center, w_center = frame.shape[0]//2, frame.shape[1]//2
    rect_size = 100
    rect = frame[h_center-rect_size//2:h_center+rect_size//2,
                 w_center-rect_size//2:w_center+rect_size//2]

    Z = rect.reshape((-1,3))
    Z = np.float32(Z)
    _, labels, centers = cv2.kmeans(Z, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    dominant_color = np.uint8(centers[0])
    cv2.rectangle(frame, (w_center-rect_size//2, h_center-rect_size//2),
                  (w_center+rect_size//2, h_center+rect_size//2),
                  (int(dominant_color[0]), int(dominant_color[1]), int(dominant_color[2])), 2)

    # --- Display ---
    cv2.imshow("Tracking", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
