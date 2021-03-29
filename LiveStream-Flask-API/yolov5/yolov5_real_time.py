
from pathlib import Path
import torch
from models.yolo import Model
import numpy as np
from PIL import Image
import cv2

def custom(path_or_model='path/to/model.pt', autoshape=True):
    model = torch.load(path_or_model) if isinstance(path_or_model, str) else path_or_model  # load checkpoint
    if isinstance(model, dict):
        model = model['model']  # load model

    hub_model = Model(model.yaml).to(next(model.parameters()).device)  # create
    hub_model.load_state_dict(model.float().state_dict())  # load state_dict
    hub_model.names = model.names  # class names
    return hub_model.autoshape() if autoshape else hub_model


model = torch.hub.load('ultralytics/yolov5', 'custom', path_or_model='./best.pt', autoshape=True)
cap = cv2.VideoCapture("http://192.168.43.181/?action=stream")

def detect():
    while True:

        ret, frame = cap.read()
        # frame = cv2.resize(frame, (640, 360))
        # results = model(frame)
        results = model(frame)
        cv2.imshow('inference',frame)
        # # 若按下 q 鍵則離開迴圈
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # results.print()
        # # results.save()
        # print(results.xyxy[0])
    cap.release()
    cv2.destroyAllWindows()
detect()


# model = custom(path_or_model='./best.pt', autoshape=True)  # custom example
# def detect1():
#     results = model(Image.open('./201832.jpg'))
#     results.print()
#     results.save()
# detect1()  
   
# model1 = torch.hub.load('ultralytics/yolov5', 'custom', path_or_model='./best.pt', autoshape=True)
# def detect2():
#     results = model1(Image.open('./201832.jpg'))
#     results.print()
#     results.save()
# detect2()  
   