#200행, 300열 행렬 2개 그림처럼 배치
import numpy as np, cv2

image = np.zeros((200, 300), np.uint8)
image[:] = 0

title1, title2 = "win mode1", "win mode2"

cv2.namedWindow(title1)
cv2.namedWindow(title2)
cv2.moveWindow(title1, 0, 0)
cv2.moveWindow(title2, image.shape[1], image.shape[0])

cv2.imshow(title1, image)
cv2.imshow(title2, image)

cv2.waitKey(0)
cv2.destroyAllWindows()