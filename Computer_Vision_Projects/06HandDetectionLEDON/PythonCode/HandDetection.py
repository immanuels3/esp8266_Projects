import cv2
import mediapipe as mp
import requests

ESP_IP = "http://192.168.43.232"  # Change to your ESP IP

hand_detected = False
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    has_hand = results.multi_hand_landmarks is not None

    if has_hand:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.putText(frame, "Hand Detected", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "No Hand", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Send to ESP8266 only when state changes
    if has_hand and not hand_detected:
        requests.get(ESP_IP + "/hand?state=1")
        hand_detected = True
    elif not has_hand and hand_detected:
        requests.get(ESP_IP + "/hand?state=0")
        hand_detected = False

    cv2.imshow("Hand Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
