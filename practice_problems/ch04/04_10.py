import numpy as np, cv2

def onMouse(event, x, y, flags, param):
    global title

    if event == cv2.EVENT_RBUTTONDOWN:
        cv2.circle(image, (x, y), 20, (0, 0, 255), 3)
    elif event == cv2.EVENT_LBUTTONDOWN:
        cv2.rectangle(image, (x, y), (x+30, y+30), (255, 0, 0), 3)

    cv2.imshow(title, image)

image = np.zeros((200, 300, 3), np.uint8)
image[:] = (255, 255, 255)
title = "04_10"

cv2.imshow(title, image)
cv2.setMouseCallback(title, onMouse)
cv2.waitKey(0)
cv2.destroyAllWindows()