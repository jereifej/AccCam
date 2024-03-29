import cv2
import numpy as np
import time
import threading
import speech_recognition as sr
import serial
import struct
import datetime


known_distance = 40.5
known_width = 6.125

GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
ser = serial.Serial('COM3', 115200, timeout=1)            #SERIAL

def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image):
    # print(np.shape(width_in_rf_image))
    # print(np.shape(measured_distance))
    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length


def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):
    distance = (real_face_width * Focal_Length) / face_width_in_frame
    return distance


def face_data(image):
    face_width = 0  # making face width to zero

    # converting color image to gray scale image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detecting face in the image
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)
    dim = np.shape(image)
    # print(str(dim[0]) + " " + str(dim[1]))
    # looping through the faces detect in the image
    # getting coordinates x, y , width and height
    diff = 0
    for (x, y, h, w) in faces:
        # draw the rectangle on the face
        cv2.rectangle(image, (x, y), (x + w, y + h), GREEN, 2)
        cv2.circle(image, (x+int(w/2), y+int(h/2)), 5, RED, 1)
        diff = dim[1]/2 - (x+int(w/2))
        cv2.line(image, (x+int(w/2), int(dim[0]/2)), (int(dim[1]/2), int(dim[0]/2)), GREEN, 1)
        # print(diff)
        # getting face width in the pixels
        face_width = w

    # return the face width in pixel
    return face_width, diff


def angleCalc(hypotenuse, opposite):
    return np.arcsin(opposite/hypotenuse)
def faceRec() :
    ref_image = cv2.imread("RF.jpg")
    ref_image_face_width, _ = face_data(ref_image)
    # print(str(ref_image_face_width) + "here")
    Focal_length_found = Focal_Length_Finder(
        known_distance, known_width, ref_image_face_width)

    # print(Focal_length_found)

    # cv2.imshow("ref_image", ref_image)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    fonts = cv2.FONT_HERSHEY_COMPLEX

    test = struct.pack('f', 0.9424431920051575)
    print(test)
    # print(struct.unpack('f', test))
    ser.write(test)

    while True:

        # reading the frame from camera
        _, frame = cap.read()

        # calling face_data function to find
        # the width of face(pixels) in the frame
        face_width_in_frame, face_difference = face_data(frame)
        scaled_face_difference = .13 * face_difference
        # check if the face is zero then not
        # find the distance
        if face_width_in_frame != 0:
            # finding the distance by calling function
            # Distance finder function need
            # these arguments the Focal_Length,
            # Known_width(centimeters),
            # and Known_distance(centimeters)
            Distance = Distance_finder(
                Focal_length_found, known_width, face_width_in_frame)
            # printtime(str(Distance) + " " + str(face_difference))
            angle = angleCalc(Distance, scaled_face_difference)

            new_angle = angle * 180 / (np.pi)

            sendangle = struct.pack('f', new_angle)
            ser.write(sendangle)

            # draw line as background of text
            cv2.line(frame, (30, 30), (230, 30), RED, 32)
            cv2.line(frame, (30, 30), (230, 30), BLACK, 28)

            # Drawing Text on the screen
            cv2.putText(
                frame, f"Angle: {round(angle * 180 / (np.pi), 2)} deg", (30, 35),
                fonts, 0.6, GREEN, 2)

        # show the frame on the screen
        cv2.imshow("frame", frame)

        # quit the program if you press 'q' on keyboard
        if cv2.waitKey(1) == ord("q"):
            break

    # closing the camera
    cap.release()

    # closing the windows that are opened
    cv2.destroyAllWindows()


def NLP() :
    r = sr.Recognizer()
    m = sr.Microphone()
    now = datetime.datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    print("date and time =", dt_string)

    f = open("Transcripts/Transcript" + dt_string + ".txt", "x")
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
                    f.write(format(value).encode("utf-8") + '\n')
                    f.flush()
                else:  # this version of Python uses unicode for strings (Python 3+)
                    print("You said {}".format(value))
                    f.write(format(value) + '\n')
                    f.flush()
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