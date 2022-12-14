import numpy as np, cv2, pickle, gzip, os
from urllib.request import urlretrieve
import matplotlib.pyplot as plt

def place_middle(number, new_size):
    h, w = number.shape[:2]
    square = np.full(number.shape[:2], 255, np.float32)  # 실수 자료형

    dx, dy = np.subtract(square.shape[:2], (w,h))//2
    square[dy:dy + h, dx:dx + w] = number

    alpha = cv2.resize(square, new_size).flatten()
    return alpha  # 크기변경 및 벡터변환 후 반환

#에러