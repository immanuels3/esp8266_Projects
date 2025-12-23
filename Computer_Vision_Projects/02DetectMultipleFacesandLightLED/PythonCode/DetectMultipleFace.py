import cv2
import mediapipe as mp
import requests

ESP_IP = "http://192.168.43.232"  # Replace with your ESP IP

mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

prev_status = -1
stable_count = 0
threshold = 3  # Frames required to confirm status

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_detection.process(frame_rgb)

    count = 0
    if result.detections:
        count = len(result.detections)
        for det in result.detections:
            bboxC = det.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            x = int(bboxC.xmin * iw)
            y = int(bboxC.ymin * ih)
            w = int(bboxC.width * iw)
            h = int(bboxC.height * ih)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)

    cv2.putText(frame, f"Face Count: {count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Debounce logic
    if count != prev_status:
        stable_count += 1
    else:
        stable_count = 0

    if stable_count >= threshold:
        if count == 0:
            requests.get(ESP_IP + "/face?status=0")  # Red
        elif count == 1:
            requests.get(ESP_IP + "/face?status=1")  # Green
        else:
            requests.get(ESP_IP + "/face?status=2")  # Blue
        prev_status = count
        stable_count = 0

    cv2.imshow("Mediapipe Face Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
