import numpy as np, cv2

no = 0
while True:
    # 위쪽 방향키를 눌렀을 때 사진 번호를 -1, 아래 방향키를 눌렀을 때 사진 번호 +1
    # 하여 영상 전환, Esc키를 눌렀을 때는 창을 모두 닫고 종료
    key = cv2.waitKeyEx()
    if key == 0x260000:
        no = no - 1
    elif key == 0x280000:
        no = no + 1
    elif key == 27:
        break;

    fname = "C:/images/test_car/{0:02d}.jpg".format(no)
    image = cv2.imread(fname, cv2.IMREAD_COLOR)
    if image is None:
        print(str(no) + "번 영상 파일이 없습니다.")
        continue

    mask = np.ones((5, 17), np.uint8)  # 닫힘 연산 마스크
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 명암도 영상 변환
    gray = cv2.blur(gray, (5, 5))  # 블러링
    gray = cv2.Sobel(gray, cv2.CV_8U, 1, 0, 5)  # 소벨 에지 검출
    # gray = cv2.Canny(gray, 100,200)  # 소벨 에지 검출

    # 이진화 및 닫힘 연산 수행
    _, th_img = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    morph = cv2.morphologyEx(th_img, cv2.MORPH_CLOSE, mask, iterations=3)

    cv2.imshow("image", image)
    cv2.imshow("binary image", th_img)
    cv2.imshow("opening", morph)
    cv2.waitKey()
