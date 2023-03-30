import numpy as np
import cv2
import time
import serial

global fc, fp, WIN_NAME

WIN_NAME = "Output"
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


def optical_flow(cam, fc, fp):
    while True:
        ret, fc = cam.read()

        if ret:     # if there's a frame
            fc = cv2.cvtColor(fc, cv2.COLOR_BGR2GRAY)  # convert to grayscale
            fc = cv2.GaussianBlur(fc, (9, 9), 20)  # blur bc my webcam is *fart noises*
            fc = np.array(fc, dtype=int)
            diff = fc - fp      # subtracts current frame from background
            ft = np.array(threshold(diff), dtype=np.uint8)  # subtract current and previous frame, then threshold
            cv2.rectangle(ft, (int(WIDTH / 3), 0), (int(2 * WIDTH / 3), int(HEIGHT)), (255, 0, 0), 2)   # square
            cv2.rectangle(ft, (int(WIDTH / 2), 0), (int(WIDTH / 2), int(HEIGHT)), (255, 0, 0), 2)       # split the frame equally
            acc = accumulate(ft, int(WIDTH))
            if 5000 < acc < 1e5:
                #print(acc, "motion")
                return True
            cv2.imshow(WIN_NAME, ft)
            fp = fc

        if cv2.waitKey(1) & 0xFF == ord('q'):       # show frame through webcam
            return False


def detect_face(cam, model):
    start = time.time()
    has_faces = False
    pos = -1    # -1 ORIGINALLY
    while time.time() - start < 5 and not has_faces:

        ret, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = model.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=4)
        if isinstance(faces, np.ndarray):
            has_faces = True
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            pos = x + int(w / 2)
            cv2.imshow(WIN_NAME, frame)

        return pos

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return


def center_camera(xpos, w):
    # if the face is within the region, you good
    if int(w/3) < xpos < int(2*w/3):
        return
    #
    #   calculate the step angle here
    #
    time.sleep(1)
    #print("done moving to", xpos)



# start main
cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
face = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# initial position of the motor
position = 90

ret, fc = cap.read()        # reads the frame, bool var returns true if frame is available
WIDTH = cap.get(3)          # check the frame width
HEIGHT = cap.get(4)         # check the frame height
fc = cv2.cvtColor(fc, cv2.COLOR_BGR2GRAY)   # change the color space to grey
fp = np.zeros_like(fc, dtype=int)           # return an array of zeros w/ the same data types

# initialize serial comm
ser = serial.Serial('COM16', 115200, timeout=1)

while True:

    # while there's no motion in outer region of frame
    moving = optical_flow(cap, fc, fp)

    # look for face in outer area for 2s or until detected
    if moving:
        pos = detect_face(cap, face)
        print("xpos", pos)

        # xpos mapping
        if pos >= 0:
            xpos = np.int32(((pos - 50) / (580-50)) * (255))
            ser.write(int.to_bytes(abs(xpos.item()), 1, 'big'))     # send as positve integers

            # calculate step angle
            angle = np.int32(((xpos - 50)/(255-50)) * (2) + (-1))

    # if face found, center camera... somehow
    if pos != -1:
        center_camera(pos, WIDTH)
    else: print("face not found")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
