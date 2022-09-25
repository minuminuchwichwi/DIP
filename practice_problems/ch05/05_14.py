import numpy as np, cv2

data = [3, 6, 3, -5, 6, 1, 2, -3, 5]
m1 = np.array(data, np.float32).reshape(3, 3)
m2 = np.array([2, 10, 28], np.float32)


ret, inv = cv2.invert(m1, cv2.DECOMP_LU)
if ret:
    _, dst = cv2.solve(m1, m2, cv2.DECOMP_LU)

    print("역행렬 = \n%s\n"%inv)
    print("가우시안 소거법의 역함수를 통한 연립방정식의 해 \n", dst.flatten())
else: print("역행렬이 존재하지 않습니다.")