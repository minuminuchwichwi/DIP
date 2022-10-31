import numpy as np, cv2

image1 = cv2.imread("C:/images/add1.jpg", cv2.IMREAD_GRAYSCALE) # 영상읽기
image2 = cv2.imread("C:/images/add2.jpg", cv2.IMREAD_GRAYSCALE)
if image1 is None or image2 is None: raise Exception("영상파일 읽기 오류")
title = 'dst'   # 윈도우 이름

## 영상 합성 방법
alpha, beta = 0.6, 0.7  # 곱셈 비율
image3 = cv2.addWeighted(image1, alpha, image2, beta, 0)   # 두 영상 비율에 따른 더하기

# 영상 3개가 들어갈 배열 생성하고 영상 넣기
# opencv는 행렬계산 -> (x,y)가 아닌 (y,x)
y, x = image1.shape                                          # image1의 세로, 가로 길이
dst = np.zeros((y, x*3), np.uint8)                           # image1의 세로, 가로 * 3의 배열 생성
dst[0:y, 0:x] = image1[0:y, 0:x]                             # 배열의 맨 앞에 image1 넣기
dst[:, x*2:] = image2[0:y, 0:x]                              # 배열의 맨 뒤에 image2 넣기
dst[0:y, x:x*2] = image3[0:y, 0:x]                           # 배열의 가운데에 image3 넣기

cv2.imshow(title, dst)
cv2.waitKey(0)