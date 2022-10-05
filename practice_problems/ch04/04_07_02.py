import numpy as np, cv2

def onMouse(event, x, y, flags, param):
    global title, pt
    if event == cv2.EVENT_LBUTTONDOWN:
        if pt[0] < 0: pt = (x, y)
        else:
            cv2.circle(image, pt, 5, 100, 1)
            cv2.imshow(title, image)
            pt = (-1, -1)
    elif event == cv2.EVENT_RBUTTONDOWN:
        if pt[0] < 0: pt = (x, y)
        else:
            cv2.rectangle(image, pt, (pt[0]+30, pt[1]+30), 100, 2)
            cv2.imshow(title, image)
            pt = (-1, -1)

image = np.ones((300, 300), np.uint8) * 255

title = "Draw Event"
pt = (-1, -1)
cv2.namedWindow(title)
cv2.imshow(title, image)
cv2.setMouseCallback(title, onMouse)
cv2.waitKey(0)
cv2.destroyAllWindows()