import numpy as np, cv2, math

def contain(p, shape):
    return 0<= p[0] < shape[0] and 0<= p[1] < shape[1]

def translate(img, pt):
    dst = np.zeros(img.shape, img.dtype)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            x, y = np.subtract((j, i) , pt)
            if contain((y, x), img.shape):
                dst[i, j] = img[y, x]
    return dst

def draw_point(x, y):
    pts.append([x,y])
    print("좌표:", len(pts), [x,y])
    cv2.circle(tmp, (x, y), 2, 255, 2)  # 중심 좌표 표시
    cv2.imshow("image", tmp)

def onMouse(event, x, y, flags, param):
    global tmp, pts, x1, y1, x2, y2
    if (event == cv2.EVENT_LBUTTONDOWN and len(pts) == 0):
        draw_point(x, y)
        x1, y1 = [x, y]
    if (event == cv2.EVENT_LBUTTONUP and len(pts) == 1):
        draw_point(x, y)
        x2, y2 = [x, y]
        cv2.line(tmp, (x1, y1), (x2, y2), 255, 2)
        dst = translate(image, ((x2 - x1), (y2 - y1)) )
        cv2.imshow("image", tmp)
        cv2.imshow("dst", dst)

image = cv2.imread('images/rotate.jpg', cv2.IMREAD_COLOR)
if image is None: raise Exception("영상 파일을 읽기 에러")
tmp = np.copy(image)
pts = []

cv2.imshow("image", image)
cv2.setMouseCallback("image", onMouse, 0)

cv2.waitKey(0)