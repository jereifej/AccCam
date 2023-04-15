import cv2
import numpy as np
import time
import threading
import speech_recognition as sr

def faceRec() :
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("yeah!")
    # Turn off auto exposure
    # cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
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
            faces = face.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            # numpy.append(faces, face.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # print(isinstance(faces, tuple))
        # print(isinstance(faces, np.ndarray))
        cv2.imshow('output', frame)
        count += 1
        diff = time.time() - instFPS
        acc += diff

        # print("FPS: ", 1.0 / diff)  # FPS = 1 / time to process loop
        print("Avg FPS: ", count / acc)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()


def NLP() :
    r = sr.Recognizer()
    m = sr.Microphone()

    try:
        print("A moment of silence, please...")
        with m as source:
            r.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(r.energy_threshold))
        while True:
            print("Say something!")
            with m as source:
                audio = r.listen(source)
            print("Got it! Now to recognize it...")
            try:
                # recognize speech using Google Speech Recognition
                value = r.recognize_google(audio)

                # we need some special handling here to correctly print unicode characters to standard output
                if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                    print(u"You said {}".format(value).encode("utf-8"))
                else:  # this version of Python uses unicode for strings (Python 3+)
                    print("You said {}".format(value))
            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    # creating thread
    t1 = threading.Thread(target=faceRec, args=())
    t2 = threading.Thread(target=NLP, args=())

    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()

    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()

    # both threads completely executed
    print("Done!")