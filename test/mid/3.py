import numpy as np, cv2, math

def contain(p, shape):                              # 좌표(y,x)가 범위내 인지 검사
    return 0<= p[0] < shape[0] and 0<= p[1] < shape[1]
def translate(img, pt):
    dst = np.zeros(img.shape, img.dtype)            # 목적 영상 생성
    for i in range(img.shape[0]):                           # 목적 영상 순회 - 역방향 사상
        for j in range(img.shape[1]):
            x, y = np.subtract((j, i) , pt)
            if contain((y, x), img.shape):
                dst[i, j] = img[y, x]
    return dst
def draw_point(x, y):
    pts.append([x,y])
    print("분수대 중심 좌표:", len(pts), [x,y])
    cv2.circle(tmp, (x, y), 2, 255, 2)  # 중심 좌표 표시
    cv2.imshow("image", tmp)

def onMouse(event, x, y, flags, param):
    global tmp, pts, x1, y1

    if (event == cv2.EVENT_LBUTTONDOWN and len(pts) == 0):
        draw_point(x, y)
        x1, y1 = [x, y]
        cv2.circle(tmp, (x1, y1), 1, 255, 2)
        distance = center - (x1, y1)                        #분수대 중심을 영상의 중심좌표로 이동시키기 위해 두 점간의 차이를 구함.
        dst = translate(image, (distance[0], distance[1]))
        cv2.imshow("dst", dst)

image = cv2.imread('images/mid_fig3.jpg', cv2.IMREAD_COLOR)
if image is None: raise Exception("영상 파일을 읽기 에러")
tmp = np.copy(image)
pts = []
center = np.divmod(image.shape[::-1], 2)[0][1:]
print("영상의 중심 좌표", center)

cv2.imshow("image", image)
cv2.setMouseCallback("image", onMouse, 0)

cv2.waitKey(0)