import numpy as np, cv2

image = cv2.imread("example.jpg", cv2.IMREAD_GRAYSCALE) #이미지를 그레이스케일로 읽음

_, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)     #이미지를 이진화시킴
binary_image[binary_image == 0] = 1
binary_image[binary_image == 255] = 0                                   #이진화된 결과를 반전

#문제에서 주어진 cv2.reduce()를 사용하여 수식 계산
histo_vy = cv2.reduce(binary_image, 1, 0, cv2.REDUCE_SUM, dtype=cv2.CV_32F)       #수평 수식
histo_vx = cv2.reduce(binary_image, 0, 0, cv2.REDUCE_SUM, dtype=cv2.CV_32F)       #수직 수식

#line함수를 사용할 수 있도록 1차원 행렬을 1행n열로 전치
histo_vx = histo_vx.T

height, width = binary_image.shape                      #이미지의 크기만큼 높이와 너비 설정
horizon_histogram = np.zeros((height, width, 3), np.uint8)       #수평방향 투영 히스토그램을 위해 이미지와 같은 크기의 검은화면 출력
vertical_histogram = np.zeros((height, width, 3), np.uint8)      #수직방향 투영 히스토그램을 위해 이미지와 같은 크기의 검은화면 출력

#수평방향 투영 히스토그램 구현
#윈도우의 왼쪽 끝에서 시작해 오른쪽으로 뻗어가는 선을 통한 히스토그램
#(0, row)에서 시작해 (계산된 수식*gap, row)에서 끝나는 라인을 계속 그려 나감
for row in range(height-1):
    cv2.line(horizon_histogram, (0, row), (int(histo_vy[row]*width/height), row), (255, 255, 255), 1)
#수직방향 투영 히스토그램 구현
#윈도우의 위쪽에서 아래쪽으로 뻗어가는 선을 통한 히스토그램
for col in range(width-1):
    cv2.line(vertical_histogram, (col,0), (col,int(histo_vx[col]*width/height)), (255,255,255), 1)
vertical_histogram = cv2.flip(vertical_histogram, 0)      #위와 거의 동일하지만 이미지 상하 반전을 통해 아래에서 위로 뻗어갈 수 있도록 히스토그램 수정

#원본 이미지와 수평, 수직으로 투영한 히스토그램을 윈도우에 띄움
cv2.imshow("image", binary_image+255)
cv2.imshow("horizion", horizon_histogram)
cv2.imshow("vertical", vertical_histogram)

cv2.waitKey(0)