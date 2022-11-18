import numpy as np, cv2

def draw_bar(img, pt, w, bars):
    pt = np.array(pt, np.int)
    for bar in bars:
        (x, y), h = pt, w*6
        cv2.rectangle(img, (x, y, w, h), (0, 0, 0), -1)
        if bar == 0:
            y = y + int(11*w/4)
            h = int(w/2)
            cv2.rectangle(img, (x, y, w, h), (255, 255, 255), -1)
        pt += (int(w*1.5), 0)

c = 200
r, sr, c2, c4 = c//2, c//4, c*2, c*4

white, black = (255, 255, 255), (0, 0, 0)
blue, red = (255,0,0), (0,0,255)
img = np.full((c4, c4, 3), white, np.uint8)

cv2.ellipse(img, (c2, c2), (r, r), 0, 180, 360, red, -1)
cv2.ellipse(img, (c2, c2), (r, r), 0, 0, 180, blue, -1)
cv2.ellipse(img, (c2+r-sr, c2), (sr, sr), 180, 0, 180, blue, -1)
cv2.ellipse(img, (c2  -sr, c2), (sr, sr),   0, 0, 180, red, -1)

left  = (c2 - c * (18+8)/24, c2 - sr)
right = (c2 + c * (18+0)/24, c2 - sr)


draw_bar(img, right, c//12, (0,0,0))
draw_bar(img, left,  c//12, (1,1,1))
angle = cv2.fastAtan2(2,3)
img = cv2.warpAffine(img, cv2.getRotationMatrix2D((c2, c2), -angle*2, 1), (c4, c4))
cv2.imshow('test', img)

## 감(5) 리(4) 정의
draw_bar(img, right, c//12, (0,1,0))
draw_bar(img, left, c//12, (1,0,1))

## 올바른 각도로 태극기 회전
angle = cv2.fastAtan2(2,3)
img = cv2.warpAffine(img, cv2.getRotationMatrix2D((c2, c2), angle, 1), (c4, c4))

roi = img[200:600, 100:700]
cv2.imshow("roi", roi)
cv2.waitKey(0)