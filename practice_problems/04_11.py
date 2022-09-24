import numpy as np, cv2

def onMouse(event, x, y, flags, param):
    global title, rad, line

    if event == cv2.EVENT_RBUTTONDOWN:
        cv2.circle(image, (x, y), rad, (0, 0, 255), line)
        print("반지름 : %d, 선 굵기 : %d인 원 생성"%(rad, line))
    elif event == cv2.EVENT_LBUTTONDOWN:
        cv2.rectangle(image, (x, y), (x+30, y+30), (255, 0, 0), line)
        print("선 굵기 : %d인 정사각형 생성"%line)

    cv2.imshow(title, image)

def line_trackbar(value):
    global line
    line = value
    print("선 굵기 트랙바 값 : ", line)
def radius_trackbar(value):
    global rad
    rad = value
    print("반지름 트랙바 값 : ", rad)

image = np.zeros((600, 600, 3), np.uint8)
image[:] = (255, 255, 255)
title = "04_10"

cv2.imshow(title, image)

rad, line = 20, 3

cv2.createTrackbar('radius', title, 20, 100, radius_trackbar)
cv2.setTrackbarMin('radius', title, 1)
cv2.createTrackbar('thickness', title, 3, 10, line_trackbar)
cv2.setTrackbarMin('thickness', title, 1)

cv2.setMouseCallback(title, onMouse)
cv2.waitKey(0)
cv2.destroyAllWindows()