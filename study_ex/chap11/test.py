import numpy as np, cv2, pickle

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./recognizers/face-trainner.yml")          # 학습 결과 파일

labels = {"person_name": 1}

with open("pickles/face-labels.pickle", 'rb') as f:
   og_labels = pickle.load(f)
   labels = {v:k for k,v in og_labels.items()}            # 번호 : 이름
cap = cv2.VideoCapture(0)
blue, white = (255, 0, 0), (255,255,255)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 400)      # 카메라 프레임 너비
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)     # 카메라 프레임 높이

while(True):
    ret, frame = cap.read()
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        id_, conf = recognizer.predict(roi_gray)
        if conf>=4 and conf <= 85:
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = "%-10s: %5.2f" %(labels[id_], conf)
            cv2.putText(frame, name, (x,y), font, 0.6, white, 2, cv2.LINE_AA)

        cv2.imwrite("7.png", roi_color)
        cv2.rectangle(frame, (x, y, w, h) , blue, 2)

    if cv2.waitKey(20) & 0xFF == ord('q'): break
    cv2.imshow('frame',frame)

cap.release()
cv2.destroyAllWindows()

