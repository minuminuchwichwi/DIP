# 카메라에서 한 프레임을 가져와 원근 투영은 성공했으나
# 비디오 파일 원근 투영은 실패..
import numpy as np, cv2
from Common.utils import contain_pts

def draw_rect(capture):
    rois = [(p - small, small * 2) for p in pts1]
    for (x, y), (w, h) in np.int32(rois):
        roi = capture[y:y + h, x:x + w]
        val = np.full(roi.shape, 80, np.uint8)
        cv2.add(roi, val, roi)
        cv2.rectangle(capture, (x, y, w, h), (0, 255, 0), 1)
    cv2.polylines(capture, [pts1.astype(int)], True, (0, 255, 0), 1)
    cv2.imshow("select rect", capture)


def warp(capture):
    perspect_mat = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(capture, perspect_mat, (350, 400))
    cv2.imshow("perspective transform", dst)


def onMouse(event, x, y, flags, param):
    global check
    if event == cv2.EVENT_LBUTTONDOWN:
        for i, p in enumerate(pts1):
            p1, p2 = p - small, p + small
            if contain_pts((x, y), p1, p2): check = i

    if event == cv2.EVENT_LBUTTONUP: check = -1

    if check >= 0:
        pts1[check] = (x, y)
        draw_rect(np.copy(frame))
        warp(np.copy(frame))

capture = cv2.VideoCapture(0)
if capture.isOpened() == False: raise Exception("카메라가 연결되지 않음")

capture.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
capture.set(cv2.CAP_PROP_AUTOFOCUS, 0)
capture.set(cv2.CAP_PROP_BRIGHTNESS, 100)

ret, frame = capture.read()
if not ret: raise Exception("카메라 영상 읽기 에러")

small = np.array((12, 12))
check = -1
pts1 = np.float32([(100, 100), (300, 100), (300, 300), (100, 300)])
pts2 = np.float32([(0, 0), (400, 0), (400, 350), (0, 350)])
draw_rect(np.copy(frame))
cv2.setMouseCallback("select rect", onMouse, 0)
cv2.waitKey(0)
capture.release()