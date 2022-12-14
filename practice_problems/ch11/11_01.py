#from paint_init import *
#-------
DRAW_RECTANGLE = 0  #사각형 그리기
DRAW_CIRCLE    = 1  # 원 그리기
DRAW_ECLIPSE   = 2  # 타원 그리기
DRAW_LINE      = 3  # 직선 그리기
DRAW_BRUSH     = 4  # 브러시 그리기
ERASE          = 5  # 지우개
OPEN           = 6  # 열기 명령
SAVE           = 7  # 저장 명령
PLUS           = 8  # 밝게 하기 명령
MINUS          = 9  # 어둡게 하기 명령
CREAR          = 10 # 지우기	명령
COLOR          = 11 # 색상 아이콘
HISTOGRAM      = 12 # 히스토그램
MOSAIC         = 13 # 모자이크
PALETTE        = 14 # 색상팔레트
HUE_IDX        = 15 # 색상인덱스

# 전역 변수
mouse_mode, draw_mode = 0, 0                # 그리기 모드, 마우스 상태
pt1, pt2, Color = (0, 0), (0, 0), (0, 0, 0) # 시작 좌표, 종료 좌표
thickness = 3                               # 선 두께

#-------
#from paint_utils import *
#-------
import numpy as np, cv2

def place_icons(image, size):
    icon_name = ["rect" , "circle", "eclipe", "line",   # 아이콘 파일 이름
                 "brush", "eraser", "open"  , "save",
                 "plus" , "minus" , "clear" , "color",
                 "histogram", "mosaic"]

    icons = [(i%2, i//2, 1, 1) for i in range(len(icon_name))]
    icons = np.multiply(icons, size*2)                  # icons 모든 원소에 size 곱합

    for roi, name in zip(icons, icon_name):
        icon = cv2.imread('C:/images/icon/%s.jpg' %name , cv2.IMREAD_COLOR)
        if icon is None: continue
        x, y, w, h = roi
        image[y:y+h, x:x+w] = cv2.resize(icon, size)
    return list(icons)                   # 팔레트 생성

def create_hueIndex(image, roi):
    x, y, w, h =  roi                         # 관심영역 너비, 높이
    index = [[(j, 1, 1) for j in range(w)] for i in range(h)]      # 가로로 만들기
    ratios = (180 / w, 255, 255)
    hueIndex = np.multiply(index, ratios).astype('uint8')  # HSV 화소값 행렬

    image[y:y+h, x:x+w] = cv2.cvtColor(hueIndex, cv2.COLOR_HSV2BGR)

def create_colorPlatte(image, idx, roi):
    x, y, w, h = roi
    hue = idx-x
    palatte = [[(hue, j, h-i-1) for j in range(w)] for i in range(h)]

    ratios = (180/w, 255/w, 255/h )
    palatte = np.multiply(palatte, ratios).astype('uint8')

    image[y:y+h, x:x+w] = cv2.cvtColor(palatte, cv2.COLOR_HSV2BGR)

def create_colorPlatte1(image, hueidx, roi):
    x, y, w, h = roi
    ratio1 = 180 / h                     # 팔레트 높이에 따른 색상 비율
    ratio2 = 255 / w                      # 팔레트 너비에 따른 채도 비율
    ratio3 = 255 / h                     # 팔레트 높이에 따른 명도 비율
    hue = ((hueidx - x) * ratio1)           # 색상팔레트 기본 색상

    palatte = [[(hue, j, (h-i-1)) for j in range(w)] for i in range(h)]
    palatte = np.multiply(palatte, (1, ratio2, ratio3)).astype('uint8')

    image[y:y+h, x:x+w] = cv2.cvtColor(palatte, cv2.COLOR_HSV2BGR)

def create_colorPlatte2(image, hueidx, roi):
    x, y, w, h = roi
    ratio1 = 180 / w  # 팔레트 높이에 따른 색상 비율
    ratio2 = 256 / w  # 팔레트 너비에 따른 채도 비율
    ratio3 = 256 / h  # 팔레트 높이에 따른 명도 비율

    hue = round((hueidx - x) * ratio1)  # 색상 팔레트 기본 색상
    palatte = [[(hue, j * ratio2, (h - i - 1) * ratio3)  # (색상, 채도, 명도) 화소 구성
                for j in range(w)] for i in range(h)]  # roi 크기 순회
    palatte = np.array(palatte, np.uint8)

    image[y:y + h, x:x + w] = cv2.cvtColor(palatte, cv2.COLOR_HSV2BGR)

    return hue

#-------

def getAffineMat(center, degree, fx = 1, fy = 1, translate = (0,0)):
    cen_trans = np.eye(3, dtype=np.float32)
    org_trans = np.eye(3, dtype=np.float32)
    scale_mat = np.eye(3, dtype=np.float32)         # 크기 변경 행렬
    trans_mat = np.eye(3, dtype=np.float32)         # 평행 이동 행렬
    rot_mat   = np.eye(3, dtype=np.float32)         # 회전 변환 행렬

    radian = (degree/180.0) * np.pi                 # 회전 각도 - 라디언  계산
    rot_mat[0] = [ np.cos(radian), np.sin(radian), 0]
    rot_mat[1] = [-np.sin(radian), np.cos(radian), 0]

    cen_trans[:2, 2] = center                       # 중심 좌표를 기준으로 회전
    org_trans[:2, 2] = np.multiply(center[0], -1)   # 원점으로 이동
    scale_mat[0, 0], scale_mat[1, 1] = fx, fy       # 크기 변경 행렬의 원소 지정

    ret_mat = cen_trans.dot(rot_mat.dot(trans_mat.dot(scale_mat.dot(org_trans))))
    return np.delete(ret_mat, 2, axis=0)            # 행 제거 ret_mat[0:2,:]

def onMouse(event, x, y, flags, param):
    global pt1, pt2, mouse_mode, draw_mode

    if event == cv2.EVENT_LBUTTONUP:  # 왼쪽 버튼 떼기
        for i, (x0, y0, w, h) in enumerate(icons):  # 메뉴아이콘 사각형 조회
            if x0 <= x < x0 + w and y0 <= y < y0 + h:  # 메뉴 클릭 여부 검사
                if i < 6:  # 그리기 명령이면
                    mouse_mode = 0  # 마우스 상태 초기화
                    draw_mode = i  # 그리기 모드
                else:
                    command(i)  # 일반 명령이면
                return

        pt2 = (x, y)  # 종료좌표 저장
        mouse_mode = 1  # 버튼 떼기 상태 지정

    elif event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 버튼 누르기
        pt1 = (x, y)  # 시작좌표 저장
        mouse_mode = 2

    if mouse_mode >= 2:  # 왼쪽 버튼 누르기 또는 드래그
        mouse_mode = 0 if x < 125 else 3  # 메뉴 영역 확인- 마우스 상태 지정
        pt2 = (x, y)


def draw(image, color=(200, 200, 200)):
    global draw_mode, thickness, pt1, pt2

    if draw_mode == DRAW_RECTANGLE:  # 사각형 그리기
        cv2.rectangle(image, pt1, pt2, color, thickness)

    elif draw_mode == DRAW_LINE:  # 직선 그리기
        cv2.line(image, pt1, pt2, color, thickness)

    elif draw_mode == DRAW_BRUSH:  # 브러시 그리기
        cv2.line(image, pt1, pt2, color, thickness * 3)
        pt1 = pt2  # 종료 좌표를 시작 좌표로 지정

    elif draw_mode == ERASE:  # 지우개
        cv2.line(image, pt1, pt2, (255, 255, 255), thickness * 5)
        pt1 = pt2

    elif draw_mode == DRAW_CIRCLE:  # 원 그리기
        d = np.subtract(pt1, pt2)  # 두 좌표 차분
        radius = int(np.sqrt(d[0] ** 2 + d[1] ** 2))
        cv2.circle(image, pt1, radius, color, thickness)

    elif draw_mode == DRAW_ECLIPSE:  # 타원 그리기
        center = np.abs(np.add(pt1, pt2)) // 2  # 두 좌표의 중심점 구하기
        size = np.abs(np.subtract(pt1, pt2)) // 2  # 두 좌표의 크기의 절반
        cv2.ellipse(image, tuple(center), tuple(size), 0, 0, 360, color, thickness)

    cv2.imshow("PaintCV", image)


def command(mode):
    global icons, image, canvas, Color, hue, mouse_mode
    if mode == PALETTE:  # 색상팔레트 영역 클릭 시
        pixel = image[pt2[::-1]]
        x, y, w, h = icons[COLOR]
        image[y:y + h - 1, x:x + w - 1] = pixel
        Color = tuple(map(int, pixel))

    elif mode == HUE_IDX:  # 색상인텍스 클릭 시
        create_colorPlatte(image, pt2[0], icons[PALETTE])  # 팔레트 새로 그리기

    elif mode == OPEN:  # 영상 파일 열기
        tmp = cv2.imread("C:/images/my_picture.jpg", cv2.IMREAD_COLOR)
        cv2.resize(tmp, canvas.shape[1::-1], canvas)

    elif mode == SAVE:  # 캔버스 영역 저장
        cv2.imwrite("C:/images/my_save.jpg", canvas)

    elif mode == PLUS:  # 캔버스 영상 밝게 변경
        val = np.full(canvas.shape, 10, np.uint8)  # 증가 화소값 행렬 생성
        cv2.add(canvas, val, canvas)

    elif mode == MINUS:  # 캔버스 영상 어둡게 변경
        val = np.full(canvas.shape, 10, np.uint8)  # 증가 화소값 행렬 생성
        cv2.subtract(canvas, val, canvas)

    elif mode == CREAR:  # 캔버스 영역 전체 지우기
        canvas[:] = (255, 255, 255)  # 캔버스를 흰색으로
        mouse_mode = 0  # 마우스 상태 초기화


    cv2.imshow("PaintCV", image)


def onTrackbar(value):  # 트랙바 콜백 함수
    global mouse_mode, thickness
    mouse_mode = 0  # 마우스 상태 초기화
    thickness = value


image = np.full((500, 800, 3), 255, np.uint8)
icons = place_icons(image, (60, 60))  # 아이콘 배치, 아이콘 크기
x, y, w, h = icons[-1]  # 아이콘 사각형 마지막1 원소

## 팔레트 및 색상인덱스 크기 60으로 변환
icons.append((0, y + h + 2, 60, 60))  # 팔레트 사각형 추가
icons.append((0, y + h + 62, 60, 15))  # 색상인덱스 사각형 추가
create_colorPlatte(image, 0, icons[PALETTE])  # 팔레트 생성
create_hueIndex(image, icons[HUE_IDX])  # 색상인텍스 생성

cv2.imshow("PaintCV", image)
cv2.setMouseCallback("PaintCV", onMouse)  # 마우스 콜백 함수
cv2.createTrackbar("Thickness", "PaintCV", thickness, 255, onTrackbar)

canvas = image[:, w * 2:image.shape[1]]  # 메뉴를 제외한 캔버스 영역
center = np.divmod(canvas.shape[::-1], 2)[0][1:]
while True:
    if mouse_mode == 1:  # 마우스 버튼 떼기
        draw(image, Color)  # 원본에 그림
    elif mouse_mode == 3:  # 마우스 드래그
        if draw_mode == DRAW_BRUSH or draw_mode == ERASE:
            draw(image, Color)  # 원본에 그림
        else:
            draw(np.copy(image), (200, 200, 200))  # 복사본에 회색으로 그림
    if cv2.waitKey(30) == 27:  # ESC 키를 누르면 종료
        break
