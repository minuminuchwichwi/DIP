from Common.histogram import draw_histo_hue
from coin_preprocess import *
from coin_utils import *

def onMouse(event, x, y, flags, param):
    global pre_img, hist_roi
    if event == cv2.EVENT_LBUTTONDOWN:
        for i, ((cx, cy), radius) in enumerate(circles):
            dx, dy = (cx - x), (cy - y)
            dist = np.sqrt(dx**2 + dy**2)               #빈칸 부분

            if dist < radius:
                hist_img = draw_histo_hue(coin_hists[i], (80, 128, 3))
                h, w = hist_img.shape[:2]
                hist_roi = [x, y, w, h]
                #좌표의 위치에 따른 히스토그램 위치 수정(히스토그램의 좌표가 이미지 밖이면 에러가 발생)
                if y > int(image.shape[1] / 2) & x < int(image.shape[0] / 2):       # 3사분면
                    pre_img = image[y - h:y, x:x + w].copy()
                    image[y - h:y, x:x + w] = hist_img
                elif y > int(image.shape[1] / 2) & x > int(image.shape[0] / 2):     # 2사분면
                    pre_img = image[y - h:y, x - w:x].copy()
                    image[y - h:y, x - w:x] = hist_img
                elif y < int(image.shape[1] / 2) & x > int(image.shape[0] / 2):     # 1사분면
                    pre_img = image[y:y + h, x - w:x].copy()
                    image[y:y + h, x - w:x] = hist_img
                else:                                                           # 4사분면
                    pre_img = image[y:y + h, x:x + w].copy()
                    image[y:y+h, x:x+w] = hist_img
                cv2.imshow("image", image)

    if event == cv2.EVENT_LBUTTONUP:
        x, y, w, h = hist_roi
        if y > (image.shape[1] // 2) & x < (image.shape[0] // 2):
            image[y - h:y, x:x + w] = pre_img
        elif y > (image.shape[1] // 2) & x > (image.shape[0] // 2):
            image[y - h:y, x - w:x] = pre_img
        elif y < (image.shape[1] // 2) & x > (image.shape[0] // 2):
            image[y:y + h, x - w:x] = pre_img
        else:
            image[y:y + h, x:x + w] = pre_img
        cv2.imshow("image", image)

coin_no = 87
image, th_img = preprocessing(coin_no)
circles = find_coins(th_img)

coin_imgs = make_coin_img(image, circles)                   #빈칸 부분
coin_hists = [calc_histo_hue(coin) for coin in coin_imgs]   #빈칸 부분

for center, radius in circles:
    cv2.circle(image, center, radius, (0, 255, 0), 2)

cv2.imshow("image", image)
cv2.setMouseCallback("image", onMouse)
cv2.waitKey(0)