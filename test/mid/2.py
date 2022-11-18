import numpy as np, cv2, time
#수행 시간 체크 함수.
#mode==0이면 시작시간, mode==1이면 종료시간을 구해 수행시간을 체크한다.
def ck_time(mode = 0):
    global stime
    if (mode ==0 ):
       stime = time.perf_counter()
    elif (mode==1):
       etime = time.perf_counter()
       print("수행시간 = %.5f sec" % (etime - stime))   #초 단위 경과 시간
#평균값 필터 함수
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

#중간값 필터 함수
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
def salt_pepper_noise(img, n):      #잡음 생성 함수
    h, w = img.shape[:2]
    x, y = np.random.randint(0, w, n), np.random.randint(0, h, n)
    noise = img.copy()
    for (x, y) in zip(x, y):
        noise[y, x] = 0 if np.random.rand() < 0.5 else 255
    return noise

image = cv2.imread("images/mid_fig2.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상파일 읽기 오류")

print("median 수행시간")
ck_time(0)
noise = salt_pepper_noise(image, 500)
med_img = median_filter(noise, 3)  # 사용자 정의 함수
ck_time(1)

print("average 수행시간")
ck_time(0)
avg_img = average_filter(image, 3)
ck_time(1)

difference = np.subtract(avg_img, med_img)  # median과 average를 비교하기 위해 두 영상의 차이를 구함.

cv2.imshow("image", image),
cv2.imshow("noise", noise),
cv2.imshow("median", med_img)
cv2.imshow("avg", avg_img)
cv2.imshow("difference", difference)
cv2.waitKey(0)