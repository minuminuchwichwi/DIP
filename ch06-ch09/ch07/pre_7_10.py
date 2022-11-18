import numpy as np, cv2
from Common.filters import filter

# 이미지 불러와 blue, green, red 3채널로 분리
image = cv2.imread("C:/images/filter_sharpen.jpg", cv2.IMREAD_COLOR)
if image is None: raise Exception("영상파일 읽기 오류")

blue, green, red = cv2.split(image)

# 블러링 마스크 원소 지정
# 1/9로 채워진 3x3 블러링 마스크 만들어주고 각 채널을 평균값 필터링
data1 = [ 1/9, 1/9, 1/9,    # 블러링 마스크 원소 지정
          1/9, 1/9, 1/9,
          1/9, 1/9, 1/9]
mask1 = np.array(data1, np.float32).reshape(3, 3)   # 마스크1 행렬 생성

blur_blue = filter(blue, mask1)
blur_green = filter(green, mask1)
blur_red = filter(red, mask1)
# 윈도우 표시 위한 행변환
bluring_blue = cv2.convertScaleAbs(blur_blue)
bluring_green = cv2.convertScaleAbs(blur_green)
bluring_red = cv2.convertScaleAbs(blur_red)
# 블러링된 3개의 채널 합칩 것과 블러링 opencv filter2D()함수 비교
blur_user = cv2.merge([bluring_blue, bluring_green, bluring_red])
blur_cv2 = cv2.filter2D(image, -1, mask1)

# 샤프닝 마스크 원소 지정
# 각 채널을 3x3 샤프닝 마스크 필터링
data2 = [ 0,-1, 0,
         -1, 5,-1,
          0,-1, 0]
mask2 = np.array(data2, np.float32).reshape(3, 3)
sharp_blue = filter(blue, mask2)
sharp_green = filter(green, mask2)
sharp_red = filter(red, mask2)
# 윈도우 표시 위한 행변환
sharpen_blue = cv2.convertScaleAbs(sharp_blue)
sharpen_green = cv2.convertScaleAbs(sharp_green)
sharpen_red = cv2.convertScaleAbs(sharp_red)

# 샤프닝된 3개의 채널 합친 것과 샤프닝 opencv filter2D()함수 비교
sharp_user = cv2.merge([sharpen_blue, sharpen_green, sharpen_red])
sharp_cv2 = cv2.filter2D(image, -1, mask2)

cv2.imshow("image", image)
cv2.imshow("blur_user", blur_user)
cv2.imshow("blur_cv2", blur_cv2)
cv2.imshow("sharp_user", sharp_user)
cv2.imshow("sharp_cv2", sharp_cv2)
cv2.waitKey(0)
