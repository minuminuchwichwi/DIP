import cv2
import numpy as np

capture = cv2.VideoCapture(0)
if capture.isOpened() == False: raise Exception("카메라가 연결되지 않음")

capture.set(cv2.CAP_PROP_FRAME_WIDTH, 400)      #영상의 크기를 600*600으로 설정
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
capture.set(cv2.CAP_PROP_AUTOFOCUS, 0)
capture.set(cv2.CAP_PROP_BRIGHTNESS, 100)

title = "main window"
cv2.namedWindow(title)

while True:
    ret, frame = capture.read()
    if not ret: break
    if cv2.waitKey(10) == 27: break

    cv2.rectangle(frame, (30, 30), (320, 240), (0, 0, 255), 3, cv2.LINE_4)

    mask = np.zeros_like(frame)     #프레임과 같은 크기의 마스크를 만들어 0으로 초기화
    mask[30:240, 30:320] = 1        #프레임의 관심영역에 따라 마스크 값을 1로 바꿈

    cv2.imshow(title, cv2.multiply(frame, mask))

capture.release()