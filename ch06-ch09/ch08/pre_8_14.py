import numpy as np, cv2, math

# 예제 8.4.1의 평행이동 함수를 참조
def contain(p, shape):  # 좌표 (y,x)가 범위내 인지 검사
    return 0<=p[0] < shape[0] and 0<=p[1] < shape[1]

def translate(img, pt):
    dst = np.zeros(img.shape, img.dtype)    # 목적 영상 생성
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            x, y = np.subtract((j, i), pt)
            if contain((y, x), img.shape):
                dst[i, j] = img[y, x]
    return dst

## 드래그의 시작점과 종료점의 좌표 원을 그리고 좌표를 출력
def draw_point(x, y):
    pts.append([x,y])
    print("좌표:", len(pts), [x,y])
    cv2.circle(tmp, (x,y), 2, 255, 2)   # 중심 좌표 표시
    cv2.imshow("image", tmp)

## 드래그의 시작점과 종료점에 draw_point 함수를 이용해 점을 그려주고 각각의 좌표의
## x축, y축 차분만큼 영상을 평행이동 시켜주는 함수
def onMouse(event, x, y, flags, param):
    global tmp, pts
    if (event == cv2.EVENT_LBUTTONDOWN and len(pts) == 0): draw_point(x, y)
    if (event == cv2.EVENT_LBUTTONUP and len(pts) == 1): draw_point(x, y)
    if len(pts) == 2:
        d = np.subtract(pts[1], pts[0])
        print("평행 이동 거리 : x축 : %3.2f" % d[0], "y축 : %3.2f" % d[1])
        dst = translate(image, (d[0], d[1]))
        cv2.imshow("image", dst)
        pts=[]

image = cv2.imread("C:/images/rotate.jpg", cv2.IMREAD_COLOR)
if image is None: raise Exception("영상 파일을 읽기 에러")
tmp = np.copy(image)
pts = []

cv2.imshow("image", image)
cv2.setMouseCallback("image", onMouse, 0)
cv2.waitKey(0)
