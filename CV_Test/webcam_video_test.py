""" required libraries """
import cv2
import time

""" setup webcam for video capturing 
    default webcam: 0"""
video = cv2.VideoCapture(0)
frame_no = 0    # to record no of frames captured

""" start video capturing with opencv """
while True:
    """ success = determine if frame is successfully captured
        frame = details of the video frame captured """
    success, frame = video.read()

    if success:
        frame_no += 1

    """ debugging """
    # print(success)
    # print(frame)

    """ display video frame """
    cv2.imshow('Video', frame)
    fps = video.get(cv2.CAP_PROP_FPS)   # to display FPS for debugging
    print(fps)

    """ delay & check for keyboard interrupt to stop video capturing """
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

" exit code "
print(frame_no)
video.release()
cv2.destroyAllWindows()
