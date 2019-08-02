""" required libraries """
import cv2
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

""" parameters for RPI camera """
resolution = (640, 640)
video_format = "bgr"
frame_no = 0    # to record no of frames captured
initial_time = time.time()

""" setup RPI camera """
camera = PiCamera()
camera.resolution = resolution
camera.framerate = 24
rawCapture = PiRGBArray(camera, size = resolution)


time.sleep(0.1) # time for Pi Camera to warmup

""" start video capturing with opencv """
for video in camera.capture_continuous(rawCapture, format = video_format, use_video_port = True):
    """ extract details from video frame """
    frame = video.array
    frame_no += 1

    """ debugging """
    # print(frame)

    """ display video frame """
    cv2.imshow('Video', frame)


    """ delay & check for keyboard interrupt to stop video capturing """
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)  # clear the video stream in prep for the next frame
    
    if key == ord('q'):
        break

" debug camera & compute performance "
final_time = time.time()
diff_time = final_time - initial_time
fps = frame_no / diff_time
print("No of frames: " + str(frame_no))
print("Capture time: " + str(diff_time))
print("Average fps: " + str(fps))

""" exit code """
rawCapture.truncate(0)
cv2.destroyAllWindows()
