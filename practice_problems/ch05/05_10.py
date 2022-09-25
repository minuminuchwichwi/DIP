#3번은 포기, 잘된건지도 모르겠음...
import numpy as np, cv2

capture = cv2.VideoCapture(0)
if capture.isOpened() == False: raise Exception("카메라가 연결되지 않음")

capture.set(cv2.CAP_PROP_FRAME_WIDTH, 600)      #영상의 크기를 600*600으로 설정
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
capture.set(cv2.CAP_PROP_AUTOFOCUS, 0)
capture.set(cv2.CAP_PROP_BRIGHTNESS, 100)

title = "Show a particular region"
cv2.namedWindow(title)

while True:
    ret, frame = capture.read()
    if not ret: break
    if cv2.waitKey(10) == 27: break

    blue, green, red = cv2.split(frame)

    #100*200을 표현하기 위해 아래처럼 구현, [100:300, 200:300]인 이유는 [높이, 너비]이기 때문에 [dh = 200, dw = 100]
    cv2.add(green[100:300, 200:300], 50, green[100:300, 200:300])

    frame = cv2.merge([blue, green, red])

    cv2.rectangle(frame, (200, 100), (300, 300), (0, 0, 255), 3, cv2.LINE_4)    #(200,100)에서 100*200만큼의 관심영역 테두리 설정

    mask = np.zeros(frame.shape[:2], np.uint8)
    mask[100:200, 200:300] = 1

    sum_value = cv2.sumElems(frame)
    mean_value = cv2.mean(frame, mask)
    print("[sum_value] = ", sum_value)
    print("[mean_value] = ", mean_value)

    cv2.imshow(title, frame)

capture.release()