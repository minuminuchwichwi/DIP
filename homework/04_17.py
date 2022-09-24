import cv2

capture = cv2.VideoCapture(0)
if capture.isOpened() == False: raise Exception("카메라가 연결되지 않음")

title = "flip_test"
cv2.namedWindow(title)

fps, size, fourcc = 15, (640, 480), cv2.VideoWriter_fourcc(*'DIVX')
delay = round(1000/fps)

writer = cv2.VideoWriter("C:/images/flip_test.avi", fourcc, fps, size)
if writer.isOpened() == False: raise Exception("동영상 파일 개방 안됨")

capture.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])
capture.set(cv2.CAP_PROP_AUTOFOCUS, 0)
capture.set(cv2.CAP_PROP_BRIGHTNESS, 100)

while True:
    ret, frame = capture.read()
    if not ret: break
    if cv2.waitKey(delay) >= 0: break

    frame = cv2.flip(frame, 1)
    writer.write(frame)
    cv2.imshow(title, frame)

writer.release()
capture.release()
