import numpy as np, cv2, math
from Common.interpolation import bilinear_value
from Common.utils import contain              # 사각형으로 범위 확인 함수

# 회전 변환 함수 참조
def rotate(img, degree):
    dst = np.zeros(img.shape[:2], img.dtype)                     # 목적 영상 생성
    radian = (degree/180) * np.pi                               # 회전 각도 - 라디언
    sin, cos = np.sin(radian), np.cos(radian)   # 사인, 코사인 값 미리 계산

    for i in range(img.shape[0]):                                       # 목적 영상 순회 - 역방향 사상
        for j in range(img.shape[1]):
            y = -j * sin + i * cos
            x =  j * cos + i * sin                  # 회선 변환 수식
            if contain((y, x), img.shape):             # 입력 영상의 범위 확인
                dst[i, j] = bilinear_value(img, [x, y])           # 화소값 양선형 보간
    return dst

## 우선 두 좌표를 입력받아서 이은 직선의 기울기를 구하는 함수
def calc_gradient(pt):
    d = np.subtract(pts[1], pts[0])
    gradient = -d[1]/d[0]
    return gradient

## 값이 잘 나왔는지 확인하기 위해 드래그한 두 좌표를 출력
def print_point(x, y):
    pts.append([x, y])
    print("좌표:", len(pts), [x,y])

# rotate 함수는 양수가 반시계 방향 회전을 해주기 때문에 각도에 (-) 음수 부호
# atan 값이 라디안 값으로 나와서 '180/파이' 를 곱해주는 함수
def calc_angle(pts):
    d = np.subtract(pts[1], pts[0]).astype(float)  # 두 좌표간 차분 계산
    angle = math.atan(-abs(d[1]/d[0]))*180/np.pi
    return angle

## 드래그 두 좌표를 지정하고 두 좌표를 이은 직선을 그어준 후, 다시 클릭했을 때 기울기와
## 회전각을 콘솔창에 출력해주고 영상의 기울기를 보정해주는 onMouse 함수
def onMouse(event, x, y, flags, param):
    global tmp, pts
    if (event == cv2.EVENT_LBUTTONDOWN and len(pts) == 0): print_point(x, y)
    if (event == cv2.EVENT_LBUTTONUP and len(pts) == 1):
        print_point(x, y)
        cv2.line(tmp, pts[0], pts[1], (0, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow("image", tmp)
    if (event == cv2.EVENT_LBUTTONDOWN and len(pts) == 2):
        angle = calc_angle(pts) # 회전각 계산
        gradient = calc_gradient(pts)
        print("회전각 : %3.2f" % angle)
        print("기울기 : %3.2f" % gradient)
        dst = rotate(image, angle)  # 사용자 정의 함수 회전 수행
        cv2.imshow("image", dst)    # 연습문제 opencv 이용해 컬러 영상으로 수행 작성
        tmp = np.copy(image)    # 임시 행렬 초기화
        pts = []


image = cv2.imread('C:/images/rotate.jpg', cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상 파일을 읽기 에러")

tmp = np.copy(image)
pts = []

cv2.imshow("image", image)
cv2.setMouseCallback("image", onMouse, 0)
cv2.waitKey(0)