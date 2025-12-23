import cv2
import mediapipe as mp
import requests

ESP_IP = "http://192.168.43.232"  # Replace with your ESP IP

# Initialize mediapipe
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)
prev_status = -1
stable_count = 0
threshold = 5  # Frames to wait before confirming detection

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_detection.process(frame_rgb)

    detected = result.detections is not None

    # Show results
    if detected:
        for det in result.detections:
            bboxC = det.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                         int(bboxC.width * iw), int(bboxC.height * ih)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Real Face Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "No Face", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Debounce and avoid flicker
    if detected:
        stable_count += 1
    else:
        stable_count -= 1

    stable_count = max(0, min(threshold, stable_count))  # clamp between 0 and threshold

    # Send request only when stable state changes
    if stable_count == threshold and prev_status != 1:
        requests.get(ESP_IP + "/face?status=1")
        prev_status = 1
    elif stable_count == 0 and prev_status != 0:
        requests.get(ESP_IP + "/face?status=0")
        prev_status = 0

    cv2.imshow("Accurate Face Detection", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
