import numpy as np, cv2
from Common.fft2d import FFT, IFFT, calc_spectrum
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_butterworthFilter(shape, R, n):
    u = np.array(shape)//2
    y = np.arange(-u[0], u[0], 1)
    x = np.arange(-u[1], u[1], 1)
    x, y = np.meshgrid(x, y)
    dist = np.sqrt(x** 2 + y** 2)

    filter = 1 / (1 + np.power(R / dist, 2 * n))
    return x, y, filter if len(shape) < 3 else cv2.merge([filter, filter])

# 버터워스 필터를 영상의 FFT 결과와 곱해 필터링
image = cv2.imread('images/filter.jpg', cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상 파일 읽기 에러")

mode = 3
dft, spectrum = FFT(image, mode)
x2, y2, butter_filter = get_butterworthFilter(dft.shape, 30, 10)

filtered_dft2 = dft * butter_filter
butter_img= IFFT(filtered_dft2, image.shape, mode)
spectrum2 = calc_spectrum(filtered_dft2)

if mode==3:
    butter_filter = butter_filter[:,:,0]

fig = plt.figure(figsize=(10,10))
ax2 = plt.subplot(333, projection='3d')
ax2.plot_surface(x2, y2, butter_filter,cmap='RdPu'), plt.title('butter_filter')

titles = ['input image','butter_highpassed_image','input spectrum',
          'butter_highpassed_spectrum', 'butter_filter']
images = [image, butter_img, spectrum, spectrum2, butter_filter]
plt.gray()                                          # 명암도 영상으로 표시
for i, t in enumerate(titles):
    plt.subplot(3,3,i+4), plt.imshow(images[i]), plt.title(t)
plt.tight_layout(), plt.show()