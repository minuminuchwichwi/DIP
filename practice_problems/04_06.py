#300행, 400열 행렬을 회색 바탕생(100)으로 생성 -> 500행 600열의 윈도우에 표시
import numpy as np
import cv2

image = np.zeros((300, 400), np.uint8)
image.fill(100)

title = "04_06"
cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)

cv2.imshow(title, image)
cv2.resizeWindow(title, 500, 600)
cv2.waitKey(0)
cv2.destroyAllWindows()