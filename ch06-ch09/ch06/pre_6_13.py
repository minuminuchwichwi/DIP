import numpy as np, cv2

BGR_img = cv2.imread("C:/images/color_space.jpg", cv2.IMREAD_COLOR)
if BGR_img is None: raise Exception("영상파일 읽기 오류")
blue, green, red = cv2.split(BGR_img)

Y_img_a = cv2.addWeighted(red, 0.299, green, 0.587, 0)
Y_img = cv2.addWeighted(Y_img_a, 1, blue, 0.114, 0)
Cb_img = cv2.addWeighted(red,0.564, Y_img, -0.564, 128)
Cr_img = cv2.addWeighted(blue, 0.713, Y_img, -0.713, 126)

YCC_img = cv2.merge([Y_img, Cb_img, Cr_img])

OpenCV_YCC = cv2.cvtColor(BGR_img, cv2.COLOR_BGR2YCrCb)

cv2.imshow("BGR_img", BGR_img)
cv2.imshow("YCC_img", YCC_img)
cv2.imshow("OpenCV_YCC", OpenCV_YCC)

cv2.waitKey(0)
