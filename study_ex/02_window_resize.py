import numpy as np
import cv2

image = np.zeros((200, 300), np.uint8)
image.fill(200)

title1, title2 = 'AUTOSIZE', 'NORMAL'
cv2.namedWindow(title1, 1)
cv2.namedWindow(title2, 0)

cv2.imshow(title1, image)
cv2.imshow(title2, image)
cv2.resizeWindow(title1, 400, 300)
cv2.resizeWindow(title2, 400, 300)
cv2.waitKey(0)
cv2.destroyAllWindows()