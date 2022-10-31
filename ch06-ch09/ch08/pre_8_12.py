import numpy as np,  cv2
from Common.interpolation import bilinear_value
from Common.utils import contain              # 사각형으로 범위 확인 함수

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

## cv2.split 함수를 추가해 R,G,B 채널로 분리해서 각각 rotate()함수로 회전 변환
image = cv2.imread('C:/images/rotate.jpg', cv2.IMREAD_COLOR)
if image is None: raise Exception("영상 파일을 읽기 에러")

blue, green, red = cv2.split(image)
blue_rotation = rotate(blue, 20)
green_rotation = rotate(green, 20)
red_rotation = rotate(red, 20)

dst = cv2.merge([blue_rotation, green_rotation, red_rotation])

cv2.imshow("image", image)
cv2.imshow("dst", dst)
cv2.waitKey(0)