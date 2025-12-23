import cv2
import requests

ESP_IP = "http://192.168.43.232"  # Change to your ESP IP
led_on = False

cap = cv2.VideoCapture(0)
qr_detector = cv2.QRCodeDetector()

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    data, bbox, _ = qr_detector.detectAndDecode(frame)

    if bbox is not None and data:
        cv2.polylines(frame, [bbox.astype(int)], True, (0, 255, 0), 2)
        cv2.putText(frame, f"QR: {data}", (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        if not led_on:
            requests.get(f"{ESP_IP}/qr?state=1")
            led_on = True
    else:
        cv2.putText(frame, "No QR detected", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if led_on:
            requests.get(f"{ESP_IP}/qr?state=0")
            led_on = False

    cv2.imshow("QR Code Scanner", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
