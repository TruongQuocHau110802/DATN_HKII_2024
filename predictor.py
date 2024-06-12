from ultralytics import YOLO
import cv2
model = YOLO(r'model\best_object.pt')
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,360)

while cam.isOpened():
    ok,frame = cam.read()
    if ok:
        results = model(frame)
        annotated_frame = results[0].plot()
        cv2.imshow('yolov8',annotated_frame)
    if cv2.waitKey(1) == ord('q'):
        break
'''
    for result in results:
        boxes = results[0].boxes.numpy()
        for box in boxes:
            print('class',box.cls)
            print('xyxy',box.xyxy)
            print('conf',box.conf)
'''
