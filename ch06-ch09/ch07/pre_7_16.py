import numpy as np, cv2

# 침식 연산인 erode()함수와 팽창 연산인 dilate() 함수는 morphology함수 내의
# (if, elif)를 제외하고는 사실상 같음. 따라서, type 인수를 0 또는 1로 입력
# 받아서 if 구문으로 침식 또는 팽창 연산을 선택할 수 있도록 morphology 함수 정의
def morphology(img, mask=None, type=None):
    dst = np.zeros(img.shape, np.uint8)
    if mask is None: mask = np.ones((3,3), np.uint8)
    ycenter, xcenter = np.divmod(mask.shape[:2], 2)[0]

    mcnt = cv2.countNonZero(mask)
    for i in range(ycenter, img.shape[0] - ycenter):    # 입력 행령 반복 순회
        for j in range(xcenter, img.shape[1] - xcenter):
            y1, y2 = i - ycenter, i + ycenter + 1   # 마스크 높이 범위
            x1, x2 = j - xcenter, j + xcenter + 1   # 마스크 너비 범위
            roi = img[y1:y2, x1:x2]     # 마스크 영역
            temp = cv2.bitwise_and(roi, mask)
            cnt = cv2.countNonZero(temp)    # 일치한 화소수 계산
            # 0 = 팽창, 1 = 침식
            if(type == 0):
                dst[i, j] = 0 if (cnt == 0) else 255
            elif(type == 1):
                dst[i, j] = 255 if (cnt == mcnt) else 0
    return dst

image = cv2.imread("C:/images/morph.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상파일 읽기 오류")

mask = np.array([[0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]]).astype("uint8")
th_img = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)[1]   # 영상 이진화
# type = 1 침식 # 사용자 정의 함수와 opencv 제공 함수 차이 확인
# 검은 배경의 노이즈 제거, 글자 속 노이즈 선명
dst_erode = morphology(th_img, mask, 1)
dst_erode_opencv = cv2.morphologyEx(th_img, cv2.MORPH_ERODE, mask)
# type = 0 팽창 # 사용자 정의 함수와 opencv 제공 함수 차이 확인
# 검은 배경의 노이즈 선명, 글자 속 노이즈 제거
dst_dilate = morphology(th_img, mask, 0)
dst_dilate_opencv = cv2.morphologyEx(th_img, cv2.MORPH_DILATE, mask)

cv2.imshow("image", image)
cv2.imshow("dst_erode-user", dst_erode)
cv2.imshow("dst_erode-opencv", dst_erode_opencv)
cv2.imshow("dst_dilate-user", dst_dilate)
cv2.imshow("dst_dilate_opencv", dst_dilate_opencv)
cv2.waitKey(0)
