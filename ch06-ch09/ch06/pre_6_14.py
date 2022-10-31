# 2차원 히스토그램 Hue(세로), Saturation(가로)의 2개 축
import numpy as np, cv2

hscale = 32

# RGB 이미지를 HSV 색상공간으로 변환
BGR_img = cv2.imread("C:/images/color_space.jpg", cv2.IMREAD_COLOR)
if BGR_img is None: raise Exception("영상파일 읽기 오류")
# HSV 컬러 공간 변환
HSV_img = cv2.cvtColor(BGR_img, cv2.COLOR_BGR2HSV)

# 2차원 히스토그램(색상, 채도)
hist = cv2.calcHist([HSV_img], [0, 1], None, [180, 256], [0, 180, 0, 256])
# 180행 256열의 3채널 행렬 생성
hsv_map = np.zeros((180, 256, 3), np.uint8)

# 0채널 H(색상), 1채널 S(채도), 2채널 V(명도) -> 3채널 2차원 배열
h, s = np.indices(hsv_map.shape[:2])
hsv_map[:, :, 0] = h    # 0채널 Hue(색상)
hsv_map[:, :, 1] = s    # 1채널 Saturation(채도)
#밝기=빈도값으로, 3채널 V공간의 값=H와 S에 대한 2차원 히스토그램의 결과값
hsv_map[:, :, 2] = hist # 2채널 히스토그램의 빈도값

# HSV공간으로 변환한 이미지와 위 배열을 곱하여 빈도값을 밝기로 설정
hist = np.clip(hist*0.005*hscale, 0, 1) # 스케일링
hist = hsv_map*hist[:, :, np.newaxis] / 255 # 이미지와 HSV색상 맵의 곱

cv2.imshow("BGR_img", BGR_img)  # 원본
cv2.imshow("HSV_img", HSV_img)  # HSV
cv2.imshow("Hist2D", hist) # 빈도값 밝기 표현

cv2.waitKey(0)
