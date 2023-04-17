import cv2
import numpy as np


def DisplayHaarCascadeBox(image, object_group):
    for (x, y, w, h) in object_group:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

def PortraitAngleTest(filename, image_ratio=.7):
    face = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    profile = cv2.CascadeClassifier("haarcascade_profileface.xml")
    eye = cv2.CascadeClassifier("haarcascade_eye.xml")

    image_original = cv2.imread(filename)
    image_original = cv2.resize(image_original,
                                (0, 0),
                                fx=image_ratio,
                                fy=image_ratio,
                                interpolation=cv2.INTER_NEAREST)

    gray = cv2.cvtColor(image_original, cv2.COLOR_BGR2GRAY)
    image1 = image_original
    faces = face.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=9)
    profiles = profile.detectMultiScale(gray, scaleFactor=1.09, minNeighbors=5)
    DisplayHaarCascadeBox(image1, faces)

    cv2.imshow(filename, image1)
    cv2.waitKey(0)

    DisplayHaarCascadeBox(image1, profiles)

    cv2.imshow(filename, image1)
    cv2.waitKey(0)

    image2 = image_original
    eyes = eye.detectMultiScale(gray, scaleFactor=1.09, minNeighbors=7)

    DisplayHaarCascadeBox(image2, eyes)

    cv2.imshow(filename, image2)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


PortraitAngleTest(filename="test_images/PortraitAngle1.png", image_ratio=.7)
PortraitAngleTest(filename="test_images/PortraitAngle2.png", image_ratio=.9)
# PortraitAngleTest(filename="PortraitAngle3.png")
