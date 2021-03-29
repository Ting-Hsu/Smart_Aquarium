import numpy as np
import cv2
import os
from flask import Flask, request, render_template, Response
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
# import torch
from PIL import Image
# from io import BytesIO,StringIO
import base64

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
cors = CORS(app)
api = Api(app)

# UPLOAD_FOLDER = 'UPLOAD_FOLDER'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

webcam = "http://192.168.43.181:8080/?action=stream"
# webcam = 0

# yolov5
# model = torch.hub.load('ultralytics/yolov5', 'custom', path_or_model='../best20210315.pt', autoshape=True)  # for file/URI/PIL/cv2/np inputs and NMS
# model.conf = 0.50  # confidence threshold (0-1)
# model.iou = 0.50 # NMS IoU threshold (0-1)
# set_model_conf = 0.50 # 
# set_model_iou = 0.50 # 

# yolov4 
model_folder_path = "yolo-coco"
model_label = "obj.names"
model_weights = "yolov4-tiny-fish_best.weights"
model_cfg = "yolov4-tiny-fish.cfg"
set_confidence = 0.50
set_threshold = 0.45

###########################  YOLOv4 串流辨識 ok  #############################
class YOLOv4LiveStreaming(Resource):
    def __init__(self):
        # WebCam
        self.cap = cv2.VideoCapture(webcam)
        # 讀取label檔
        self.labelsPath = os.path.sep.join([model_folder_path, model_label])
        self.LABELS = open(self.labelsPath).read().strip().split("\n")
        # 隨機標籤顏色
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3),dtype="uint8")
        # Model 相關設定
        self.set_confidence = set_confidence # 預設信心指數
        self.set_threshold = set_threshold #
        # 讀取權重
        self.weightsPath = os.path.sep.join([model_folder_path, model_weights])
        self.configPath = os.path.sep.join([model_folder_path, model_cfg])
        self.net = cv2.dnn.readNetFromDarknet(self.configPath, self.weightsPath)
        # 獲取網絡所有層的名稱
        self.ln = self.net.getLayerNames()
        # 獲取輸出圖層的索引
        self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        self.fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        self.socket_data = ""
    def get(self):
        return Response(self.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    def post(self):
        print("YOLOv4LiveStream Start...! ")

    def gen_frames(self):
        print("YOLOv4LiveStream 相機開啟")
        (W, H) = (None, None)
        while True:
            ret, frame = self.cap.read() # 讀取每一幀圖像
            #print(type(frame)) # numpy.ndarray
            frame = cv2.resize(frame, (640, 360)) # 將圖像壓縮成 640,360
            if W is None or H is None: (H, W) = frame.shape[:2] # 檢查圖片形狀，並給值
            '''
            blobFromImage 功能
            對圖像進行預處理，包括減均值，比例縮放，裁剪，交換通道等，返回一個4通道的blob，可以想像成是一個 N維 的數組，用於神經網絡的輸入
            (416, 416) 設定輸出影像尺寸
            (1 / 255.0) 設定影像尺寸
            mean 用於各通道減去的值，以降低光照的影響
            swapRB:交換RB通道，默認為False (cv2.imread讀取的是彩圖是bgr通道)
            crop:圖像裁剪,默認為False. 當值為True時，先按比例縮放，然後從中心裁剪成size尺寸
            blob 在電腦的術語裡面其實是 Binary Large Object 的簡寫，說穿了就是一種以很長一串 0、1 二進位表示的物件。那為什麼會冒出來這東西呢？其實，DNN 也是需要自己能夠接受的 Input 格式，這個 blobFromImage 指令就是命令程式先把第 32 到 36 列照相機抓進來的畫面，經過縮放處理之後，再轉換成 DNN 可以接受的 Input 格式，才給 DNN 去當成 Input。
            '''
            blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),swapRB=True, crop=False)
            # 將圖像和輸出合併
            self.net.setInput(blob) # 設定網路
            layerOutputs = self.net.forward(self.ln) # 進行推論
            # print(layerOutputs) # 整張圖的陣列值
            boxes = [] ; confidences = [] ; classIDs = [] ; inference_data = []
            for output in layerOutputs: # 在每個圖層上做輸出循環
                for detection in output: # 將圖片輸出做檢測
                    # 取出當前物件偵測到是屬於那個ClassID和信心指數是多少
                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]
                    # 偵測信心指數 大於 預設值信心指數
                    if confidence > self.set_confidence:
                        # 縮放邊框相對於圖片大小的坐標
                        # 請記住YOLO 實際上返回邊界框的中心（x，y）坐標，然後返回框的寬度和高度
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype("int")
                        # 使用中心（x，y）坐標算出邊界框的和左上角
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))
                        # 更新邊界框坐標，confidence 和 classID 的列表
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)
            # 應用非最大值抑制來抑制弱的重疊邊界框
            idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.set_confidence,self.set_threshold)
            # 確保至少有一個檢測到
            if len(idxs) > 0:
                # 循環遍歷保持的索引
                for i in idxs.flatten():
                    # 提取邊界框坐標
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])
                    # 在邊框上繪製邊框和標籤
                    color = [int(c) for c in self.COLORS[classIDs[i]]]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    text = "{}: {:.4f}".format(self.LABELS[classIDs[i]], confidences[i])
                    cv2.putText(frame, text, (x, y - 5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    inference_data.append({"label": self.LABELS[classIDs[i]], "bbox":boxes[i], "confidences": confidences[i]})
            # 利用cv2影像解碼功能，讀取每幀圖像轉乘binary印在網頁上
            ret, buffer = cv2.imencode('.jpg', frame) 
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        self.cap.release()
        cv2.destroyAllWindows()

###########################  YOLOv4 上傳辨識 ok  #############################
class YOLOv4UploadToModelInference(Resource):
    def __init__(self):
        self.name="nc"
        self.count=0
        # 讀取label檔
        self.labelsPath = os.path.sep.join([model_folder_path, model_label])
        self.LABELS = open(self.labelsPath).read().strip().split("\n")
        # 隨機標籤顏色
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3),dtype="uint8")
        # Model 相關設定
        self.set_confidence = set_confidence # 預設信心指數
        self.set_threshold = set_threshold # 預設 iou
        # 讀取權重
        self.weightsPath = os.path.sep.join([model_folder_path, model_weights])
        self.configPath = os.path.sep.join([model_folder_path, model_cfg])
        self.net = cv2.dnn.readNetFromDarknet(self.configPath, self.weightsPath)
        # 獲取網絡所有層的名稱
        self.ln = self.net.getLayerNames()
        # 獲取輸出圖層的索引
        self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        self.fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    def get(self):
        return "YOLOv4UploadToModelInference"

    def post(self):
        '''
        nodejs-client ajax:
        var form_data = new FormData();  // 可以想像成建立一個裝載檔案的箱子
        var file_data = $('#blockimg').prop('files'); //取得檔案資料
        for(let i=0; i<file_data.length;i++){    // 迴圈是要把多個檔案裝到箱子裡
            form_data.append('file', file_data[i]); // 這裡的 file 會對應到flask request.files.getlist('file')
        } 

        '''
        img_files_list = request.files.getlist("file") # 接收多筆上傳的檔案
        data = []
        (W, H) = (None, None)
        for img in img_files_list: # 辨識每張圖
            '''
            Image.open 讀 RGB 和 cv2.imread 讀 BGR  所以要轉換成cv2可以讀的格式。 
            '''
            img = Image.open(img).convert("RGB")
            img = cv2.cvtColor(np.array(img),cv2.COLOR_RGB2BGR)
            # 將圖片壓縮成 640
            frame = cv2.resize(img, (640, 360))
            if W is None or H is None: # 如果長寬是0 就賦予frame 的長寬
                (H, W) = frame.shape[:2] 
            blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                swapRB=True, crop=False)
            self.net.setInput(blob) # 圖像與網路結合
            layerOutputs = self.net.forward(self.ln) # 開始inference
            boxes = [] ; confidences = [] ; classIDs = [] ; inference_data = []
            for output in layerOutputs:
                for detection in output:
                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]
                    if confidence > self.set_confidence:
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype("int")
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)
            idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.set_confidence, self.set_threshold)
            if len(idxs) > 0:
                for i in idxs.flatten():
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])
                    color = [int(c) for c in self.COLORS[classIDs[i]]]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    text = "{}: {:.4f}".format(self.LABELS[classIDs[i]],confidences[i])
                    cv2.putText(frame, text, (x, y - 5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    inference_data.append({"label": self.LABELS[classIDs[i]], "bbox":boxes[i], "confidences": confidences[i]})
            base64_str = cv2.imencode('.jpg',frame)[1]
            base64_str = base64.b64encode(base64_str).decode('ascii')
            data.append([inference_data,{"base64": base64_str}])
            print(data)
        return data


###########################  YOLOv5 串流辨識  #############################
class YOLOv5LiveStreaming(Resource):
    def __init__(self):
        self.name=""
        self.cap = cv2.VideoCapture(webcam)
        self.font = cv2.FONT_HERSHEY_SIMPLEX # 字體樣式
        self.font_scale = 0.8 # 縮放比例
        self.font_line_size = 1 # 線粗細
        self.thickness = cv2.FILLED # 填滿(-1) 
        self.status = None
        # 讀取label檔
        self.labelsPath = os.path.sep.join([model_folder_path, model_label])
        self.LABELS = open(self.labelsPath).read().strip().split("\n")
        # 根據LABEL數量做出不同類別對應不同顏色
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3),dtype="uint8")
        self.img_size = 480
        self.fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    def get(self):
        # return {"data":1}
        return Response(self.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    def post(self):
        print("YOLOv5LiveStream 相機開啟")
        
    def gen_frames(self):
        (W, H) = (None, None) # 圖像長寬初始化
        while True:
            success, frame = self.cap.read()  # read the camera frame
            if not success: # 相機沒有開啟
                break
            else: # 讀取到相機
                if W is None or H is None: #
                    (H, W) = frame.shape[:2]
                results = model(frame) # 辨識
                json_results = self.results_to_json(results, model) # 將辨識結果轉成json格式
                ################################################################## 方法一
                if len(json_results[0])>0: # 每張frame偵測到有幾個物件，大於0畫框
                    for i in json_results[0]: # 將一張圖上的每個物件畫框
                        if i['confidence'] > set_model_conf: # 信心指數大於多少就畫框
                            cs, cn, bbox, cf = i['class'], i['class_name'], i['normalized_box'], i['confidence']
                            text = ""+ str(cn)+": {:.1f}%".format(cf * 100) # 偵測到的物件標籤文字
                            box = bbox[0:4] * np.array([W, H, W, H]) # 把 bbox 還原成實際大小
                            color = [int(c) for c in self.COLORS[len(i)]]
                            (centerX, centerY, width, height) = box.astype("int") # 然後把 bbox 轉成整數
                            # print([centerX,centerY,width, height])
                            # 要先計算文字長寬和縮放比例，再去畫文字的背景框
                            text_wh, text_scale  = cv2.getTextSize(text, self.font, self.font_scale, self.font_line_size) # 要輸入的字符串, font, fontScale, thickness
                            # 畫物件框線
                            cv2.rectangle(frame, (centerX, centerY),(width ,height), color, 4) 
                            # 畫標籤背景框-填滿
                            cv2.rectangle(frame, (centerX, centerY), (centerX+text_wh[0], centerY-50), color, self.thickness)
                            # cv2.putText(影像, 文字, 座標, 字型, 大小, 顏色, 線條寬度, 線條種類)
                            cv2.putText(frame, text, (centerX, centerY-10), self.font, self.font_scale, (255,255,255), self.font_line_size,cv2.LINE_AA)
                    # 以下利用cv2影像解碼功能，讀取每幀圖像轉成binary印在網頁上
                    ret, buffer = cv2.imencode('.jpg', frame) 
                    frame = buffer.tobytes()
                    
                    yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                else:
                    # 以下利用cv2影像解碼功能，讀取每幀圖像轉成binary印在網頁上
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    # bytearray
                    yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        self.cap.release()
        cv2.destroyAllWindows()


    def results_to_json(self, results, model):
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

###########################  YOLOv5 上傳辨識ok  #############################
class YOLOv5UploadToModelInference2(Resource):  
    def __init__(self):
        # OpenCV - font style
        self.font = cv2.FONT_HERSHEY_SIMPLEX # 字體樣式
        self.font_scale = 0.8 # 縮放比例
        self.font_line_size = 1 # 線粗細
        self.thickness = cv2.FILLED # 填滿(-1) 
        self.count=0 # make to files
        self.data=[] # data array
        # 讀取label檔
        self.labelsPath = os.path.sep.join([model_folder_path, model_label])
        self.LABELS = open(self.labelsPath).read().strip().split("\n")
        # 根據LABEL數量做出不同類別對應不同顏色
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3),dtype="uint8")
        self.img_size = 320
        self.status = None
    def get(self):
        return "get"
    def post(self):
        img_files_list = request.files.getlist("file") # 接收多筆上傳的檔案
        data = []
        (W, H) = (None, None)
        for img in img_files_list: # 辨識每張圖
            img = Image.open(img).convert("RGB") # yolov5 torchloadmodel 不用再轉cv2 BGR
            if W is None or H is None:
                (H, W) = img.size[:2]
            results = model(img,size=320) # 辨識
            json_results = results_to_json(results, model) # 將結果整理成json格式
            print(json_results)
            img = cv2.cvtColor(np.array(img),cv2.COLOR_RGB2BGR) # 因應下方cv2只接收格式為BGR 所以這邊要轉成符合格式
            # 將圖片壓縮成 640
            frame = cv2.resize(img, (W, H))
            # print(frame)
            for i in json_results[0]: # 將一張圖上的每個物件畫框
                if i['confidence'] > set_model_conf: # 大於多少信心指數再畫框
                    cs, cn, bbox, cf = i['class'], i['class_name'], i['normalized_box'], i['confidence']
                    text = ""+ str(cn)+": {:.1f}%".format(cf * 100) # 偵測到的物件標籤文字
                    box = bbox[0:4] * np.array([W, H, W, H]) # 把 bbox 還原成實際大小
                    color = [int(c) for c in self.COLORS[0]]
                    (centerX, centerY, width, height) = box.astype("int") # 然後把 bbox 轉成整數
                    # print([centerX,centerY,width, height])
                    # 要先計算文字長寬和縮放比例，再去畫文字的背景框
                    text_wh, text_scale  = cv2.getTextSize(text, self.font, self.font_scale, self.font_line_size) # 要輸入的字符串, font, fontScale, thickness
                    # 畫物件框線
                    cv2.rectangle(frame, (centerX, centerY),(width ,height), color, 4) 
                    # 畫標籤背景框-填滿
                    cv2.rectangle(frame, (centerX, centerY), (centerX+text_wh[0], centerY-50), color, self.thickness)
                    # cv2.putText(影像, 文字, 座標, 字型, 大小, 顏色, 線條寬度, 線條種類)
                    cv2.putText(frame, text, (centerX, centerY-10), self.font, self.font_scale, (0, 0, 0), self.font_line_size,cv2.LINE_AA)
            # # cv2_image to image_base64
            base64_str = cv2.imencode('.jpg',frame)[1]
            base64_str = base64.b64encode(base64_str).decode('ascii')
            json_results.append({"base64":base64_str})
            data.append(json_results)
            '''
            要再補上：
                信心指數大於多少再 push data，不要全部都push，
            '''
        return data # all inference data


# 測試用
class YOLOv4UploadToModelInference1(Resource):
    def __init__(self):
        self.name="nc"
        self.count=0
        # 讀取label檔
        self.labelsPath = os.path.sep.join([model_folder_path, model_label])
        self.LABELS = open(self.labelsPath).read().strip().split("\n")
        # 隨機標籤顏色
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3),dtype="uint8")
        # Model 相關設定
        self.set_confidence = set_confidence # 預設信心指數
        self.set_threshold = set_threshold # 預設 iou
        # 讀取權重
        self.weightsPath = os.path.sep.join([model_folder_path, model_weights])
        self.configPath = os.path.sep.join([model_folder_path, model_cfg])
        self.net = cv2.dnn.readNetFromDarknet(self.configPath, self.weightsPath)
        # 獲取網絡所有層的名稱
        self.ln = self.net.getLayerNames()
        # 獲取輸出圖層的索引
        self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        # self.fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    def get(self):
        return "YOLOv4UploadToModelInference"
    def post(self):
        data = request.get_json(silent=True) # 接收 nodejs-server 的圖片base64資料
        item = data.get('data') # item = base64_string
        data = []
        (W, H) = (None, None)
        for i in item: # 有幾張圖
            self.count+=1
            # print(i) # base64: /9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAIBAQEBAQIBAQECAgICAgQDAgICAgUEBAMEBgUGBgYFBgYGBwkIBgcJBwYGCAsICQoKCgoKBggLDA
            # print(BytesIO(i))
            '''
            encode是 unicode 轉換成str  /// decode是 str 轉換成 unicode。
            base64.b64decode(i) 將base64字串轉成 binary byte。
            BytesIO實現了在內存中讀寫bytes，我們創建一個BytesIO，然後寫入一些bytes：
            Image.open()
            '''
            im = Image.open(BytesIO(base64.b64decode(i))) # 圖片 base64 解碼
            # print(im) # <PIL.JpegImagePlugin.JpegImageFile image mode=RGB.......
            im.save('../public/inference/pre_inference'+str(self.count)+'.jpg') # 解碼base64後存成實體圖片
            frame = cv2.imread('../public/inference/pre_inference'+str(self.count)+'.jpg')
            # print(frame) # ndarray
            frame = cv2.resize(frame, (640, 360))
            if W is None or H is None:
                (H, W) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                swapRB=True, crop=False)
            self.net.setInput(blob)
            layerOutputs = self.net.forward(self.ln)
            boxes = [] ; confidences = [] ; classIDs = [] ; inference_data = []
            for output in layerOutputs:
                for detection in output:
                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]
                    if confidence > self.set_confidence:
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype("int")
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)
            idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.set_confidence, self.set_threshold)
            if len(idxs) > 0:
                for i in idxs.flatten():
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])
                    color = [int(c) for c in self.COLORS[classIDs[i]]]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    text = "{}: {:.4f}".format(self.LABELS[classIDs[i]],confidences[i])
                    cv2.putText(frame, text, (x, y - 5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    inference_data.append({"label": self.LABELS[classIDs[i]], "bbox":boxes[i], "confidences": confidences[i]})
            base64_str = cv2.imencode('.jpg',frame)[1]
            base64_str = base64.b64encode(base64_str).decode('ascii')
            data.append([inference_data,{"base64": base64_str}])
        return data

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

# Router set
api.add_resource(YOLOv4LiveStreaming, '/YOLOv4LiveStreaming') # ok
api.add_resource(YOLOv4UploadToModelInference, '/YOLOv4UploadToModelInference') #ok
api.add_resource(YOLOv5LiveStreaming, '/YOLOv5LiveStreaming') # ok
api.add_resource(YOLOv5UploadToModelInference2, '/YOLOv5UploadToModelInference2') # ok
# 測試用
api.add_resource(YOLOv4UploadToModelInference1, '/YOLOv4UploadToModelInference1')





class YOLOv4Tracker(Resource):
    def __init__(self):
        # WebCam
        self.cap = cv2.VideoCapture(webcam)
        # 讀取label檔
        self.labelsPath = os.path.sep.join([model_folder_path, model_label])
        self.LABELS = open(self.labelsPath).read().strip().split("\n")
        # 隨機標籤顏色
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3),dtype="uint8")
        # Model 相關設定
        self.set_confidence = set_confidence # 預設信心指數
        self.set_threshold = set_threshold #
        # 讀取權重
        self.weightsPath = os.path.sep.join([model_folder_path, model_weights])
        self.configPath = os.path.sep.join([model_folder_path, model_cfg])
        self.net = cv2.dnn.readNetFromDarknet(self.configPath, self.weightsPath)
        # 獲取網絡所有層的名稱
        self.ln = self.net.getLayerNames()
        # 獲取輸出圖層的索引
        self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        self.fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        self.socket_data = ""
    def get(self):
        return Response(self.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    def post(self):
        print("YOLOv4LiveStream Start...! ")

    def gen_frames(self):
        print("YOLOv4LiveStream 相機開啟")
        (W, H) = (None, None)
        while True:
            ret, frame = self.cap.read() # 讀取每一幀圖像
            #print(type(frame)) # numpy.ndarray
            frame = cv2.resize(frame, (640, 360)) # 將圖像壓縮成 640,360
            if W is None or H is None: (H, W) = frame.shape[:2] # 檢查圖片形狀，並給值
            '''
            blobFromImage 功能
            對圖像進行預處理，包括減均值，比例縮放，裁剪，交換通道等，返回一個4通道的blob，可以想像成是一個 N維 的數組，用於神經網絡的輸入
            (416, 416) 設定輸出影像尺寸
            (1 / 255.0) 設定影像尺寸
            mean 用於各通道減去的值，以降低光照的影響
            swapRB:交換RB通道，默認為False (cv2.imread讀取的是彩圖是bgr通道)
            crop:圖像裁剪,默認為False. 當值為True時，先按比例縮放，然後從中心裁剪成size尺寸
            blob 在電腦的術語裡面其實是 Binary Large Object 的簡寫，說穿了就是一種以很長一串 0、1 二進位表示的物件。那為什麼會冒出來這東西呢？其實，DNN 也是需要自己能夠接受的 Input 格式，這個 blobFromImage 指令就是命令程式先把第 32 到 36 列照相機抓進來的畫面，經過縮放處理之後，再轉換成 DNN 可以接受的 Input 格式，才給 DNN 去當成 Input。
            '''
            blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),swapRB=True, crop=False)
            # 將圖像和輸出合併
            self.net.setInput(blob) # 設定網路
            layerOutputs = self.net.forward(self.ln) # 進行推論
            # print(layerOutputs) # 整張圖的陣列值
            boxes = [] ; confidences = [] ; classIDs = [] ; inference_data = []
            for output in layerOutputs: # 在每個圖層上做輸出循環
                for detection in output: # 將圖片輸出做檢測
                    # 取出當前物件偵測到是屬於那個ClassID和信心指數是多少
                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]
                    # 偵測信心指數 大於 預設值信心指數
                    if confidence > self.set_confidence:
                        # 縮放邊框相對於圖片大小的坐標
                        # 請記住YOLO 實際上返回邊界框的中心（x，y）坐標，然後返回框的寬度和高度
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype("int")
                        # 使用中心（x，y）坐標算出邊界框的和左上角
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))
                        # 更新邊界框坐標，confidence 和 classID 的列表
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)
            # 應用非最大值抑制來抑制弱的重疊邊界框
            idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.set_confidence,self.set_threshold)
            # 確保至少有一個檢測到
            if len(idxs) > 0:
                # 循環遍歷保持的索引
                for i in idxs.flatten():
                    # 提取邊界框坐標
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])
                    # 在邊框上繪製邊框和標籤
                    color = [int(c) for c in self.COLORS[classIDs[i]]]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    text = "{}: {:.4f}".format(self.LABELS[classIDs[i]], confidences[i])
                    cv2.putText(frame, text, (x, y - 5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    inference_data.append({"label": self.LABELS[classIDs[i]], "bbox":boxes[i], "confidences": confidences[i]})
            # 利用cv2影像解碼功能，讀取每幀圖像轉乘binary印在網頁上
            ret, buffer = cv2.imencode('.jpg', frame) 
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        self.cap.release()
        cv2.destroyAllWindows()



# tracker cv
api.add_resource(YOLOv4Tracker, '/YOLOv4Tracker')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
    


