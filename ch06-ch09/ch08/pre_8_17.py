import numpy as np, cv2

image = cv2.imread("C:/images/translate.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상파일 읽기 에러")

h, w = image.shape

# flip1은 좌우대칭 변환 행렬 = 영상의 가로 길이 (w-1)만큼 가로로 평행 이동
flip1 = np.float32([[-1, 0, w-1],
                     [0, 1, 0]])
# flip2는 상하대칭 변환 행렬 = 영상의 세로 길이 (h-1)만큼 세로로 평행 이동
flip2 = np.float32([[1, 0, 0],
                    [0, -1, h-1]])
# flip3은 상하좌우 대칭 변환 행렬 = 영상의 세로 길이 (h-1)만큼 세로로 평행 이동
# 영상의 가로 길이 (w-1)만큼 가로로 평행 이동
flip3 = np.float32([[-1, 0, w-1],
                    [0, -1, h-1]])

dst1 = cv2.warpAffine(image, flip1, (w,h))
dst2 = cv2.warpAffine(image, flip2, (w,h))
dst3 = cv2.warpAffine(image, flip3, (w,h))

cv2.imshow("image", image);         cv2.imshow("flip1", dst1)
cv2.imshow("flip2", dst2);          cv2.imshow("flip3", dst3)
cv2.waitKey()