import cv2, numpy as np

def preprocessing(no):  # 검출 전처리
    image = cv2.imread('images/face/%2d.jpg' %no, cv2.IMREAD_COLOR)
    if image is None: return None, None
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 명암도 영상 변환
    gray = cv2.equalizeHist(gray)  # 히스토그램 평활화
    return image, gray

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")  # 정면 검출기
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")

image, gray = preprocessing(57)  # 전처리
if image is None: raise Exception("영상 파일 읽기 에러")

faces = face_cascade.detectMultiScale(gray, 1.1, 2, 0, (100, 100))  # 얼굴 검출

for (x, y, w, h) in faces:
    roi = gray[y:y + h, x:x + w]

    smile_rects, rejectLevels, levelWeights = smile_cascade.detectMultiScale3(roi, 1.1, 2, outputRejectLevels=True)
    if len(levelWeights) == 0:
        cv2.rectangle(image, (x, y), (x + w, y + h), [0, 0, 255], 2)
        cv2.putText(image, "Not Smiling", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, [0, 0, 255], 3)
    else:
        if max(levelWeights) < 2:
            cv2.rectangle(image, (x, y), (x + w, y + h), [0, 0, 255], 2)
            cv2.putText(image, "Not Smiling", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, [0, 0, 255], 3)
        else:
            cv2.rectangle(image, (x, y), (x + w, y + h), [0, 255, 0], 2)
            cv2.putText(image, "Smiling", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, [0, 255, 0], 3)

cv2.imshow("image", image)
cv2.waitKey(0)
