import numpy as np, cv2
from Common.fft2d import fft2, ifft2, calc_spectrum, fftshift

def onChange_alpha(value):
    global alpha, beta, title, dst, middlepassed_img, middlepass

    alpha = cv2.getTrackbarPos('alpha', title)
    middlepass = np.zeros(dft.shape, np.float32)
    cv2.circle(middlepass , (cx, cy), alpha, 1, -1)
    cv2.circle(middlepass, (cx, cy), beta, 0, -1)

    middlepassed_dft = dft * middlepass
    middlepassed_img = IFFT(middlepassed_dft, image.shape, mode)
    dst = calc_spectrum(middlepassed_dft)

    cv2.imshow(title, dst)
    cv2.imshow("middlepass_img", middlepassed_img)
def onChange_beta(value):
    global alpha, beta, title, dst, middlepassed_img, middlepass

    beta = cv2.getTrackbarPos('beta', title)
    middlepass = np.zeros(dft.shape, np.float32)
    cv2.circle(middlepass, (cx, cy), alpha, 1, -1)
    cv2.circle(middlepass, (cx, cy), beta, 0, -1)

    middlepassed_dft = dft * middlepass
    middlepassed_img = IFFT(middlepassed_dft, image.shape, mode)
    dst = calc_spectrum(middlepassed_dft)

    cv2.imshow(title, dst)
    cv2.imshow("middlepass_img", middlepassed_img)

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

image = cv2.imread('images/filter.jpg', cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상 파일 읽기 에러")
cy, cx = np.divmod(image.shape, 2)[0]                 # 행렬 중심점 구하기
mode = 1

alpha, beta = 90, 30

dft, spectrum = FFT(image, mode)                  # FFT 수행 및 셔플링
middlepass = np.zeros(dft.shape, np.float32)
cv2.circle(middlepass , (cx, cy), alpha, 1, -1)
cv2.circle(middlepass , (cx, cy), beta, 0, -1)

middlepassed_dft = dft * middlepass
middlepassed_img = IFFT(middlepassed_dft, image.shape, mode)

title = "middlepass_spect"

cv2.imshow("image", image)
cv2.imshow("spectrum_img", spectrum)
cv2.imshow(title, calc_spectrum(middlepassed_dft))
cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar("alpha", title, alpha, cx, onChange_alpha)
cv2.createTrackbar("beta", title, beta, cx, onChange_beta)
cv2.imshow("middlepass_img", middlepassed_img)

cv2.waitKey(0)