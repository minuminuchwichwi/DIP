<<<<<<< HEAD
import numpy as np, cv2

#Common.filters.filter()함수
def filter(image, mask):

    rows, cols = image.shape[:2]
    dst = np.zeros((rows, cols), np.float32)
    xcenter, ycenter = mask.shape[1] // 2, mask.shape[0] // 2

    for i in range(ycenter, rows - ycenter):
        for j in range(xcenter, cols - xcenter):
            y1, y2 = i - ycenter, i + ycenter + 1
            x1, x2 = j - xcenter, j + xcenter + 1

            roi = image[y1:y2, x1:x2].astype("float32")
            tmp = cv2.multiply(roi, mask)
            dst[i, j] = cv2.sumElems(tmp)[0]

    return dst

#가우시안 블러링을 위해 마스크를 반환하는 함수
def getGaussianMask(ksize, sigmaX, sigmaY):
    sigma = 0.3 * ((np.array(ksize) - 1.0) * 0.5 - 1.0) + 0.8  # 표준 편차
    if sigmaX <= 0: sigmaX = sigma[0]
    if sigmaY <= 0: sigmaY = sigma[1]

    u = np.array(ksize)//2
    x = np.arange(-u[0], u[0]+1, 1)
    y = np.arange(-u[1], u[1]+1, 1)
    x, y = np.meshgrid(x, y)

    ratio = 1 / (sigmaX*sigmaY * 2 * np.pi)
    v1 = x ** 2 / (2 * sigmaX ** 2)
    v2 = y ** 2 / (2 * sigmaY ** 2 )
    mask = ratio * np.exp(-(v1+v2))
    return mask / np.sum(mask)

image = cv2.imread("images/smoothing.jpg", cv2.IMREAD_COLOR)
if image is None: raise Exception("영상파일 읽기 오류")

blue, green, red = cv2.split(image)     #조건3의 컬러영상 채널 분리

#분리한 각 채널에 각각 가우시안 블러링을 사용
size = (3, 3)
gauss_image_blue = cv2.GaussianBlur(blue, size, 0)
gauss_image_green = cv2.GaussianBlur(green, size, 0)
gauss_image_red = cv2.GaussianBlur(red, size, 0)

#조건2의 샤프닝 마스크의 크기는 3*3이기에 샤프닝 마스크 데이터 9개 생성
data = [0, -1, 0,
        -1, 5, -1,
        0, -1, 0]

#샤프닝을 위해 마스크 데이터를 3*3 마스크로 변환 후, 각 채널에 샤프닝 수행
#문제에서 말하는 filter()함수를 샤프닝에 사용
sharpening_mask = np.array(data, np.float32).reshape(3, 3)
sharp_image_blue = filter(gauss_image_blue, sharpening_mask)
sharp_image_green = filter(gauss_image_green, sharpening_mask)
sharp_image_red = filter(gauss_image_red, sharpening_mask)

sharp_image_blue = cv2.convertScaleAbs(sharp_image_blue)
sharp_image_green = cv2.convertScaleAbs(sharp_image_green)
sharp_image_red = cv2.convertScaleAbs(sharp_image_red)

#조건3에서 블러링과 샤프닝을 수행한 후, 다시 분리된 채널 합치기
merge_image = cv2.merge([sharp_image_blue, sharp_image_green, sharp_image_red])

gaussian_2d = getGaussianMask(size, 0, 0)
direct_image_blur = cv2.filter2D(image, -1, gaussian_2d)
direct_image = cv2.filter2D(direct_image_blur, -1, sharpening_mask)

#원본 이미지와 각각 2개의 수정된 컬러영상들의 차이 비교
dif_image_split = image - merge_image
dif_image_direct = image - direct_image

titles = ['image', 'merge_image', 'direct_image', 'dif_image_split', 'dif_image_direct']
for t in titles: cv2.imshow(t, eval(t))

=======
import numpy as np, cv2

#Common.filters.filter()함수
def filter(image, mask):

    rows, cols = image.shape[:2]
    dst = np.zeros((rows, cols), np.float32)
    xcenter, ycenter = mask.shape[1] // 2, mask.shape[0] // 2

    for i in range(ycenter, rows - ycenter):
        for j in range(xcenter, cols - xcenter):
            y1, y2 = i - ycenter, i + ycenter + 1
            x1, x2 = j - xcenter, j + xcenter + 1

            roi = image[y1:y2, x1:x2].astype("float32")
            tmp = cv2.multiply(roi, mask)
            dst[i, j] = cv2.sumElems(tmp)[0]

    return dst

#가우시안 블러링을 위해 마스크를 반환하는 함수
def getGaussianMask(ksize, sigmaX, sigmaY):
    sigma = 0.3 * ((np.array(ksize) - 1.0) * 0.5 - 1.0) + 0.8  # 표준 편차
    if sigmaX <= 0: sigmaX = sigma[0]
    if sigmaY <= 0: sigmaY = sigma[1]

    u = np.array(ksize)//2
    x = np.arange(-u[0], u[0]+1, 1)
    y = np.arange(-u[1], u[1]+1, 1)
    x, y = np.meshgrid(x, y)

    ratio = 1 / (sigmaX*sigmaY * 2 * np.pi)
    v1 = x ** 2 / (2 * sigmaX ** 2)
    v2 = y ** 2 / (2 * sigmaY ** 2 )
    mask = ratio * np.exp(-(v1+v2))
    return mask / np.sum(mask)

image = cv2.imread("images/smoothing.jpg", cv2.IMREAD_COLOR)
if image is None: raise Exception("영상파일 읽기 오류")

blue, green, red = cv2.split(image)     #조건3의 컬러영상 채널 분리

#분리한 각 채널에 각각 가우시안 블러링을 사용
size = (3, 3)
gauss_image_blue = cv2.GaussianBlur(blue, size, 0)
gauss_image_green = cv2.GaussianBlur(green, size, 0)
gauss_image_red = cv2.GaussianBlur(red, size, 0)

#조건2의 샤프닝 마스크의 크기는 3*3이기에 샤프닝 마스크 데이터 9개 생성
data = [0, -1, 0,
        -1, 5, -1,
        0, -1, 0]

#샤프닝을 위해 마스크 데이터를 3*3 마스크로 변환 후, 각 채널에 샤프닝 수행
#문제에서 말하는 filter()함수를 샤프닝에 사용
sharpening_mask = np.array(data, np.float32).reshape(3, 3)
sharp_image_blue = filter(gauss_image_blue, sharpening_mask)
sharp_image_green = filter(gauss_image_green, sharpening_mask)
sharp_image_red = filter(gauss_image_red, sharpening_mask)

sharp_image_blue = cv2.convertScaleAbs(sharp_image_blue)
sharp_image_green = cv2.convertScaleAbs(sharp_image_green)
sharp_image_red = cv2.convertScaleAbs(sharp_image_red)

#조건3에서 블러링과 샤프닝을 수행한 후, 다시 분리된 채널 합치기
merge_image = cv2.merge([sharp_image_blue, sharp_image_green, sharp_image_red])

gaussian_2d = getGaussianMask(size, 0, 0)
direct_image_blur = cv2.filter2D(image, -1, gaussian_2d)
direct_image = cv2.filter2D(direct_image_blur, -1, sharpening_mask)

#원본 이미지와 각각 2개의 수정된 컬러영상들의 차이 비교
dif_image_split = image - merge_image
dif_image_direct = image - direct_image

titles = ['image', 'merge_image', 'direct_image', 'dif_image_split', 'dif_image_direct']
for t in titles: cv2.imshow(t, eval(t))

>>>>>>> origin/master
cv2.waitKey(0)