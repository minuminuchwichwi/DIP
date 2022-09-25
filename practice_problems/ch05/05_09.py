import numpy as np, cv2

np.random.seed(10)

a = np.random.randint(1, 10, (3, 6))
print(a)
a = np.full((3, 6), 5, np.uint8)
print(a)

b = cv2.reduce(a, dim = 1, rtype = cv2.REDUCE_AVG)
print("b = \n", b)

c = cv2.reduce(a, dim = 0, rtype = cv2.REDUCE_AVG)
print("c = \n ", c)