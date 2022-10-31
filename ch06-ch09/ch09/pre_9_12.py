import numpy as np, cv2, math
from Common.dft2d import exp, calc_spectrum, fftshift
from Common.fft2d import zeropadding

def butterfly(pair, L, N, dir):
    for k in range(L):                                       # 버터플라이 수행
        Geven, Godd = pair[k], pair[k + L]
        pair[k]     = Geven + Godd * exp(dir * k / N)       # 짝수부
        pair[k + L] = Geven - Godd * exp(dir * k / N)       # 홀수부

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

def fft2(image):
    pad_img = zeropadding(image)  # 영삽입
    tmp = [fft(row) for row in pad_img]
    dst = [fft(row) for row in np.transpose(tmp)]
    return np.transpose(dst)                        # 전치 환원 후 반환

## FFT 역변환
def ifft(g):
    fft = pairing(g, len(g), -1)
    return [v / len(g) for v in fft]

def ifft2(image):
    tmp = [ifft(row) for row in image]
    dst = [ifft(row) for row in np.transpose(tmp)]
    return np.transpose(dst)                        # 전치 환원 후 반환


image = cv2.imread('C:/images/dft_240.jpg', cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상파일 읽기 에러")

# zero
dft1 = fft2(image)                                # 2차원 DFT 수행
spectrum1 = calc_spectrum(fftshift(dft1))           # 셔플링후 주파수 스펙트럼 영상 생성
idft_zero = ifft2(dft1).real                          # 2차원 IDFT 수행

# non-zero
dft2 = np.fft.fft2(image)                                # 2차원 DFT 수행
idft_non_zere = np.fft.ifft2(dft2).real                          # 2차원 IDFT 수행

## 원본의 크기만큼의 관심 영역을 지정
roi = idft_zero[0:240, 0:240]

cv2.imshow("spectrum1", spectrum1)
cv2.imshow("idft_zero", cv2.convertScaleAbs(idft_zero))
cv2.imshow("idft_idft_non_zere", cv2.convertScaleAbs(idft_non_zere))
cv2.waitKey(0)