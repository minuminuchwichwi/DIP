#600행, 400열 윈도우를 만들고 (100,100)에 200*300크기의 빨간 사각형 그리기
import numpy as np, cv2

image = np.zeros((600, 400, 3), np.uint8)
image[:] = (255, 255, 255)

cv2.rectangle(image, (100, 100), (300, 400), (0, 0, 255), 3)    #굵기를 3으로

cv2.imshow("04_09", image)

cv2.waitKey(0)
cv2.destroyAllWindows()