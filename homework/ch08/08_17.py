import numpy as np, cv2

image = cv2.imread("images/translate.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상파일 읽기 에러")

h, w = image.shape
center = (w/2, h/2)

flip1 = np.array([[-1, 0, w-1], [0, 1, 0]], dtype=np.float32)
flip2 = np.array([[1, 0, 0], [0, -1, h-1]], dtype=np.float32)
flip3 = np.array([[-1, 0, w-1], [0, -1, h-1]], dtype=np.float32)

dst1 = cv2.warpAffine(image, flip1, (w, h))
dst2 = cv2.warpAffine(image, flip2, (w, h))
dst3 = cv2.warpAffine(image, flip3, (w, h))

title = ["image", "dst1", "dst2", "dst3"]
for t in title: cv2.imshow(t, eval(t))
cv2.waitKey(0);
