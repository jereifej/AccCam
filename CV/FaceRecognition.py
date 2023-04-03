import cv2
import numpy as np
import time

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
# Turn off auto exposure
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
cap.set(cv2.CAP_PROP_FPS, 30)
face = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

avgFPS = time.time()
count = 0
acc = 0
while True:
    ret, frame = cap.read()
    instFPS = time.time()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=4)
        # numpy.append(faces, face.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    #print(isinstance(faces, tuple))
    #print(isinstance(faces, np.ndarray))
    cv2.imshow('output', frame)
    count += 1
    diff = time.time() - instFPS
    acc += diff

   # print("FPS: ", 1.0 / diff)  # FPS = 1 / time to process loop

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
print("Avg FPS: ", count / acc)

cap.release()
cv2.destroyAllWindows()