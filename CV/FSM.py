import numpy as np
import cv2


def threshold(difference):
    out = np.full_like(difference, 128)  # start and assume there are no events
    out[difference < -10] = 0  # if event is negative enough, OFF event
    out[difference > 10] = 255  # if event is positive enough, ON event
    return out


def accumulate(frame, width):
    left = frame[:, :int(width/3)]
    right = frame[:, int(width * 2/3):]
    acc = (left == 255).sum() + (right == 255).sum()
    return acc


cap = cv2.VideoCapture(1, cv2.CAP_MSMF)
face = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

ret, fc = cap.read()
WIDTH = cap.get(3)
HEIGHT = cap.get(4)
fc = cv2.cvtColor(fc, cv2.COLOR_BGR2GRAY)
fp = np.array(fc, dtype=int)
while True:
    ret, fc = cap.read()

    if ret:
        fc = cv2.cvtColor(fc, cv2.COLOR_BGR2GRAY)  # convert to grayscale
        fc = cv2.GaussianBlur(fc, (9, 9), 20)  # blur bc my webcam is *fart noises*
        fc = np.array(fc, dtype=int)
        diff = fc - fp
        ft = np.array(threshold(diff), dtype=np.uint8)  # subtract current and previous frame, then threshold
        cv2.rectangle(ft, (int(WIDTH / 3), 0), (int(2*WIDTH / 3), int(HEIGHT)), (255, 0, 0), 2)
        cv2.imshow('output', ft)
        acc = accumulate(ft, int(WIDTH))
        if acc > 5000:
            print(acc, "motion")
        fp = fc


      # after showing temporal difference, assign current frame to previous frame
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

