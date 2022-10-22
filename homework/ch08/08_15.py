import numpy as np, cv2, math

def contain(p, shape):
    return 0<= p[0] < shape[0] and 0<= p[1] < shape[1]
def bilinear_value(img, pt):
    x, y = np.int32(pt)
    if y >= img.shape[0]-1: y = y - 1
    if x >= img.shape[1]-1: x = x - 1

    P1, P2, P3, P4 = np.float32(img[y:y+2,x:x+2].flatten())
    alpha, beta = pt[1] - y,  pt[0] - x

    M1 = P1 + alpha * (P3 - P1)
    M2 = P2 + alpha * (P4 - P2)
    P  = M1 + beta  * (M2 - M1)
    return np.clip(P, 0, 255)

def get_Angle(x1, x2, y1, y2):
    x1, y1, x2, y2 = x1 - x1, y1 - y1, x2 - x1, y2 - y1
    radian = math.atan2(y2, x2)
    return radian

def rotate(img, radian):
    dst = np.zeros(img.shape[:2], img.dtype)
    b, g, r = cv2.split(img)
    sin, cos = np.sin(radian), np.cos(radian)

    for i in range(b.shape[0]):
        for j in range(b.shape[1]):
            y = -j * sin + i * cos
            x =  j * cos + i * sin
            if contain((y, x), b.shape):
                dst[i, j] = bilinear_value(b, [x, y])
    for i in range(g.shape[0]):
        for j in range(g.shape[1]):
            y = -j * sin + i * cos
            x =  j * cos + i * sin
            if contain((y, x), g.shape):
                dst[i, j] = bilinear_value(g, [x, y])
    for i in range(r.shape[0]):
        for j in range(r.shape[1]):
            y = -j * sin + i * cos
            x =  j * cos + i * sin
            if contain((y, x), r.shape):
                dst[i, j] = bilinear_value(r, [x, y])
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
        angle = get_Angle(x1, x2, y1, y2)
        dst = rotate(image, angle)
        cv2.imshow("image", tmp)
        cv2.imshow("dst", dst)

image = cv2.imread('images/rotate.jpg', cv2.IMREAD_COLOR)
if image is None: raise Exception("영상 파일을 읽기 에러")
tmp = np.copy(image)
pts = []

cv2.imshow("image", image)
cv2.setMouseCallback("image", onMouse, 0)

cv2.waitKey(0)