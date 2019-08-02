
""" include required libraries & dependencies """
import cv2
from utils import draw_boxes
from frontend import YOLO
import json
import time
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import bluetooth

class Object_Recognition:
    """ setup required parameters"""
    def __init__(self, config, weight):
        self.state = 0

        """ setup picamera """
        self.frame_rate = 32
        self.resolution = (640, 640)
        self.frame_size = self.resolution[0] * self.resolution[1]
        self.camera_format = "bgr"
        self.frame_percentage = 0.1
        
        self.initial_frame = None
        self.previous_frame = None
        self.current_frame = None
        self.predict_frame = None

        """ for debugging of performance """
        self.frame_no = 0  # record number of frames captured
        self.initial_time = 0   # to take the time diff for debugging (FPS)
        self.current_time = 0
        self.previous_time = 0
        self.final_time = 0

        """ object classification """
        self.boxes = []
        self.object = {"Plastic": 0, "Metal": 1, "Glass": 2, "Paper": 3, "Trash": 4}

        """ setup model and weight for Yolo object detection """""
        self.config = config
        self.weight = weight

        with open(self.config) as config_buffer:
            self.config_json = json.load(config_buffer)

        ###############################
        #   Make the model
        ###############################

        self.yolo = YOLO(backend=self.config_json['model']['backend'],
                         input_size=self.config_json['model']['input_size'],
                         labels=self.config_json['model']['labels'],
                         max_box_per_image=self.config_json['model']['max_box_per_image'],
                         anchors=self.config_json['model']['anchors'])

        ###############################
        #   Load trained weights
        ###############################

        self.yolo.load_weights(self.weight)


    """ check for the state of the trashbin
        0: initial state. Waiting for rubbish to be thrown in
        1: trash detected. waiting for motion to stop
        2: trash detected & no motion. identify trash
        3: trash identified. Move to correct bin and deposit """
    def state_function(self):
        if self.state == 0:
            print("Waiting for waste")
            return self.detect_motion()

        elif self.state == 1:
            print("Waste detected!")
            return self.motion_stop()

        elif self.state == 2:
            print("Identifying...")
            return self.predict_trash()

        elif self.state == 3:
            print("Depositing trash...")
            return self.move_trash()

    """ detect if user place waste into bin
            capture image of initial EMPTY area
            detect motion using % change as compared to initial frame
            if motion detect, wait until motion stop: adjust no of frames according to processing speed"""

    def detect_motion(self):
        """ Setup picamera """
        camera = PiCamera()
        camera.resolution = self.resolution
        camera.framerate = self.frame_rate
        rawCapture = PiRGBArray(camera, size=self.resolution)
        time.sleep(0.1)
        motion_count = 0
        
        for video in camera.capture_continuous(rawCapture, format=self.camera_format, use_video_port=True):
            """ extract details from video frame """
            frame = video.array
            self.previous_frame = self.current_frame

            """ convert frame to grayscale and guassian blur image for processing """
            self.current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.current_frame = cv2.GaussianBlur(self.current_frame, (21, 21), 0)

            """ record the initial state of the bin (before input of waste) """
            if self.previous_frame is None:
                self.previous_frame = self.current_frame

            """ verify the difference between the first & current condition of bin (using diff in pixel) """
            delta_frame = cv2.absdiff(self.previous_frame, self.current_frame)
            thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

            """ only when certain % of pixels are different will consider as motion, prevent noise detection like fly
                calibrate sensitivity by change frame_percentage (under '__init__') """
            if np.count_nonzero(thresh_delta) > self.frame_percentage * self.frame_size:
                motion_count += 1

            else:
                motion_count = 0

            print(motion_count)

            """ if # continuous frames are different: user input waste
                proceed to the next stage: wait for user to remove his/her hand (no motion)
                # is determined by FPS of computer (faster = more #) """
            if motion_count >= 2:
                self.state += 1
                rawCapture.truncate(0)
                camera.close()
                cv2.destroyAllWindows()
                self.previous_frame = self.current_frame
                return self.state_function()

            """ for debugging """
            cv2.imshow('Video', frame)
            #cv2.imshow('Processing', self.current_frame)
            #cv2.imshow('Delta', delta_frame)
            cv2.imshow('Thresh', thresh_delta)
            # self.previous_time = self.current_time
            # self.current_time = time.time()
            # motion_latency = self.current_time - self.previous_time

            """ continue to take new frame unless keyboard interrupt detected """
            cv2.waitKey(1) & 0xFF
            rawCapture.truncate(0)

    """ wait for the user to remove their hand and the trash to stabilise
            let the trash sit for 1s after stabilise
            calibrate according to FPS """

    def motion_stop(self):
        """ Setup picamera """
        camera = PiCamera()
        camera.resolution = self.resolution
        camera.framerate = self.frame_rate
        rawCapture = PiRGBArray(camera, size=self.resolution)
        time.sleep(0.1)
        wait_count = 0
        
        for video in camera.capture_continuous(rawCapture, format=self.camera_format, use_video_port=True):
            """ extract details from video frame """
            frame = video.array

            """ record previous frame for comparison """
            self.previous_frame = self.current_frame

            """ convert frame to grayscale and guassian blur image for processing """
            self.current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.current_frame = cv2.GaussianBlur(self.current_frame, (21, 21), 0)

            """ check if there is no motion in the bin (previous frame and current frame are equal) for 2s
                adjust according to latency of the processing """
            delta_frame = cv2.absdiff(self.previous_frame, self.current_frame)
            thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

            """ only when certain % of pixels are different will consider as motion, prevent noise detection like fly
                calibrate sensitivity by change frame_percentage (under '__init__')
                 if motion is detected suddenly, reset counter """
            if np.count_nonzero(thresh_delta) < self.frame_percentage * self.frame_size:
                wait_count += 1

            else:
                wait_count = 0

            print(wait_count)

            """ give 2s after no motion detected
                frame counter depends on speed of computer """
            if wait_count > 10:
                self.state += 1
                rawCapture.truncate(0)
                camera.close()
                cv2.destroyAllWindows()
                return self.state_function()

            """ for debugging """
            cv2.imshow('Video', frame)
            #cv2.imshow("Delta", delta_frame)
            cv2.imshow("Threshold", thresh_delta)

            """ always continue to take new frame, unless keyboard interrupt """
            cv2.waitKey(1) & 0xFF
            rawCapture.truncate(0)

        cv2.destroyAllWindows()
        return self.state_function()

    """ object detection
            if more than 1 object, throw as trash
            elif object in classified with this list: paper, plastic, glass and metal, throw into correct bin
            else: throw as trash """

    def predict_trash(self):
        """ Setup picamera """
        camera = PiCamera()
        camera.resolution = self.resolution
        camera.framerate = self.frame_rate
        rawCapture = PiRGBArray(camera, size=self.resolution)
        time.sleep(0.1)
        
        """ start timing for latency debugging"""
        # self.initial_time = time.time()

        """ take an image with picamera for waste identification """
        camera.capture(rawCapture, format=self.camera_format)
        frame = rawCapture.array

        """ identify object & draw bounding box around detected object"""
        self.predict_frame = frame
        self.boxes = self.yolo.predict(self.predict_frame)
        self.predict_frame = draw_boxes(self.predict_frame, self.boxes, self.config_json['model']['labels'])

        """ for debugging """
        cv2.imshow('Object Detection', self.predict_frame)
        cv2.imshow("image", frame)
        rawCapture.truncate(0)
        camera.close()
        key = cv2.waitKey(2000) & 0xFF
            
        print("Detected, proceed to throw!")
        cv2.destroyAllWindows()
        self.state += 1
        return self.state_function()

    """ throw into correct bin
            reset all and return to state 0 after depositing waste"""

    def move_trash(self):
        """ alert arduino to throw waste into correct bin
            2: Plastic
            3: Metal
            4: Glass
            5: Paper
            6: Waste """
        if len(self.boxes) == 0:
            print("Sent to trash!")

        elif len(self.boxes) > 1:
            if all(box == self.boxes[0] for box in self.boxes):
                waste_type = self.boxes[0].get_label()
                bin_type = waste_type + 2
                print("Sent to {}!".format(waste_type))

            else:
                print("Sent to trash!")

        else:
            for box in self.boxes:
                if box is not None:
                    waste_type = box.get_label()
                    print(waste_type)
                    bin_type = 2 + waste_type
                    print("Sent to {}!".format(waste_type))

        
        return self.reset_all()

    """ revert to initial state """
    def reset_all(self):
        self.state = 0

        self.initial_frame = None
        self.previous_frame = None
        self.current_frame = None
        self.predict_frame = None

        """ for debugging of performance """
        self.frame_no = 0  # record number of frames captured
        self.initial_time = 0   # to take the time diff for debugging (FPS)
        self.current_time = 0
        self.previous_time = 0
        self.final_time = 0

        time.sleep(2)
        return self.state_function()


""" path to model & weight """
config_path = "config.json"
weight_path = "trash_sort_2_74.h5"

""" create your object
    and run! """
noob_noob = Object_Recognition(config_path, weight_path)
noob_noob.state_function()
