import cv2
import numpy as np
import time
from pygame import mixer

mixer.init()
mixer.music.load('./src/index/alarm.wav')

# Load the YOLO model
net = cv2.dnn.readNet("./lib/yolov3-files/yolov3_training_2000.weights", "./lib/yolov3-files/yolov3_testing.cfg")
classes = [""]
#with open("./configuration/coco.names", "r") as f:
    #classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Load webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
font = cv2.FONT_HERSHEY_SIMPLEX
starting_time = time.time()
frame_id = 0

while True:
    # Read webcam
    _, frame = cap.read()
    frame_id += 1
    height, width, channels = frame.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Visualising data
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.1:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.8, 0.3)
    if indexes == 0: 
        frame = cv2.copyMakeBorder(frame, 10, 10, 10, 10, cv2.BORDER_CONSTANT, None, value=[0, 0, 255])
        mixer.music.play(-1)
    else:
        frame = cv2.copyMakeBorder(frame, 10, 10, 10, 10, cv2.BORDER_CONSTANT, None, value=[0, 255, 0])
        mixer.music.stop()
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            color = colors[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    elapsed_time = time.time() - starting_time
    fps = frame_id / elapsed_time
    cv2.namedWindow("Image", flags=cv2.WINDOW_GUI_NORMAL)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setWindowProperty("Image", cv2.WND_PROP_TOPMOST, 1)
    cv2.resizeWindow("Image", 800, 600)
    cv2.moveWindow("Image", 370, 75)
    cv2.imshow("Image", frame)
    key = cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()