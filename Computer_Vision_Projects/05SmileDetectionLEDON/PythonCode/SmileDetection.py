import cv2
from fer import FER
import requests

ESP_IP = "http://192.168.43.232"  # Replace with your ESP8266 IP

detector = FER(mtcnn=True)  # Fast and lightweight
cap = cv2.VideoCapture(0)

last_smile = False
stable_count = 0
unstable_count = 0
STABLE_FRAMES = 2
UNSTABLE_FRAMES = 2
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    frame_count += 1

    if frame_count % 3 == 0:  # Every 3 frames (reduce CPU usage)
        try:
            emotion_data = detector.top_emotion(frame)
            if emotion_data:
                emotion, score = emotion_data

                if emotion == "happy":
                    stable_count += 1
                    unstable_count = 0
                else:
                    unstable_count += 1
                    stable_count = 0

                if stable_count >= STABLE_FRAMES and not last_smile:
                    requests.get(f"{ESP_IP}/smile?state=1")
                    last_smile = True
                    stable_count = 0

                elif unstable_count >= UNSTABLE_FRAMES and last_smile:
                    requests.get(f"{ESP_IP}/smile?state=0")
                    last_smile = False
                    unstable_count = 0

                # UI
                label = f"😊 Smiling" if last_smile else f"😐 Not Smiling"
                color = (0, 255, 0) if last_smile else (0, 0, 255)
                cv2.putText(frame, label, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        except Exception as e:
            cv2.putText(frame, "Face not detected", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Fast Smile Detection (FER)", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
