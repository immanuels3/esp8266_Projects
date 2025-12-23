import cv2
from deepface import DeepFace
import requests

ESP_IP = "http://192.168.43.232"  # Your ESP8266 IP

cap = cv2.VideoCapture(0)
last_emotion = ""
stable_count = 0
stable_threshold = 5

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    try:
        # DeepFace returns dictionary with 'dominant_emotion'
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)[0]
        emotion = result['dominant_emotion']

        cv2.putText(frame, f'Emotion: {emotion}',
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # Stable emotion check
        if emotion == last_emotion:
            stable_count += 1
        else:
            stable_count = 0

        if stable_count >= stable_threshold:
            if emotion == "happy":
                requests.get(f"{ESP_IP}/emotion?status=happy")
            elif emotion == "angry":
                requests.get(f"{ESP_IP}/emotion?status=angry")
            else:
                requests.get(f"{ESP_IP}/emotion?status=neutral")
            stable_count = 0

        last_emotion = emotion

    except Exception as e:
        cv2.putText(frame, "No face/emotion detected", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Emotion Detection (DeepFace)", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
