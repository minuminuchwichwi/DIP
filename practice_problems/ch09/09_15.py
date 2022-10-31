import numpy as np, cv2
from Common.dct2d import dct2, idct2

def dct_8x8(img):
    dst = np.empty(img.shape, np.float32)
    for i in range(0, img.shape[0], 8):
        for j in range(0, img.shape[1], 8):
            block = img[i:i+8, j:j+8]
            dst[i:i+8, j:j+8] = dct2(block)
    return cv2.convertScaleAbs(dst)

def idct_8x8(img):
    dst = np.empty(img.shape, np.float32)
    for i in range(0, img.shape[0], 8):
        for j in range(0, img.shape[1], 8):
            block = img[i:i+8, j:j+8]
            dct_block = dct2(block)
            dst[i:i+8, j:j+8] = idct2(dct_block)
    return cv2.convertScaleAbs(dst)

image = cv2.imread('C:/images/dct.jpg', cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상 파일을 읽기 에러")

dst1 = dct_8x8(image)
dst2 = idct_8x8(image)

cv2.imshow('image', image)
cv2.imshow('8x8 dct', dst1)
cv2.imshow('8x8 idct', dst2)
cv2.waitKey(0)

