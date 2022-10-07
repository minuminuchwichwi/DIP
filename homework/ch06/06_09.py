import numpy as np, cv2

def onChange_alpha(value):
    global alpha, beta, title, image1, image2, dst

    alpha = cv2.getTrackbarPos('image1', title) / 100

    image3 = cv2.addWeighted(image1, alpha, image2, beta, 0)
    dst[0:h, w:w*2] = image3[0:h, 0:w]

    cv2.imshow(title, dst)
def onChange_beta(value):
    global alpha, beta, title, image1, image2, dst

    beta = cv2.getTrackbarPos('image2', title) / 100

    image3 = cv2.addWeighted(image1, alpha, image2, beta, 0)
    dst[0:h, w:w*2] = image3[0:h, 0:w]

    cv2.imshow(title, dst)


image1 = cv2.imread("add1.jpg", cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread("add2.jpg", cv2.IMREAD_GRAYSCALE)
if image1 is None or image2 is None: raise Exception("영상 파일 읽기 오류 발생")

title = 'dst'

alpha, beta = 0.5, 0.5
image3 = cv2.addWeighted(image1, alpha, image2, beta, 0)

w, h = image1.shape[:2]
hor = np.zeros((w, h*2), np.uint8)
dst = np.zeros((w, h*3), np.uint8)

hor = cv2.hconcat([image1, image3])
dst = cv2.hconcat([hor, image2])

cv2.imshow(title, dst)

cv2.createTrackbar('image1', title, 50, 100, onChange_alpha)
cv2.createTrackbar('image2', title, 50, 100, onChange_beta)

cv2.waitKey(0)
