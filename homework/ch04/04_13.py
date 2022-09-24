import cv2

image = cv2.imread("C:/images/mine2.jpg", cv2.IMREAD_COLOR)     #C:\image\ 경로에 있는 컬러영상파일 적재

if image is None : raise Exception("영상 파일 읽기 에러")

cv2.imshow('test', image)   #불러온 컬러영상파일 출력

cv2.imwrite("C:/images/test.jpg", image, (cv2.IMWRITE_JPEG_QUALITY, 100))   #jpg는 100일때 가장 좋은 화질
cv2.imwrite("C:/images/tes.png", image, (cv2.IMWRITE_PNG_COMPRESSION, 9))   #png는 9가 가장 좋은 화질

cv2.waitKey(0)
cv2.destroyAllWindows()