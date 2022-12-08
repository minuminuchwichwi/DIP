from paint_init import *
from paint_utils import *

def place_icons(image, size):
    icon_name = ["rect", "circle", "eclipe", "line", "brush", "eraser",  # 아이콘 파일 이름
                 "open", "save", "plus", "minus", "clear", "color", "zoomin", "zoomout"]
    icons = [(i, i//16, 1, 1) for i in range(len(icon_name))]       #첫번째 i는 ex) i%2 x축으로 2줄, 두번째 i는 ex)i//16 16개 아이콘을 한줄에, 1, 1은 아이콘의 크기
    icons = np.multiply(icons, size*2)                  # icons 모든 원소에 size 곱합

    for roi, name in zip(icons, icon_name):
        icon = cv2.imread('images/icon/%s.jpg' % name, cv2.IMREAD_COLOR)
        if icon is None: continue
        x, y, w, h = roi
        image[y:y+h, x:x+w] = cv2.resize(icon, size)
    return list(icons)

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
        tmp = cv2.imread("images/my_picture.jpg", cv2.IMREAD_COLOR)
        cv2.resize(tmp, canvas.shape[1::-1], canvas)

    elif mode == SAVE:  # 캔버스 영역 저장
        cv2.imwrite("images/my_save.jpg", canvas)

    elif mode == PLUS:  # 캔버스 영상 밝게 변경
        val = np.full(canvas.shape, 10, np.uint8)  # 증가 화소값 행렬 생성
        cv2.add(canvas, val, canvas)

    elif mode == MINUS:  # 캔버스 영상 어둡게 변경
        val = np.full(canvas.shape, 10, np.uint8)  # 증가 화소값 행렬 생성
        cv2.subtract(canvas, val, canvas)

    elif mode == CREAR:  # 캔버스 영역 전체 지우기
        canvas[:] = (255, 255, 255)  # 캔버스를 흰색으로
        mouse_mode = 0  # 마우스 상태 초기화

    elif mode == ZOOMIN:
        scaleup = getAffineMat((0, 0), 0, 1.1, 1.1)
        canvas[:] = cv2.warpAffine(canvas, scaleup, (canvas.shape[1], 500))

    elif mode == ZOOMOUT:
        scaledown = getAffineMat((0, 0), 0, 0.9, 0.9)
        canvas[:] = cv2.warpAffine(canvas, scaledown, (canvas.shape[1], 500))

    cv2.imshow("PaintCV", image)


def onTrackbar(value):  # 트랙바 콜백 함수
    global mouse_mode, thickness
    mouse_mode = 0  # 마우스 상태 초기화
    thickness = value


image = np.full((500, 800, 3), 255, np.uint8)
icons = place_icons(image, (40, 40))  # 아이콘 배치, 아이콘 크기
x, y, w, h = icons[-1]  # 아이콘 사각형 마지막1 원소

icons.append((x + w + 2, 0, 40, 40))  # 팔레트 사각형 추가
icons.append((x + w + 42, 0, 40, 40))  # 색상인덱스 사각형 추가
create_colorPlatte(image, 0, icons[PALETTE])  # 팔레트 생성
create_hueIndex(image, icons[HUE_IDX])  # 색상인텍스 생성

cv2.imshow("PaintCV", image)
cv2.setMouseCallback("PaintCV", onMouse)  # 마우스 콜백 함수
cv2.createTrackbar("Thickness", "PaintCV", thickness, 255, onTrackbar)

canvas = image[h * 2:image.shape[0], :]  # 메뉴를 제외한 캔버스 영역
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
