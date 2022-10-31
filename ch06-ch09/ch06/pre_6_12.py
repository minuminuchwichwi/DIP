# 이미지에서 검은색을 찾아 horizontal, vertical projection 하여 검은 선으로 만들어진 histogram
import cv2
import numpy as np

show_im = cv2.imread("C:/images/result.png", cv2.IMREAD_GRAYSCALE)
im = cv2.imread("C:/images/result.png", cv2.IMREAD_GRAYSCALE)
# 검은색 값 찾기 위해 인버팅
im = 255 - im
proj = np.sum(im,1)
# reduce()이용 horizontal, vertical projection
horProj = cv2.reduce(im, 1, cv2.REDUCE_SUM, dtype=cv2.CV_32S)
verProj = cv2.reduce(im, 0, cv2.REDUCE_SUM, dtype=cv2.CV_32S)

m = np.max(proj)
w = im.shape[1]
# vertical projection 검은색 선
result_v = np.zeros((im.shape[0],im.shape[1]), np.uint8) + 255
for col in range(im.shape[1]):
   cv2.line(result_v, (col, 0), (col, int(verProj[0][col]*w/m)), (0,0,0), 2)

m = np.max(proj)
w = im.shape[1]
# horizontal projection 검은색 선
result_h = np.zeros((im.shape[0],im.shape[1]), np.uint8) + 255
for row in range(im.shape[0]):
   cv2.line(result_h, (0,row), (int(horProj[row]*w/m),row), (0,0,0), 2)

cv2.imshow("image",show_im)   # 원본
cv2.imshow("result_h", result_h) # horizontal projection histogram
cv2.imshow("result_v", cv2.flip(result_v,0)) # vertical projection histogram
cv2.waitKey(0)
