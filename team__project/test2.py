import numpy as np, cv2

def draw_rect(img):
    rois = [(p - small, small * 2) for p in pts1]
    for (x, y), (w, h) in np.int32(rois):
        roi = img[y:y + h, x:x + w]  # 좌표 사각형 범위 가져오기
        val = np.full(roi.shape, 80,
                      np.uint8)  # 컬러(3차원) 행렬 생성      cv2.add(roi, val, roi)                               # 관심영역 밝기 증가
        cv2.add(roi, val, roi)
        cv2.rectangle(img, (x, y, w, h), (255, 0, 0), 1)
    cv2.polylines(img, [pts1.astype(int)], True, (255, 0, 0), 1)  # pts는 numpy 배열
    if cnt == 0:
        cv2.imshow("img", img)
    else: cv2.imshow("dst",img)

def contain_pts(p, p1, p2):
    return p1[0] <= p[0] < p2[0] and p1[1] <= p[1] < p2[1]

def warp(img):
    perspect_mat = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(img, perspect_mat, (350, 400), cv2.INTER_CUBIC)
    cv2.imshow("perspective transform", dst)
    return dst

def onMouse(event, x, y, flags, param):
    global check, cnt
    if event == cv2.EVENT_LBUTTONDOWN:
        for i, p in enumerate(pts1):
            p1, p2 = p - small, p + small  # p점에서 우상단, 좌하단 좌표생성
            if contain_pts((x, y), p1, p2): check = i

    if event == cv2.EVENT_LBUTTONUP: check = -1  # 좌표 번호 초기화

    if event == cv2.EVENT_RBUTTONDOWN:
        no = int(input("몇번으로 저장하시겠습니까?"))
        cv2.imwrite("images/cat%d.jpg" % no, warp(np.copy(img)))
        cnt = 1
        draw_rect(detectCatFace(no))

    if check >= 0:  # 좌표 사각형 선택 시
        pts1[check] = (x, y)
        draw_rect(np.copy(img))
        warp(np.copy(img))



face_cascade = cv2.CascadeClassifier("haarcascade_frontalcatface.xml")
cascade = 'C:/PyCharm Community Edition 2022.2.1/Teamp/haarcascade_frontalcatface.xml'


def detectCatFace(no):
    # 이미지 불러오기
    img = cv2.imread('images/cat%d.jpg' % no, cv2.IMREAD_COLOR)
    if img is None: raise Exception("영상파일 읽기 에러")
    # 회색으로 변경
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 얼굴 검출0
    faces = face_cascade.detectMultiScale(grayImg, 1.1, 2, 0, (100, 100))
    # 검출된 얼굴 개수 출력
    print("The number of images found is : " + str(len(faces)))
    # 검출된 얼굴 위치에 녹색 상자그리기
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # 검출된 얼굴(녹색 상자가 그려진) 이미지 데이터를 리턴
    return img


small = np.array((12, 12))  # 좌표 사각형 크기
check = -1  # 선택 좌표 사각형 번호 초기화
pts1 = np.float32([(100, 100), (300, 100), (300, 300), (100, 300)])
pts2 = np.float32([(0, 0), (400, 0), (400, 350), (0, 350)])  # 목적 영상 4개 좌표                         # 목적 영상 4개 좌표
'''
scale factor는 1에 가까울수록 인식율이 좋지만 
그만큼 느려짐(그만큼 많은  
'''
SF = 1.00
'''
내부 알고리즘에서 최소한 검출된 횟수이상 되야 인식
0이면 무수한 오 검출이 되고
1이면 한번 이상 검출된 곳만 인식된다.
값이 높아질수록 오인식율은 줄지만 그만큼 
인식율이 떨어진다.
'''
N = 2
'''
검출하려는 이미지의 최소 사이즈
이 값보다 작은 이미지는 무시 
'''
MS = (50, 50)

# 고양이 얼굴 인식용 haarcascade 파일 위치

# 고양이 얼굴 인식 cascade 생성

# 얼굴 검출 함수


# 얼굴 검출 함수 호출
cnt = 0
no = int(input("고양이 영상 번호 (0~20): "))
img = detectCatFace(no)
if img is None: raise Exception("영상파일 읽기 에러")
# 검출된 이미지가 있다면 화면에 표시
if len(img) != 0:
    cv2.imshow('img', img)
draw_rect(np.copy(img))
cv2.setMouseCallback("img", onMouse, 0)
# 아무키나 눌릴때까지 대기
cv2.waitKey(0)

cv2.destroyWindow('img')