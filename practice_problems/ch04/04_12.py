import numpy as np
import cv2

def onChange(value):
    global image, title

    image[:] = cv2.getTrackbarPos('Brightness', title)
    cv2.imshow(title, image)

image = np.zeros((300, 500), np.uint8)

title = 'Trackbar Event'
cv2.imshow(title, image)

cv2.createTrackbar('Brightness', title, image[0][0], 255, onChange)

while True:
    key = cv2.waitKeyEx(100)
    if key == 27:break

    if key == 0x250000 or key == 0x280000:
        result = cv2.getTrackbarPos('Brightness', title)
        cv2.setTrackbarPos('Brightness', title, result - 1)
    elif key == 0x260000 or key == 0x270000:
        result = cv2.getTrackbarPos('Brightness', title)
        cv2.setTrackbarPos('Brightness', title, result + 1)

    cv2.imshow(title, image)

cv2.waitKey(0)
cv2.destroyAllWindows()