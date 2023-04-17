import cv2
import numpy as np

known_distance = 40.5
known_width = 6.125

GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image):
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
    # getting coordinates x, y , width and height
    diff = 0
    for (x, y, h, w) in faces:
        # draw the rectangle on the face
        cv2.rectangle(image, (x, y), (x + w, y + h), GREEN, 2)
        cv2.circle(image, (x+int(w/2), y+int(h/2)), 5, RED, 1)
        diff = dim[1]/2 - (x+int(w/2))
        # cv2.line(image, (x+int(w/2), int(dim[0]/2)), (int(dim[1]/2), int(dim[0]/2)), GREEN, 1)
        # print(diff)
        # getting face width in the pixels
        face_width = w

    # return the face width in pixel
    return face_width, diff


def angleCalc(hypotenuse, opposite):
    return np.arcsin(opposite/hypotenuse)


face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

ref_image = cv2.imread("RF.jpg")
ref_image_face_width, _ = face_data(ref_image)
# print(str(ref_image_face_width) + "here")
Focal_length_found = Focal_Length_Finder(
    known_distance, known_width, ref_image_face_width)

# print(Focal_length_found)

# cv2.imshow("ref_image", ref_image)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
fonts = cv2.FONT_HERSHEY_COMPLEX

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
        Distance = Distance_finder(
            Focal_length_found, known_width, face_width_in_frame)

        angle = angleCalc(Distance, scaled_face_difference)


        # draw line as background of text
        cv2.line(frame, (30, 30), (230, 30), RED, 32)
        cv2.line(frame, (30, 30), (230, 30), BLACK, 28)

        # Drawing Text on the screen
        cv2.putText(
            frame, f"Angle: {round(angle*180/(np.pi), 2)} deg", (30, 35),
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



