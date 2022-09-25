import numpy as np, cv2

logo = cv2.imread("images/logo.jpg", cv2.IMREAD_COLOR)
if logo is None: raise Exception("영상 읽기 오류")

blue, green, red = cv2.split(logo)

img_zero = np.zeros_like(blue)
blue_img = cv2.merge([blue, img_zero, img_zero])
green_img = cv2.merge([img_zero, green, img_zero])
red_img = cv2.merge([img_zero, img_zero, red])

cv2.imshow('logo', logo)
cv2.imshow('blue_img', blue_img)
cv2.imshow('green_img', green_img)
cv2.imshow('red_img', red_img)
cv2.waitKey(0)