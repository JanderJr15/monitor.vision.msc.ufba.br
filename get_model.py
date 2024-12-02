# from ultralytics import YOLO
# import os
#
#
# if not os.path.exists('vision/models/new_models'):
#     os.makedirs('vision/models/new_models')
#
# name = "yolov8s"
# model = YOLO(f'vision/models/new_models/{name}.pt')
# model.export(format="tflite")
# labels = model.names
#
# with open(f"vision/models/new_models/labels-{name}.txt", "w") as file:
#     for label in labels.values():
#         file.write(f"{label}\n")

import cv2
from mjpeg_streamer import MjpegServer, Stream

cap = cv2.VideoCapture(0)

stream = Stream("my_camera", size=(640, 480), quality=50, fps=30)

server = MjpegServer("localhost", 8080)
server.add_stream(stream)
server.start()

while True:
    _, frame = cap.read()
    # print(frame)
    cv2.imshow(stream.name, frame)
    if cv2.waitKey(1) == ord("q"):
        break

    stream.set_frame(frame)

server.stop()
cap.release()
cv2.destroyAllWindows()