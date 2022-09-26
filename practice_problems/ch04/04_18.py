import numpy as np, cv2

image = np.full((400, 600, 3), (255,255,255), np.uint8)

size1 = (100, 100)
size2 = (size1[1]//2, size1[0]//2)
pt1 = (image.shape[1]//2, image.shape[0]//2)
pt2, pt3 = (pt1[1] + (size1[1] // 2), pt1[0] - 2*(size1[0] // 2)), (pt1[1] + 3*(size1[1] // 2), pt1[0] - 2*(size1[0] // 2))

cv2.ellipse(image, pt1, size1, 0, 0, 180, (255, 0, 0), -1)
cv2.ellipse(image, pt1, size1, 180, 0, 180, (0, 0, 255), -1)
cv2.ellipse(image, pt2, size2, 0, 0, 180, (0, 0, 255), -1)
cv2.ellipse(image, pt3, size2, 180, 0, 180, (255, 0, 0), -1)

cv2.imshow("image",image)
cv2.waitKey(0)
cv2.destroyAllWindows()