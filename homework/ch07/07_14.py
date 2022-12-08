import numpy as np, cv2

def onChange_th1(value):
    global th1, th2, title, image, dst

    th1 = cv2.getTrackbarPos('th1', title)

    dst = cv2.Canny(image, th1, th2)

    cv2.imshow(title, dst)
def onChange_th2(value):
    global th1, th2, title, image, dst

    th2 = cv2.getTrackbarPos('th2', title)

    dst = cv2.Canny(image, th1, th2)

    cv2.imshow(title, dst)

image = cv2.imread("images/cannay_tset.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상 파일 읽기 오류")

title = "canny edge"

#임계값 초기설정
th1, th2 = 100, 150
canny = cv2.Canny(image, th1, th2)

cv2.imshow(title, canny)
cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar("th1", title, th1, 250, onChange_th1)
cv2.createTrackbar("th2", title, th2, 250, onChange_th2)

cv2.waitKey(0)