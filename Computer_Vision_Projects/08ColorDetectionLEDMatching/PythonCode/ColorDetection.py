import cv2
import numpy as np
import requests

ESP_IP = "http://192.168.43.232"  # Replace with your ESP IP
prev_color = ""

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    h, w, _ = frame.shape
    center_x, center_y = w // 2, h // 2
    roi = frame[center_y-10:center_y+10, center_x-10:center_x+10]

    avg_color = np.mean(roi, axis=(0, 1))  # BGR
    b, g, r = avg_color
    detected_color = ""

    if r > g and r > b and r > 80:
        detected_color = "red"
    elif g > r and g > b and g > 80:
        detected_color = "green"
    elif b > r and b > g and b > 80:
        detected_color = "blue"
    else:
        detected_color = "none"

    # Send to ESP only if color changed
    if detected_color != prev_color:
        requests.get(f"{ESP_IP}/color?val={detected_color}")
        prev_color = detected_color

    # Draw indicator
    cv2.rectangle(frame, (center_x-10, center_y-10), (center_x+10, center_y+10), (255, 255, 255), 2)
    cv2.putText(frame, f'Color: {detected_color}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("Color Detection", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
