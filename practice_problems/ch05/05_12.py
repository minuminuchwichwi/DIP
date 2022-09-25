#관심 영역(roi) 화소대비??가 뭔지 모르겠음
import numpy as np, cv2

capture = cv2.VideoCapture("C:/images/ch05/flip_test.avi")
if not capture.isOpened(): raise Exception("동영상 파일 개방 안됨")

frame_rate = capture.get(cv2.CAP_PROP_FPS)
delay = int(1000 / frame_rate)

while True:
    ret, frame = capture.read()
    if not ret or cv2.waitKey(delay) >= 0: break

    cv2.rectangle(frame, (50, 50), (240, 240), (0, 0, 255), 3, cv2.LINE_4)
    cv2.rectangle(frame, (400, 400), (320, 320), (255, 0, 0), 3, cv2.LINE_4)

    mask1 = np.zeros_like(frame)
    mask1[50:240, 50:240] = 50

    frame = cv2.add(frame, mask1)

    cv2.imshow("Read Video File", frame)

capture.release()