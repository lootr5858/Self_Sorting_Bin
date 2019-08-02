""" required libraries """
import cv2
import time

""" setting camera and capturing video """
video = cv2.VideoCapture(0)  # capture first frame from webcam. parameter: webcam to use

a = 1  # record number of frames captured

""" capture video until key pressed"""
while True:
    a += 1
    success, frame = video.read()  # read video frame captured

    ''' check if video is captured '''
    if success:
        ''' Create a CascadeClassifier Object '''
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        ''' Converting frame into greyscale '''
        frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ''' Search coordinates of the face in image '''
        faces = face_cascade.detectMultiScale(frame_grey, scaleFactor=1.05, minNeighbors=5)

        for x, y, w, h in faces:
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        cv2.imshow("Grey", frame)

        # ''' simply display video w/o processing '''
        # print(frame)
        # print(frame)
        # cv2.imshow("Video", frame) # display video frame

        key = cv2.waitKey(1)  # wait for 1ms before capturing new frame

        if key == ord('q'):
            break

    else:
        print("None")
        break

print(a)  # print no of frames captured
video.release()  # stop capturing and off webcam
cv2.destroyAllWindows()


# success, frame = video.read()  # read video frame captured
# ''' check if video is captured '''
# if success:
#     ''' Create a CascadeClassifier Object '''
#     face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#
#     ''' Converting frame into greyscale '''
#     frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     ''' Search coordinates of the face in image '''
#     faces = face_cascade.detectMultiScale(frame_grey, scaleFactor=1.05, minNeighbors=5)
#
#     for x, y, w, h in faces:
#         frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
#
#     cv2.imshow("Grey", frame)
#     print(frame)
#
#     # print(frame)  # display video data (nparray)
#     # cv2.imshow("Video", frame)  # display video
#
#     ''' exit after key press'''
#     cv2.waitKey(0)  # continue only if key is pressed
#     video.release()  #stop webcam
#     cv2.destroyAllWindows()
#
# else:
#     print("No frame captured")