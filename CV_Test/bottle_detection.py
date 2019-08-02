''' Libraries required '''
import cv2
import time

''' set variables '''
video = cv2.VideoCapture(0)  # set webcam to capture frame (0 is default camera)
frame_no = 1  # no of frames captured

while True:
    " Frame capturing "
    frame_no += 1  # record no of frames
    success, frame = video.read()  # read video frame captured

    " Bottle object detection "
    bottle_cascade = cv2.CascadeClassifier("bottle.xml")

    " Convert frame to greyscale"
    frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    " Identify if frame contains bottle"
    bottle_frame = bottle_cascade.detectMultiScale(frame_grey, scaleFactor=1.05, minNeighbors=5)

    " Create rectangle border around bottle "
    for x, y, w, h in bottle_frame:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow("Bottle Detection", frame)

    key = cv2.waitKey(1)  # wait for 1ms before capturing new frame

    if key == ord('q'):  # exit when key "q" is pressed
        break


print(frame_no)  # print no of frames captured
video.release()  # stop capturing and off webcam
cv2.destroyAllWindows()