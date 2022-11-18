import numpy as np, cv2

def contain(p, shape):  # 좌표(y,x)가 범위 내 인지 검사
    return 0<=p[0] < shape[0] and 0<=p[1] < shape[1]

## subtrack 함수를 이용해 역방향 사상을 해주고, contain 함수로 범위 내에 있는 원소들만 출력
def translate(img, pt):
    dst = np.zeros(img.shape, img.dtype)    # 목적 영상 생성
    for i in range(img.shape[0]):   # 목적 영상 순회 - 역방향 사상
        for j in range(img.shape[1]):
            x, y = np.subtract((j,i), pt)
            if contain((y,x), img.shape):
                dst[i,j] = img[y,x]
    return dst

image = cv2.imread('C:/images/translate.jpg', cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상 파일을 읽기 에러")

rows, cols = image.shape[:2]
dx, dy = 50, 60
mtrx = np.float32([[1, 0, dx],   # 어파인 변환을 위한 평행이동 행렬
                   [0, 1, dy]])

dst1 = translate(image, (50, 60))   # translate() 함수로 평행이동
dst2 = cv2.warpAffine(image, mtrx, (cols+dx, rows+dy))    # opencv 어파인 변환으로 평행이동

cv2.imshow("image", image)
cv2.imshow("translate (50, 60)", dst1)
cv2.imshow("opencv 어파인 (50, 60)", dst2)
cv2.waitKey(0)