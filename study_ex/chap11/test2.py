import cv2, numpy as np, os, pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "images")

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()       # opencv-contrib

current_id , label_ids = 0, {}
y_labels, x_train  = [], []

for root, dirs, files in os.walk(image_dir):
	for file in files:
		if file.endswith("png") or file.endswith("jpg"):
			path = os.path.join(root, file)
			label = os.path.basename(root).replace(" ", "-").lower()

			if not label in label_ids:
				label_ids[label] = current_id              # 사전 자료형
				current_id += 1

			pil_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
			image_array = cv2.resize(pil_image, (550,550))
			faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

			for (x,y,w,h) in faces:
				roi = image_array[y:y+h, x:x+w]
				x_train.append(roi)
				y_labels.append(label_ids[label])

print('y_labels:', y_labels)
print('label_ids:', label_ids)

with open("pickles/face-labels.pickle", 'wb') as f:
	pickle.dump(label_ids, f)

recognizer.train(x_train, np.array(y_labels))
recognizer.save("recognizers/face-trainner.yml")