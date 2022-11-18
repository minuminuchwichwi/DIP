import numpy as np, cv2
from Common.filters import filter

def differential(image, data1, data2):
    mask1 = np.array(data1, np.float32).reshape(3, 3)
    mask2 = np.array(data2, np.float32).reshape(3, 3)

    dst1 = filter(image, mask1)
    dst2 = filter(image, mask2)
    dst = cv2.magnitude(dst1, dst2)
    dst1, dst2 = np.abs(dst1), np.abs(dst2)

    dst = np.clip(dst, 0, 255).astype("uint8")
    dst1 = np.clip(dst1, 0, 255).astype("uint8")
    dst2 = np.clip(dst2, 0, 255).astype("uint8")
    return dst, dst1, dst2


image = cv2.imread("C:/images/edge.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상파일 읽기 오류")

# 로버츠 데이터
data1 = [-1, 0, 0,
         0, 1, 0,
         0, 0, 0]
data2 = [0, 0, -1,
         0, 1, 0,
         0, 0, 0]
# 프리윗 데이터
data3 = [-1, 0, 1,
         -1, 0, 1,
         -1, 0, 1]
data4 = [-1,-1,-1,
          0, 0, 0,
          1, 1, 1]
# 소벨 데이터
data5 = [-1, 0, 1,
         -2, 0, 2,
         -1, 0, 1]
data6 = [-1,-2,-1,
          0, 0, 0,
          1, 2, 1]

roberts, dst1, dst2 = differential(image, data1, data2)

prewitt, dst1, dst2 = differential(image, data3, data4)

sobel, dst1, dst2 = differential(image, data5, data6)

cv2.imshow("image", image)
cv2.imshow("roberts edge", roberts)
cv2.imshow("prewitt edge", prewitt)
cv2.imshow("sobel edge", sobel)
cv2.waitKey(0)