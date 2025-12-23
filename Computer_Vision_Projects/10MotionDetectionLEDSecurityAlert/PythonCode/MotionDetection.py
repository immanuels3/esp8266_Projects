import cv2
import requests

ESP_IP = "http://192.168.43.232"  # Change to your ESP IP

cap = cv2.VideoCapture(0)
_, frame1 = cap.read()
_, frame2 = cap.read()
motion_detected = False

while True:
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 25, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    detected = False

    for contour in contours:
        if cv2.contourArea(contour) < 1000:
            continue
        detected = True
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x,y), (x+w, y+h), (0,255,0), 2)

    # Show text and send to ESP only if state changed
    if detected and not motion_detected:
        requests.get(f"{ESP_IP}/motion?state=1")
        motion_detected = True
        cv2.putText(frame1, "Motion Detected!", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    elif not detected and motion_detected:
        requests.get(f"{ESP_IP}/motion?state=0")
        motion_detected = False

    cv2.imshow("Motion Detection", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if not ret:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
