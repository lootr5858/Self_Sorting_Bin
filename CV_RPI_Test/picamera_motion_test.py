""" required libraries """
import cv2
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

""" parameters for RPI camera """
resolution = (240, 240)
video_format = "bgr"
frame_no = 0    # to record no of frames captured
initial_time = time.time()

""" setup RPI camera """
camera = PiCamera()
camera.resolution = resolution
camera.framerate = 32
rawCapture = PiRGBArray(camera, size = resolution)

time.sleep(0.1) # time for Pi Camera to warmup

""" create frames for comparison: initial frame, previous frame & current frame """
first_frame = None
previous_frame = None
current_frame = None

""" start video capturing with opencv """
for video in camera.capture_continuous(rawCapture, format = video_format, use_video_port = True):
    """ extract details from video frame """
    frame = video.array
    frame_no += 1

    """ debugging """
    # print(frame)

    """ record previous frame for comparison """
    previous_frame = current_frame

    """ convert frame to grayscale and guassian blur image for processing """
    current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    current_frame = cv2.GaussianBlur(current_frame, (21,21), 0)

    """ save the 1st frame captured """
    if first_frame is None:
        first_frame = current_frame

    """ verify the difference between the first & current frame (using diff in pixel) """
    delta_frame = cv2.absdiff(first_frame, current_frame)
    thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_delta = cv2.dilate(thresh_delta, None, iterations=0)
    (_, cnts, _) = cv2.findContours(thresh_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    """ identify the region where motion is detected
        tweak sensitivity. by number of different pixel """
    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
    

    """ display video frame """
    cv2.imshow('Video', frame)
    cv2.imshow('Processing', current_frame)
    cv2.imshow('Delta', delta_frame)
    cv2.imshow('Thresh', thresh_delta)


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
