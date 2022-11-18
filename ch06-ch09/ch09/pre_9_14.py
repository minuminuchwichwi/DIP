import numpy as np, cv2
from Common.fft2d import fft2, ifft2, calc_spectrum, fftshift

def FFT(image, mode = 2):
    if mode == 1: dft = fft2(image)
    elif mode==2: dft = np.fft.fft2(image)
    elif mode==3: dft = cv2.dft(np.float32(image), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft = fftshift(dft)                              # 셔플링
    spectrum = calc_spectrum(dft)               # 주파수 스펙트럼 영상
    return dft, spectrum

def IFFT(dft, shape, mode=2):
    dft = fftshift(dft)                                 # 역 셔플링
    if mode == 1: img = ifft2(dft).real
    if mode == 2: img = np.fft.ifft2(dft).real
    if mode ==3:  img = cv2.idft(dft, flags= cv2.DFT_SCALE)[:,:,0]
    img = img[:shape[0], :shape[1]]                 # 영삽입 부분 제거
    return cv2.convertScaleAbs(img)

# low
def bar1(value):
    global title, low, high, dst, image, midpass, midpassed_dft, midpassed_img

    low = cv2.getTrackbarPos('low', title)
    midpass = np.zeros(dft.shape, np.float32)
    cv2.circle(midpass, (cx, cy), high, (1, 1), -1)
    cv2.circle(midpass, (cx, cy), low, (0, 0), -1)
    midpassed_dft = dft * midpass
    midpassed_img = IFFT(midpassed_dft, image.shape, mode)
    dst = calc_spectrum(midpassed_dft)

    cv2.imshow(title, dst)
    cv2.imshow("midpassed_img", midpassed_img)

# high
def bar2(value):
    global title, low, high, dst, image, midpass, midpassed_dft, midpassed_img

    high = cv2.getTrackbarPos('high', title)
    midpass = np.zeros(dft.shape, np.float32)
    cv2.circle(midpass, (cx, cy), high, (1, 1), -1)
    cv2.circle(midpass, (cx, cy), low, (0, 0), -1)
    midpassed_dft = dft * midpass
    midpassed_img = IFFT(midpassed_dft, image.shape, mode)
    dst = calc_spectrum(midpassed_dft)

    cv2.imshow(title, dst)
    cv2.imshow("midpassed_img", midpassed_img)

image = cv2.imread('C:/images/dft_240.jpg', cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상 파일 읽기 에러")
cy, cx = np.divmod(image.shape, 2)[0]                 # 행렬 중심점 구하기
mode = 1
title = 'midpass_frequency'

dft, spectrum = FFT(image, mode)                  # FFT 수행 및 셔플링
midpass = np.zeros(dft.shape, np.float32)

# case1 Low=30, High=60
high, low = 60, 30
cv2.circle(midpass, (cx, cy), high, (1,1), -1)
cv2.circle(midpass, (cx, cy), low, (0,0), -1)
midpassed_dft = dft * midpass
midpassed_img = IFFT(midpassed_dft, image.shape, mode)

cv2.imshow("image", image)
cv2.imshow("img_spectrum", spectrum)

# low, high값을 조절할 트랙바 달기
cv2.imshow(title, calc_spectrum(midpassed_dft))
cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar('low', title, low, cx, bar1)
cv2.createTrackbar('high', title, high, cx, bar2)
cv2.imshow("midpassed_img", midpassed_img)
cv2.waitKey(0)