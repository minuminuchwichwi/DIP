import numpy as np, cv2, math

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
        length = math.sqrt(pow(abs(x2 - x1), 2) + pow(abs(y2 - y1), 2))
        gradient = (y2 - y1) / (x2 - x1)
        print("직선의 길이  : ", length)
        print("직선의 기울기 : ", gradient)
        cv2.imshow("image", tmp)

image = cv2.imread('images/rotate.jpg', cv2.IMREAD_COLOR)
if image is None: raise Exception("영상 파일을 읽기 에러")
tmp = np.copy(image)
pts = []

cv2.imshow("image", image)
cv2.setMouseCallback("image", onMouse, 0)

cv2.waitKey(0)