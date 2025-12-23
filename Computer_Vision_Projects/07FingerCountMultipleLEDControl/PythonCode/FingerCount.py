import cv2
import mediapipe as mp
import requests

ESP_IP = "http://192.168.43.232"  # Replace with your ESP8266 IP

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
prev_count = -1

# Define finger tip and pip joint landmarks
fingertips_ids = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
thumb_tip = 4

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    h, w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    count = 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark

            # Count fingers (except thumb)
            for tip_id in fingertips_ids:
                if landmarks[tip_id].y < landmarks[tip_id - 2].y:
                    count += 1

            # Optional: count thumb
            if landmarks[thumb_tip].x > landmarks[thumb_tip - 1].x:
                count += 1  # uncomment to include thumb

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Show count on screen
    cv2.putText(frame, f'Fingers: {count}', (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 2)

    # Send to ESP only if count changed
    if count != prev_count:
        requests.get(f"{ESP_IP}/fingers?count={count}")
        prev_count = count

    cv2.imshow("Finger Counter", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
