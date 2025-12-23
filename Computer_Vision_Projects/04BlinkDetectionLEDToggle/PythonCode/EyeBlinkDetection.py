import cv2
import mediapipe as mp
import math
import requests

ESP_IP = "http://192.168.43.232"  # Change to your ESP IP

led_state = False
blink_counter = 0
blink_triggered = False

# Mediapipe face mesh setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

cap = cv2.VideoCapture(0)

# Eye landmark indices (LEFT eye)
LEFT_EYE_TOP = 159
LEFT_EYE_BOTTOM = 145

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape
            top = face_landmarks.landmark[LEFT_EYE_TOP]
            bottom = face_landmarks.landmark[LEFT_EYE_BOTTOM]

            top_y = int(top.y * h)
            bottom_y = int(bottom.y * h)

            eye_distance = abs(top_y - bottom_y)

            cv2.putText(frame, f"Eye distance: {eye_distance:.2f}", (20, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

            # If eye closed (blink)
            if eye_distance < 5:  # You may adjust this threshold
                blink_counter += 1
            else:
                if blink_counter >= 2 and not blink_triggered:
                    led_state = not led_state
                    blink_triggered = True
                    if led_state:
                        requests.get(ESP_IP + "/led?state=1")
                    else:
                        requests.get(ESP_IP + "/led?state=0")
                blink_counter = 0
                blink_triggered = False

    cv2.imshow("Blink Detection", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
