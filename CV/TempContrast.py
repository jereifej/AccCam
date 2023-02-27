import numpy as np
import scipy
import cv2
import time


def threshold(frame):
    out = np.full_like(frame, 128)  # start and assume there are no events
    out[frame < -10] = 0  # if event is negative enough, OFF event
    out[frame > 10] = 255  # if event is positive enough, ON event
    return out


cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('sample.mp4')

ret, fc = cap.read()
fc = cv2.cvtColor(fc, cv2.COLOR_BGR2GRAY)
fp = np.array(fc, dtype=int)
while 1:
    ret, fc = cap.read()
    fc = cv2.cvtColor(fc, cv2.COLOR_BGR2GRAY)  # convert to grayscale
    fc = cv2.GaussianBlur(fc, (9, 9), 20)  # blur bc my webcam is *fart noises*
    fc = np.array(fc, dtype=int)
    diff = fc - fp
    ft = np.array(threshold(diff), dtype=np.uint8)  # subtract current and previous frame, then threshold
    cv2.imshow('output', ft)
    # print(diff)
    fp = fc  # after showing temporal difference, assign current frame to previous frame
    # time.sleep(.1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
