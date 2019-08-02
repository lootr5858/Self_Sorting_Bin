""" Libraries required """
import cv2
import time

""" store 1st frame data """
first_frame = None
frame_gray = None

""" Video capture object and select camera to use """
video = cv2.VideoCapture(0)
frame_no = 1  # record number of frames captured
initial_time = time.time()

""" Video recording + motion & face detection """
while True:
    if frame_gray is not None:
        first_frame = frame_gray

    success, frame = video.read()  # capture frame
    frame_no += 1  # record number of frames processed

    ' Convert to grayscale and guassian blur image for processing '
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.GaussianBlur(frame_gray, (21,21), 0)

    ' setting 1st frame / empty background '
    if first_frame is None:
        first_frame = frame_gray
        continue

    ' matching the difference between the first and current frame '
    delta_frame = cv2.absdiff(first_frame, frame_gray)
    thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_delta = cv2.dilate(thresh_delta, None, iterations=0)
    (cnts,_) = cv2.findContours(thresh_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    ' identify regions where motion is detected '
    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 0, 255), 3)

    ' display video '
    cv2.imshow('Video', frame)
    cv2.imshow('Processing', frame_gray)
    cv2.imshow('Delta', delta_frame)
    cv2.imshow('Thresh', thresh_delta)

    key = cv2.waitKey(1)  # wait for 1ms and check for key response

    ' exit when "q" is pressed '
    if key == ord('q'):
        break

" exit code "
final_time = time.time()
time_diff = final_time - initial_time
print(frame_no)
print(time_diff)
print(frame_no / time_diff)
video.release()
cv2.destroyAllWindows()
