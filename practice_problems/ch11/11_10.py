from haar_utils import *                   # 검출기 적재 및 전처리 함수
from haar_histogram import *                  # 히스토그램 비교 관련 함수
import matplotlib.pyplot as plt

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")  # 정면 검출기
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")  # 눈 검출기

no = 0
max = 60
lip_face = [0]*max
hair = [0]*max
mean_sim1 = [0.0]*max
mean_sim2 = [0.0]*max

while no < max :
    image, gray = preprocessing(no)  # 전처리
    if image is None: raise Exception("영상 파일을 읽기 에러")

    faces = face_cascade.detectMultiScale(gray, 1.1, 2, 0, (100, 100))  # 얼굴 검출
    if faces.any():
        x, y, w, h = faces[0].tolist()
        face_image = image[y:y + h, x:x + w]  # 얼굴 영역 영상 가져오기
        eyes = eye_cascade.detectMultiScale(face_image, 1.15, 7, 0, (25, 20))  # 눈 검출

        if len(eyes) == 2:
            face_center = (x + w // 2, y + h // 2)
            eye_centers = [(x + ex + ew // 2, y + ey + eh // 2) for ex, ey, ew, eh in eyes]
            corr_image, corr_center = correct_image(image, face_center, eye_centers)  # 기울기 보정

            rois = detect_object(face_center, faces[0])  # 머리 및 입술영역 검출
            masks = make_masks(rois, corr_image.shape[:2])  # 4개 마스크 생성
            sim = calc_histo(corr_image, rois, masks)  # 4개 히스토그램 생성

            lip_face[no] = round(sim[0], 2)
            hair[no] = round(sim[1], 2)

        else:
            print("눈 미검출")
    else:
        print("얼굴 미검출")
    no += 1

for i in range(30):
    mean_sim1[i] = np.mean(lip_face[:30])
    mean_sim1[30 + i] = np.mean(lip_face[30:60])
    mean_sim2[i] = np.mean(hair[:30])
    mean_sim2[30 + i] = np.mean(hair[30:60])

#legend 설정때문에 2번 쓸 수 밖에 없음..
plt.scatter(0, lip_face[0], c='red', label='lip-face')
plt.scatter(0, hair[0], c='blue', marker='v', label='hair')
plt.plot(mean_sim1, 'r-', label='mean sim 1')
plt.plot(mean_sim2, 'b-', label='mean sim 2')
i = 1
for i in range(max):
    plt.scatter(i, lip_face[i], c='red')
    plt.scatter(i, hair[i], c='blue', marker='v')
    plt.plot(mean_sim1, 'r-')
    plt.plot(mean_sim2, 'b-')
plt.legend(loc='upper left')
plt.show()