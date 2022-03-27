import cv2
import os
import sys
import numpy as np
import time
from net.ViolenceDetector import ViolenceDetector
import net.DeployLiveSettings as deploySettings
import net.DataSettings as dataSettings
import net.ImageUtils as ImageUtils
import pygame #For playing sound

pygame.mixer.init()
pygame.mixer.music.load('./src/index/alarm.wav')

def PrintHelp():
    print("Usage:")
    print("\t $(ThisScript)  $(PATH_FILE_NAME_OF_SOURCE_VIDEO)")
    print()
    print("or, specified $(PATH_FILE_NAME_TO_SAVE_RESULT) to save detection result:")
    print("\t $(ThisScript)  $(PATH_FILE_NAME_OF_SOURCE_VIDEO)  $(PATH_FILE_NAME_TO_SAVE_RESULT)")
    print()


class VideoSavor:
    def AppendFrame(self, image_):
        self.outputStream.write(image_)

    def __init__(self, targetFileName, videoCapture):
        width = int(deploySettings.DISPLAY_IMAGE_SIZE)
        height = int(deploySettings.DISPLAY_IMAGE_SIZE)
        frameRate = int(videoCapture.get(cv2.CAP_PROP_FPS))
        codec = cv2.VideoWriter_fourcc(*'XVID')
        self.outputStream = cv2.VideoWriter(targetFileName + ".avi", codec, frameRate, (width, height))





""" 
                    The Game is ON!
"""

# We create a VideoCapture object to read from the camera (pass 0):



def DetectViolence(PATH_FILE_NAME_TO_SAVE_RESULT):
    # font for text used on video frames
    font = cv2.FONT_HERSHEY_SIMPLEX
    violenceDetector = ViolenceDetector()
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW) #0 assigned index for camera
    shouldSaveResult = (PATH_FILE_NAME_TO_SAVE_RESULT != None)

    if shouldSaveResult:
        videoSavor = VideoSavor(PATH_FILE_NAME_TO_SAVE_RESULT + "_Result", capture)

    listOfForwardTime = []

    # Get some properties of VideoCapture (frame width, frame height and frames per second (fps)):
    frame_width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = capture.get(cv2.CAP_PROP_FPS)

    # Print these values:
    print("CV_CAP_PROP_FRAME_WIDTH: '{}'".format(frame_width))
    print("CV_CAP_PROP_FRAME_HEIGHT : '{}'".format(frame_height))
    print("CAP_PROP_FPS : '{}'".format(fps))

    # Check if camera opened successfully
    if capture.isOpened() is False:
        print("Error opening the camera")

    flag = False
    # Read until video is completed
    while capture.isOpened():
        # Capture frame-by-frame from the camera
        ret, frame = capture.read()
        if ret:
            assert not isinstance(frame, type(None)), 'Frame not Found'

        if ret is True:
            # Display the captured frame:
            # cv2.imshow('Input frame from the camera', frame)
            netInput = ImageUtils.ConvertImageFrom_CV_to_NetInput(frame)

            startDetectTime = time.time()
            isFighting = violenceDetector.Detect(netInput)
            endDetectTime = time.time()
            listOfForwardTime.append(endDetectTime - startDetectTime)

            targetSize = deploySettings.DISPLAY_IMAGE_SIZE - 2 * deploySettings.BORDER_SIZE
            currentImage = cv2.resize(frame, (targetSize, targetSize))
            if isFighting:
                pygame.mixer.music.play(-1)
                resultImage = cv2.copyMakeBorder(frame,
                                                 deploySettings.BORDER_SIZE,
                                                 deploySettings.BORDER_SIZE,
                                                 deploySettings.BORDER_SIZE,
                                                 deploySettings.BORDER_SIZE,
                                                 cv2.BORDER_CONSTANT,
                                                 value=deploySettings.FIGHT_BORDER_COLOR)

            else:
                pygame.mixer.music.stop()
                resultImage = cv2.copyMakeBorder(frame,
                                                 deploySettings.BORDER_SIZE,
                                                 deploySettings.BORDER_SIZE,
                                                 deploySettings.BORDER_SIZE,
                                                 deploySettings.BORDER_SIZE,
                                                 cv2.BORDER_CONSTANT,
                                                 value=deploySettings.NO_FIGHT_BORDER_COLOR)
            # frameText = "Violence Detected!" if isFighting else "No Violence Detected."
            # textColor = deploySettings.FIGHT_BORDER_COLOR if isFighting else deploySettings.NO_FIGHT_BORDER_COLOR
            # cv2.putText(frame, frameText, (50, 50), font, 4, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.namedWindow("", flags=cv2.WINDOW_GUI_NORMAL)
            cv2.setWindowProperty("", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.setWindowProperty("", cv2.WND_PROP_TOPMOST, 1)
            cv2.resizeWindow("", 800, 600)
            cv2.moveWindow("", 370, 75)
            cv2.imshow("", resultImage)
            if shouldSaveResult:
                videoSavor.AppendFrame(resultImage)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                capture.release()
                cv2.destroyAllWindows()
                flag = True
                break
            else:
                isCurrentFrameValid, currentImage = capture.read()
        averagedForwardTime = np.mean(listOfForwardTime)
        # print("Averaged Forward Time: ", averagedForwardTime)

        if flag:
            break
    # print("Details about current frame:")
    # PrintUnsmoothedResults(violenceDetector.unsmoothedResults)
    # averagedForwardTime = np.mean(listOfForwardTime)
    # print("Averaged Forward Time: ", averagedForwardTime)


if __name__ == '__main__':
    print("\n\n\n")
    try:
        PATH_FILE_NAME_TO_SAVE_RESULT = sys.argv[1]+"\\"
    except:
        PATH_FILE_NAME_TO_SAVE_RESULT = "C:\\Users\\asus\\Desktop\\Anomaly Detection System\\Violence-Detection\\results\\DeployResults\\"
    DetectViolence(PATH_FILE_NAME_TO_SAVE_RESULT)

