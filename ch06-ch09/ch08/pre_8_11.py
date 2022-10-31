import numpy as np,  cv2
from Common.interpolation import bilinear_value
from Common.utils import contain              # 사각형으로 범위 확인 함수

## rotat
def rotate_pt(img, degree, pt):
    dst = np.zeros(img.shape[:2], img.dtype)                     # 목적 영상 생성
    radian = (degree/180) * np.pi      # 반시계시 degree앞에 (-)                         # 회전 각도 - 라디언
    sin, cos = np.sin(radian), np.cos(radian)   # 사인, 코사인 값 미리 계산

    for i in range(img.shape[0]):                              # 목적 영상 순회 - 역방향 사상
        for j in range(img.shape[1]):
            jj, ii = np.subtract((j, i), pt)                # 중심좌표 평행이동,
            y = -jj * sin + ii * cos               # 회선 변환 수식
            x =  jj * cos + ii * sin
            x, y = np.add((x, y), pt)
            if contain((y, x), img.shape):                      # 입력 영상의 범위 확인
                dst[i, j] = bilinear_value(img, [x, y])           # 화소값 양선형 보간
    return dst

image = cv2.imread('C:/images/rotate.jpg', cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상 파일을 읽기 에러")

## 어파인 변환 행렬
center = (100, 100)
size = image.shape[::-1]

pt1 = np.array([( 30, 70),(20, 240), (300, 110)], np.float32)
pt2 = np.array([(120, 20),(10, 180), (280, 260)], np.float32)
aff_mat = cv2.getAffineTransform(pt1, pt2)              # 3개 좌표 쌍으로 어파인 행렬 생성
dst_affine = cv2.warpAffine(image, aff_mat, size, cv2.INTER_LINEAR) # opencv 어파인 변환

dst_affine= rotate_pt(image, 30, center)                                        # 원점 기준 회전 변환

cv2.imshow("image", image)
cv2.imshow("dst_affine-rotated on (100, 100)", dst_affine)
cv2.waitKey(0)