import numpy as np
import argparse
import imutils
import time
import cv2
import os
from flask import Flask, request, render_template, Response
from flask_restful import reqparse, abort, Api, Resource
import cv2
from PIL import Image
from io import BytesIO,StringIO
import base64
import torch
import numpy as np
import websockets
import asyncio
import yaml
import socket

app = Flask(__name__)
api = Api(app)

set_confidence = 0.40
set_threshold = 0.45

# cap = cv2.VideoCapture("http://192.168.43.181:8080/?action=stream")
# model = torch.hub.load('ultralytics/yolov5', 'custom', path_or_model='best.pt', autoshape=True)  # for file/URI/PIL/cv2/np inputs and NMS
# model.conf = 0.10  # confidence threshold (0-1)
# model.iou = 0.30  # NMS IoU threshold (0-1)

# yaml
with open('./classes.yaml', 'r') as f:
    classes = yaml.load(f)


# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join(["yolo-coco", "obj.names"])
LABELS = open(labelsPath).read().strip().split("\n")
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),dtype="uint8")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join(["yolo-coco", "yolov4-tiny-fish_final.weights"])
configPath = os.path.sep.join(["yolo-coco", "yolov4-tiny-fish.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes) and determine only the *output* layer names that we need from YOLO
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
fourcc = cv2.VideoWriter_fourcc(*"MJPG")
print("[INFO] starting video capture...")
cap = cv2.VideoCapture("http://192.168.43.181:8080/?action=stream")
# cap = cv2.VideoCapture(0)
time.sleep(2.0)

# infernect_data_convert_to_json
def results_to_json(results, model):
    return [
        [
            {
                "class": int(pred[5]),
                "class_name": model.model.names[int(pred[5])],
                "normalized_box": pred[:4].tolist(),
                "confidence": float(pred[4]),
            }
            for pred in result
        ]
        for result in results.xyxyn
    ]

# run yolov4
def gen_frames():
	# print(model.model.names)
	(W, H) = (None, None)
	while True:
		ret, frame = cap.read()
		frame = cv2.resize(frame, (640, 360))
		if W is None or H is None:
			(H, W) = frame.shape[:2]
		# construct a blob from the input frame and then perform a forward pass of the YOLO object detector,
		# giving us our bounding boxes and associated probabilities
		blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),swapRB=True, crop=False)
		net.setInput(blob)
		layerOutputs = net.forward(ln)
		# initialize our lists of detected bounding boxes, confidences, and class IDs, respectively
		boxes = []
		confidences = []
		classIDs = []
		for output in layerOutputs: 	# loop over each of the layer outputs
			for detection in output:		# loop over each of the detections
				# extract the class ID and confidence (i.e., probability) of the current object detection
				scores = detection[5:]
				classID = np.argmax(scores)
				confidence = scores[classID]
				# filter out weak predictions by ensuring the detected probability is greater than the minimum probability
				if confidence > set_confidence:
					# scale the bounding box coordinates back relative to the size of the image, keeping in mind that YOLO
					# actually returns the center (x, y)-coordinates of the bounding box followed by the boxes' width and height
					box = detection[0:4] * np.array([W, H, W, H])
					(centerX, centerY, width, height) = box.astype("int")
					# use the center (x, y)-coordinates to derive the top and and left corner of the bounding box
					x = int(centerX - (width / 2))
					y = int(centerY - (height / 2))
					# update our list of bounding box coordinates, confidences, and class IDs
					boxes.append([x, y, int(width), int(height)])
					confidences.append(float(confidence))
					classIDs.append(classID)
		# apply non-maxima suppression to suppress weak, overlapping bounding boxes
		idxs = cv2.dnn.NMSBoxes(boxes, confidences, set_confidence,
			set_threshold)
		# ensure at least one detection exists
		if len(idxs) > 0:
			# loop over the indexes we are keeping
			for i in idxs.flatten():
				# extract the bounding box coordinates
				(x, y) = (boxes[i][0], boxes[i][1])
				(w, h) = (boxes[i][2], boxes[i][3])
				# draw a bounding box rectangle and label on the frame
				color = [int(c) for c in COLORS[classIDs[i]]]
				cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
				text = "{}: {:.4f}".format(LABELS[classIDs[i]],confidences[i])
				cv2.putText(frame, text, (x, y - 5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
				print(boxes[i])
                
		ret, buffer = cv2.imencode('.jpg', frame) # 利用cv2影像解碼功能，讀取每幀圖像轉乘binary印在網頁上
		frame = buffer.tobytes()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
		# cv2.imshow("Output", frame)
	print("[INFO] cleanup up...")
	cap.release()
	cv2.destroyAllWindows()

# router
@app.route('/live_video')
def live_video():
    # 影像串流網址 打印在img src tag上
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



# darknet yolo4 upload image inference
class UploadToModelInference(Resource):
    def __init__(self):
        self.name="nc"
        self.count=0
    def get(self):
        return "get"
    def post(self):
        data = request.get_json(silent=True) # 接收 nodejs-server 的圖片base64資料
        item = data.get('data') # item = base64_string
        data = []
        (W, H) = (None, None)
        for i in item: # 有幾張圖
            self.count+=1
            im = Image.open(BytesIO(base64.b64decode(i))) # 圖片 base64 解碼
            im.save('../public/inference/pre_inference'+str(self.count)+'.jpg') # 解碼base64後存成實體圖片
            # # base64 to Buffer
            # # OpenCV - Draw rectage Image 
            frame = cv2.imread('../public/inference/pre_inference'+str(self.count)+'.jpg')
            obj_num1=0
            frame = cv2.resize(frame, (640, 360))
            if W is None or H is None:
                (H, W) = frame.shape[:2]
            # construct a blob from the input frame and then perform a forward pass of the YOLO object detector,
            # giving us our bounding boxes and associated probabilities
            blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                swapRB=True, crop=False)
            net.setInput(blob)
            # start = time.time()
            layerOutputs = net.forward(ln)
            # end = time.time()

            # initialize our lists of detected bounding boxes, confidences, and class IDs, respectively
            boxes = []
            confidences = []
            classIDs = []
            inference_data = []
            for output in layerOutputs: 	# loop over each of the layer outputs
                for detection in output:		# loop over each of the detections
                    # extract the class ID and confidence (i.e., probability) of the current object detection
                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]
                    # filter out weak predictions by ensuring the detected probability is greater than the minimum probability
                    if confidence > set_confidence:
                        # scale the bounding box coordinates back relative to the size of the image, keeping in mind that YOLO
                        # actually returns the center (x, y)-coordinates of the bounding box followed by the boxes' width and height
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype("int")
                        # use the center (x, y)-coordinates to derive the top and and left corner of the bounding box
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))
                        # update our list of bounding box coordinates, confidences, and class IDs
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)
            # apply non-maxima suppression to suppress weak, overlapping bounding boxes
            idxs = cv2.dnn.NMSBoxes(boxes, confidences, set_confidence,
                set_threshold)
            # ensure at least one detection exists
            if len(idxs) > 0:
                # loop over the indexes we are keeping
                for i in idxs.flatten():
                    # extract the bounding box coordinates
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])
                    # draw a bounding box rectangle and label on the frame
                    color = [int(c) for c in COLORS[classIDs[i]]]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    text = "{}: {:.4f}".format(LABELS[classIDs[i]],confidences[i])
                    cv2.putText(frame, text, (x, y - 5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    inference_data.append({"label": LABELS[classIDs[i]], "bbox":boxes[i], "confidences": confidences[i]})
            # # cv2_image to image_base64
            base64_str = cv2.imencode('.jpg',frame)[1]
            base64_str = base64.b64encode(base64_str).decode('ascii')
            data.append([inference_data,{"base64": base64_str}])
        return data # all inference data



api.add_resource(UploadToModelInference, '/UploadToModelInference')




# # UploadToModelInference Class
# class UploadToModelInference(Resource):
#     def __init__(self):
#         # OpenCV - font style
#         self.font = cv2.FONT_HERSHEY_SIMPLEX # 字體樣式
#         self.font_scale = 0.8 # 縮放比例
#         self.font_line_size = 1 # 線粗細
#         self.thickness = cv2.FILLED # 填滿(-1) 
#         self.count=0 # make to files
#         self.obj_num=0
#         self.data=[] # data array
#         print("start~~~~~~~~~~~~~~")
#     def get(self):
#         return "get"
#     def post(self):
#         data = request.get_json(silent=True) # 接收 nodejs-server 的圖片base64資料
#         item = data.get('data') # item = base64_string
#         # print(item) # client -> nodejs-server -> flask_API-base64_img
#         data=[]
#         for i in item: # 有幾張圖
#             self.count+=1
#             im = Image.open(BytesIO(base64.b64decode(i))) # 圖片 base64 解碼
#             im.save('../public/inference/pre_inference'+str(self.count)+'.jpg') # 解碼base64後存成實體圖片
#             # # base64 to Buffer
#             # print(type(item)) # type=str
#             # print(type(base64.b64decode(item))) # type=byte
            
#             # # Inference
#             results = model(im,size=320) # 
#             json_results = results_to_json(results,model)

#             print(json_results[0])
#             results = np.array(results.xyxy[0]) # result

#             # # OpenCV - Draw rectage Image 
#             frame = cv2.imread('../public/inference/pre_inference'+str(self.count)+'.jpg')
#             obj_num1=0
			
#             for i in results:
#                 siz = str(obj_num1)
#                 print(siz)
#                 x, y, w, h, cf, nc = i 
#                 classes_name = classes['names'][int(nc)] # yaml classes
#                 text = " "+siz+": "+str(classes_name)+": {:.1f}%".format(cf * 100) # text
#                 # 計算文字長寬和縮放比例，再去畫文字背景匡
#                 text_wh, text_scale  = cv2.getTextSize(text, self.font, self.font_scale,self.font_line_size) # 輸入的文本字符串, font, fontScale, thickness
#                 cv2.rectangle(frame, (x, y),(w, h), (0, 255, 0), 4) # Draw bbox rectangle 
#                 # Draw black-background rectangle tp fill
#                 cv2.rectangle(frame, (int(x), int(y)), (int(x+text_wh[0]), int(y-50)), (255,255,0,100), self.thickness)
#                 # write text to image
#                 # cv2.putText(影像, 文字, 座標, 字型, 大小, 顏色, 線條寬度, 線條種類)
#                 cv2.putText(frame, text, (int(x), int(y-10)), self.font, self.font_scale, (0, 0, 255),self.font_line_size,cv2.LINE_AA)
#                 obj_num1+=1
                
# 			# # cv2_image to image_base64
#             base64_str = cv2.imencode('.jpg',frame)[1]
#             base64_str = base64.b64encode(base64_str).decode('ascii')
#             json_results.append({"base64":base64_str})
#             data.append(json_results)

#         return data # all inference data

# api.add_resource(UploadToModelInference, '/UploadToModelInference')


if __name__ == '__main__':
    app.run(debug=True)




