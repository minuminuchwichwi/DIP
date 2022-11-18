import numpy as np, cv2

# 낮은 임계값 th1바 생성
def bar1(value):
    global title, image, th1, th2, canny
    # 낮은 임계값 th1, 높은 임계값 th2
    th1 = cv2.getTrackbarPos('th1', title)
    # 구한 임계값으로 캐니 에지 검출
    canny = cv2.Canny(image, th1, th2)
    cv2.imshow(title, canny)

# 높은 임계값 th2바 생성
def bar2(value):
    global title, image, th1, th2, canny
    # 낮은 임계값 th1, 높은 임계값 th2
    th2 = cv2.getTrackbarPos('th2', title)
    # 구한 임계값으로 캐니 에지 검출
    canny = cv2.Canny(image, th1, th2)
    cv2.imshow(title, canny)

image = cv2.imread("C:/images/cannay_tset.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상파일 읽기 오류")
title = 'canny edge'

# opencv 캐니 에지 검출 / 낮은 임계값=50, 높은 임계값=150
th1, th2 = 100, 150
canny = cv2.Canny(image, th1, th2)

cv2.imshow(title, canny)
cv2.createTrackbar('th1', title, th1, 255, bar1)
cv2.createTrackbar('th2', title, th2, 255, bar2)
cv2.waitKey(0)
