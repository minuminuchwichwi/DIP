# filter_average 와 filter_median 두 알고리즘 비교
import cv2
import numpy as np

# filter_average
def average_filter(image, ksize):
    rows, cols = image.shape[:2]
    dst = np.zeros((rows, cols), np.uint8)
    center = ksize // 2                                 # 마스크 절반 크기

    for i in range(rows):           # 입력 영상 순회
        for j in range(cols):
            y1, y2 = i - center, i + center + 1        # 마스크 높이 범위
            x1, x2 = j - center, j + center + 1        # 마스크 너비 범위
            if y1 < 0 or y2 > rows or x1 < 0 or x2 > cols :
                dst[i, j] = image[i, j]
            else:
                mask = image[y1:y2, x1:x2]                 # 범위 지정
                dst[i, j] = cv2.mean(mask)[0]
    return dst

# filter_median
def median_filter(image, ksize):
   rows, cols = image.shape[:2]
   dst = np.zeros((rows, cols), np.uint8)
   center = ksize // 2  # 마스크 절반 크기

   for i in range(center, rows - center):  # 입력 영상 순회
      for j in range(center, cols - center):
         y1, y2 = i - center, i + center + 1  # 마스크 높이 범위
         x1, x2 = j - center, j + center + 1  # 마스크 너비 범위
         mask = image[y1:y2, x1:x2].flatten()  # 마스크 영역

         sort_mask = cv2.sort(mask, cv2.SORT_EVERY_COLUMN)  # 정렬 수행
         dst[i, j] = sort_mask[sort_mask.size // 2]  # 출력화소로 지정
   return dst

# 소금과 후추
def salt_pepper_noise(img, n):
    h, w = img.shape[:2]
    x, y = np.random.randint(0, w, n), np.random.randint(0, h, n)
    noise = img.copy()
    for (x,y) in zip(x,y):
        noise[y, x] = 0 if np.random.rand() < 0.5 else 255
    return noise

image = cv2.imread("images/median2.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상파일 읽기 오류")

# 노이즈(소금 후추)
noise = salt_pepper_noise(image, 500)   # 500개의 소금 후추 잡음 생성
avg_img  = average_filter(noise, 5)     # 5의 의미 = 5x5크기 평균값 필터링 # 사용자 정의 평균값 필터 함수
med_img = median_filter(noise, 5)       # 5의 의미 = 5x5크기 미디언 필터링 # 사용자 정의  미디움 함수

# 두 영상의 절대값 차 연산
diff = cv2.absdiff(avg_img, med_img)

# 차 영상을 극대화 하기 위해 쓰레시홀드 처리 및 컬러로 변환
_, diff = cv2.threshold(diff, 1, 255, cv2.THRESH_BINARY)
diff_red = cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)
med_img = cv2.cvtColor(med_img, cv2.COLOR_GRAY2BGR)

# 채널을 맞추기 위해
diff_red[:,:,2] = 0
print(med_img.shape)
print(diff_red.shape)

# 비교 이미지 두 번째에 변화 부분 표시
spot = cv2.bitwise_xor(med_img, diff_red)

# 결과 영상 출력
cv2.imshow("nois_image", noise)
cv2.imshow("avg_img", avg_img)
cv2.imshow("median_img", med_img)
cv2.imshow("diff_img", diff)
cv2.imshow("spot", spot)
cv2.waitKey(0)