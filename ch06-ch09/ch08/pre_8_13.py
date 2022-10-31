import numpy as np, cv2, math

## 두 좌표를 입력받아서 이은 직선의 기울기를 구하는 함수
def calc_gradient(pt):
    d = np.subtract(pts[1], pts[0])
    gradient = -d[1]/d[0]
    return gradient
## 두 좌표를 입력받아서 이은 직선의 길이를 구하는 함수
def calc_length(pt):
    d = np.subtract(pts[1], pts[0])
    length = math.sqrt(pow(d[1], 2) + pow(d[0], 2))
    return length

## 값이 잘 나왔는지 확인하기 위해 드래그한 두 좌표를 출력
def print_point(x, y):
    pts.append([x, y])
    print("좌표:", len(pts), [x,y])

## 마우스 드래그 시작점과 종료점에서 좌표를 출력해주고 직선을 그어준 후에 그 직선의
## 기울기와 길이를 출력해주는 onMouse 함수를 정의
def onMouse(event, x, y, flags, param):
    global tmp, pts
    if (event == cv2.EVENT_LBUTTONDOWN and len(pts) == 0): print_point(x,y)
    if (event == cv2.EVENT_LBUTTONUP and len(pts) == 1): print_point(x, y)
    if len(pts) == 2:
        gradient = calc_gradient(pts)
        length = calc_length(pts)
        print("길이 : %3.2f" % length)
        print("기울기 : %3.2f" % gradient)
        cv2.line(tmp, pts[0], pts[1], (0, 255, 255), 2, cv2.LINE_AA)
        pts=[]
    cv2.imshow("image", tmp)

image = cv2.imread("C:/images/rotate.jpg", cv2.IMREAD_COLOR)
if image is None: raise Exception("영상파일 읽기 에러")
tmp = np.copy(image)
pts = []

cv2.imshow("image", image)
cv2.setMouseCallback("image", onMouse, 0)
cv2.waitKey(0)