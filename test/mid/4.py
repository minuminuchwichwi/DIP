import numpy as np, cv2, math

def exp(knN):
    th = -2 * math.pi * knN
    return complex(math.cos(th), math.sin(th))
def zeropadding(img):
    h, w = img.shape[:2]
    m = 1 << int(np.ceil(np.log2(h)))         # 2의 자승 계산
    n = 1 << int(np.ceil(np.log2(w)))
    dst = np.zeros((m, n), img.dtype)        # 2의 자승 크기 영상 생성
    dst[0:h, 0:w] = img[:]                         # 자승 영상에 원본 영상 복사
    return dst
def butterfly(pair, L, N, dir):
    for k in range(L):                                       # 버터플라이 수행
        Geven, Godd = pair[k], pair[k + L]
        pair[k]     = Geven + Godd * exp(dir * k / N)       # 짝수부
        pair[k + L] = Geven - Godd * exp(dir * k / N)
def pairing(g, N, dir, start=0, stride=1):
    if N == 1: return [g[start]]
    L = N // 2
    sd = stride * 2
    part1 = pairing(g, L, dir, start, sd)
    part2 = pairing(g, L, dir, start + stride, sd)
    pair = part1 + part2                                     # 결과 병합
    butterfly(pair, L, N, dir)
    return pair
def fft(g):
    return pairing(g, len(g), 1)
def ifft(g):
    fft = pairing(g, len(g), -1)
    return [v / len(g) for v in fft]
def fft2(image):
    pad_img = zeropadding(image)  # 영삽입
    tmp = [fft(row) for row in pad_img]
    dst = [fft(row) for row in np.transpose(tmp)]
    return np.transpose(dst)
def ifft2(image):
    tmp = [ifft(row) for row in image]
    dst = [ifft(row) for row in np.transpose(tmp)]
    return np.transpose(dst)
def calc_spectrum(complex):
    if complex.ndim == 2: dst = abs(complex)                   # sqrt(re^2 + im^2) 계산
    else: dst = cv2.magnitude(complex[:,:,0], complex[:,:,1])
    dst = 20*np.log(dst+1)
    return cv2.convertScaleAbs(dst)
def fftshift(img):
    dst = np.zeros(img.shape, img.dtype)
    h, w = dst.shape[:2]
    cy, cx = h // 2, w // 2                     # 나누기 하며 소수점 절삭
    dst[h-cy:, w-cx:] = np.copy(img[0:cy , 0:cx ])      # 1사분면 -> 3사분면
    dst[0:cy , 0:cx ] = np.copy(img[h-cy:, w-cx:])      # 3사분면 -> 1사분면
    dst[0:cy , w-cx:] = np.copy(img[h-cy:, 0:cx ])      # 2사분면 -> 4사분면
    dst[h-cy:, 0:cx ] = np.copy(img[0:cy , w-cx:])      # 4사분면 -> 2사분면
    return dst

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

image = cv2.imread('images/mid_fig4.jpg', cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상 파일 읽기 에러")

mode = 1

alpha, beta = 90, 30

dft, spectrum = FFT(image, mode)                  # FFT 수행 및 셔플링
cy, cx = np.divmod(spectrum.shape, 2)[0]                 # 행렬 중심점 구하기
middlepass = np.zeros(dft.shape, np.float32)
cv2.circle(middlepass , (cx, cy), alpha, 1, -1)
cv2.circle(middlepass , (cx, cy), beta, 0, -1)

middlepassed_dft = dft * middlepass
middlepassed_img = IFFT(middlepassed_dft, image.shape, mode)

title = "middlepass_spect"

cv2.imshow("image", image)
cv2.imshow("spectrum_img", spectrum)
cv2.imshow(title, calc_spectrum(middlepassed_dft))
cv2.namedWindow(title)
cv2.createTrackbar("alpha", title, alpha, cx, onChange_alpha)
cv2.createTrackbar("beta", title, beta, cx, onChange_beta)
cv2.imshow("middlepass_img", middlepassed_img)

cv2.waitKey(0)