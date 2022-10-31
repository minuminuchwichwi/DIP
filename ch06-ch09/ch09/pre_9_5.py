import numpy as np, cv2
from Common.dft2d import dft

## 복소수 행렬 스펙트럼 계산
def calc_spectrum(complex):
    if complex.ndim == 2: dst = abs(complex)    # 복소수 객체 행렬 사용 - 2차원 행렬
    else: dst = cv2.magnitude(complex[:,:,0], complex[:,:,1])   # 복소수를 2채널로 구성 - 3차원 행렬
    dst = 20*np.log(dst+1)  # 로그 함수는 0에서 무한대이기 때문에 1을 더함
    return cv2.convertScaleAbs(dst) # 윈도우 표시 위해 unchar형 변환

## 1차원 DFT 2번 수행 -> 2차원 푸리에 변환
def dft2(image):
    tmp = [dft(row) for row in image]
    dst = [dft(row) for row in np.transpose(tmp)]
    return np.transpose(dst)                   # 전치 환원 후 반환

image = cv2.imread('C:/images/dft_64.jpg', cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상파일 읽기 에러")

dft = dft2(image)                     # 2차원 DFT 수행
spectrum1 = calc_spectrum(dft)

cv2.imshow("image", image)
cv2.imshow("spectrum1", spectrum1)
cv2.waitKey(0)