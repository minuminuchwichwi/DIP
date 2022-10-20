import numpy as np,  cv2
from Common.interpolation import bilinear_value
from Common.utils import contain

def rotate(img, degree):
    b, g, r = cv2.split(img)
    dst_b, dst_g, dst_r = np.zeros(b.shape[:2], b.dtype), np.zeros(g.shape[:2], g.dtype), np.zeros(r.shape[:2], r.dtype)
    radian = (degree/180) * np.pi
    sin, cos = np.sin(radian), np.cos(radian)

    for i in range(b.shape[0]):
        for j in range(b.shape[1]):
            y = -j * sin + i * cos
            x =  j * cos + i * sin
            if contain((y, x), b.shape):
                dst_b[i, j] = bilinear_value(b, [x, y])
    for i in range(g.shape[0]):
        for j in range(g.shape[1]):
            y = -j * sin + i * cos
            x =  j * cos + i * sin
            if contain((y, x), g.shape):
                dst_g[i, j] = bilinear_value(g, [x, y])
    for i in range(r.shape[0]):
        for j in range(r.shape[1]):
            y = -j * sin + i * cos
            x =  j * cos + i * sin
            if contain((y, x), r.shape):
                dst_r[i, j] = bilinear_value(r, [x, y])
    dst = cv2.merge([dst_b, dst_g, dst_r])
    return dst

def rotate_pt(img, degree, pt):
    b, g, r = cv2.split(img)
    dst_b, dst_g, dst_r = np.zeros(b.shape[:2], b.dtype), np.zeros(g.shape[:2], g.dtype), np.zeros(r.shape[:2], r.dtype)
    radian = (degree/180) * np.pi
    sin, cos = np.sin(radian), np.cos(radian)

    for i in range(b.shape[0]):
        for j in range(b.shape[1]):
            jj, ii = np.subtract((j, i), pt)
            y = -jj * sin + ii * cos
            x =  jj * cos + ii * sin
            x, y = np.add((x, y), pt)
            if contain((y, x), b.shape):
                dst_b[i, j] = bilinear_value(b, [x, y])
    for i in range(g.shape[0]):
        for j in range(g.shape[1]):
            jj, ii = np.subtract((j, i), pt)
            y = -jj * sin + ii * cos
            x =  jj * cos + ii * sin
            x, y = np.add((x, y), pt)
            if contain((y, x), g.shape):
                dst_g[i, j] = bilinear_value(g, [x, y])
    for i in range(r.shape[0]):
        for j in range(r.shape[1]):
            jj, ii = np.subtract((j, i), pt)
            y = -jj * sin + ii * cos
            x =  jj * cos + ii * sin
            x, y = np.add((x, y), pt)
            if contain((y, x), r.shape):
                dst_r[i, j] = bilinear_value(r, [x, y])
    dst = cv2.merge([dst_b, dst_g, dst_r])
    return dst

image = cv2.imread('images/rotate.jpg', cv2.IMREAD_COLOR)
if image is None: raise Exception("영상 파일을 읽기 에러")

center = np.divmod(image.shape[::-1], 2)[0]

dst1 = rotate(image, 20)
dst2 = rotate_pt(image, 20, (center[1], center[2]))

cv2.imshow("image", image)
cv2.imshow("dst1-rotated on org", dst1)
cv2.imshow("dst2-rotated on center", dst2)
cv2.waitKey(0)