import numpy as np, cv2

image = cv2.imread("C:/images/laplacian.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상파일 읽기 오류")

## 라플라시안 4방향 필터 데이터
data1 = [	[0,		1,		0],  												# 4 방향 필터
			[1, 	-4,		1],
			[0, 	1,		0]]

## 라플라시안
mask4 = np.array(data1, np.int16)   # 음수가 있으므로 자료형이 int8인 행렬 선언
Laplacian = cv2.filter2D(image, cv2.CV_16S, mask4)

## LoG/DoG
gaus = cv2.GaussianBlur(image, (9,9), 0, 0)            # 가우시안 마스크 적용
LoG = cv2.Laplacian(gaus, cv2.CV_16S, 9)             # 라플라시안 수행

gaus1 = cv2.GaussianBlur(image, (3, 3), 0)          # 가우사안 블러링
gaus2 = cv2.GaussianBlur(image, (9, 9), 0)
DoG = gaus1 - gaus2          # DoG 수행

## 캐니
def nonmax_suppression(sobel, direct):  # 비최대치 억제 함수
    rows, cols = sobel.shape[:2]
    dst = np.zeros((rows, cols), np.float32)
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            # 관심 영역 참조 통해 이웃 화소 가져오기
            # 행렬 처리를 통해 이웃 화소 가져오기
            values = sobel[i-1:i+2, j-1:j+2].flatten()  # 중심 에지 주변 9개 화소 가져옴
            first = [3, 0, 1, 2]    # 첫 이웃 화소 좌표 4  (기울기 방향에 따라 두개의 이웃화소 선택)
            id = first[direct[i, j]]    # 방향에 따른 첫 이웃화소 위치
            v1, v2 = values[id], values[8-id]   # 두 이웃 화소 가져옴
                # 중심화소가 두 이웃화소보다 작으면 억제
            dst[i, j] = sobel[i, j] if (v1 < sobel[i , j] > v2) else 0
    return dst

def trace(max_sobel, i, j, low):
    h, w = max_sobel.shape
    if (0 <= i < h and 0 <= j < w) == False: return  # 추적 화소 범위 확인
    if pos_ck[i, j] == 0 and max_sobel[i, j] > low: # 추적 조건 확인
        pos_ck[i, j] = 255  # 추적 좌표 완료 표시
        canny[i, j] = 255   # 에지 지정

        trace(max_sobel, i - 1, j - 1, low)# 추적 함수 재귀 호출 - 8방향 추적
        trace(max_sobel, i    , j - 1, low)
        trace(max_sobel, i + 1, j - 1, low)
        trace(max_sobel, i - 1, j    , low)
        trace(max_sobel, i + 1, j    , low)
        trace(max_sobel, i - 1, j + 1, low)
        trace(max_sobel, i    , j + 1, low)
        trace(max_sobel, i + 1, j + 1, low)

def hysteresis_th(max_sobel, low, high):                # 이력 임계값 수행
    rows, cols = max_sobel.shape[:2]
    for i in range(1, rows - 1):  # 에지 영상 순회
        for j in range(1, cols - 1):
            if max_sobel[i, j] > high:  trace(max_sobel, i, j, low)  # 추적 시작

pos_ck = np.zeros(image.shape[:2], np.uint8)    # 추적 완료 점검 행렬
canny = np.zeros(image.shape[:2], np.uint8)     # 캐니 에지 행렬

# 사용자 정의 캐니 에지
gaus_img = cv2.GaussianBlur(image, (5, 5), 0.3)
Gx = cv2.Sobel(np.float32(gaus_img), cv2.CV_32F, 1, 0, 3)  # x방향 마스크
Gy = cv2.Sobel(np.float32(gaus_img), cv2.CV_32F, 0, 1, 3)  # y방향 마스크
sobel = cv2.magnitude(Gx, Gy)                            # 두 행렬 벡터 크기
# sobel = np.fabs(Gx) + np.fabs(Gy)                       # 두 행렬 절댓값 덧셈


directs = cv2.phase(Gx, Gy) / (np.pi / 4)   # 에지 기울기 계산 및 근사
directs = directs.astype(int) % 4   # 8방향 -> 4방향 축소
max_sobel = nonmax_suppression(sobel, directs)   # 비최대치 억제
hysteresis_th(max_sobel, 100, 150)          # 이력 임계값

cv2.imshow("image", image)
cv2.imshow("Laplacian 4-direction", cv2.convertScaleAbs(Laplacian))
cv2.imshow("LoG", LoG.astype("uint8"))
cv2.imshow("DoG", DoG)
cv2.imshow("canny", canny)                 # 사용자 정의 캐니
cv2.waitKey(0)