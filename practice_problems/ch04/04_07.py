#예시 코드 오류 수정하기
import numpy as np, cv2

image = np.zeros((500, 500, 3), np.uint8)   #윈도우 크기 수정
image[:] = (255, 255, 255)

pt1, pt2 = (50, 130), (200, 300)

cv2.line(image, pt1, (100, 200), (255, 0, 0))   #색 추가
cv2.line(image, pt2, (100, 100), (100, 100, 100))  #색 추가, 좌표값 변경
cv2.rectangle(image, pt1, (pt2[0]+10, pt2[1]+10), (255, 0, 255))    #출력이 된걸 확인하기 위해 좌표값 조금 변경
cv2.rectangle(image, pt1, pt2, (0, 0, 255))

title = "Line & Rectangle"
cv2.namedWindow(title)
cv2.imshow(title, image)
cv2.waitKey(0)
cv2.destroyAllWindows()