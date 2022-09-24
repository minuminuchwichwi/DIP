import numpy as np, cv2

a = np.array([[9,3,4,5,6]])

b = cv2.sort(a, cv2.SORT_EVERY_COLUMN)

print(a.shape)
print(b)