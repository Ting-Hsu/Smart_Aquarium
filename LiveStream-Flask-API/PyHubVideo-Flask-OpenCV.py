from flask import Flask, request,jsonify,render_template
from flask_restful import reqparse, abort, Api, Resource
import torch
from PIL import Image
import websockets
import asyncio
import numpy as np
from io import BytesIO,StringIO
import base64
from werkzeug.utils import secure_filename
import cv2
import yaml
import random
import time

app = Flask(__name__)
api = Api(app)
def copy_attr(a, b, include=(), exclude=()):
    # Copy attributes from b to a, options to only include [...] and to exclude [...]
    for k, v in b.__dict__.items():
        if (len(include) and k not in include) or k.startswith('_') or k in exclude:
            continue
        else:
            setattr(a, k, v)
cap = cv2.VideoCapture(0)
model = torch.hub.load('ultralytics/yolov5', 'custom', path_or_model='best.pt', autoshape=True)  # for file/URI/PIL/cv2/np inputs and NMS
# model.load_state_dict(torch.load('best.pt')['model'].state_dict())

model.conf = 0.10  # confidence threshold (0-1)
model.iou = 0.40  # NMS IoU threshold (0-1)

with open('./classes.yaml', 'r') as f:
    classes = yaml.load(f)

# Model模型開啟

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

####################################################################################
# ####################################################################################

# UploadToModelInference Class
class UploadToModelInference(Resource):
    def __init__(self):
        # OpenCV - font style
        self.font = cv2.FONT_HERSHEY_SIMPLEX # 字體樣式
        self.font_scale = 0.8 # 縮放比例
        self.font_line_size = 1 # 線粗細
        self.thickness = cv2.FILLED # 填滿(-1) 
        self.count=0 # make to files
        self.obj_num=0
        self.data=[] # data array
        print("start~~~~~~~~~~~~~~")
    def get(self):
        return "get"

    def post(self):
        data = request.get_json(silent=True) # 接收 nodejs-server 的圖片base64資料
        item = data.get('data') # item = base64_string
        # print(item) # client -> nodejs-server -> flask_API-base64_img
        data=[]
        for i in item:
            self.count+=1
            im = Image.open(BytesIO(base64.b64decode(i))) # base64 解碼
            im.save('public/inference/pre_inference'+str(self.count)+'.jpg') # 解碼base64後存成實體圖片
            # # base64 to Buffer
            # print(type(item)) # type=str
            # print(type(base64.b64decode(item))) # type=byte
            
            # # Inference
            results = model(im,size=1280) # 
            json_results = results_to_json(results,model)

            print(json_results[0])
            results = np.array(results.xyxy[0]) # result

            # # OpenCV - Draw rectage Image 
            frame = cv2.imread('public/inference/pre_inference'+str(self.count)+'.jpg')

            obj_num1=0
            print(json_results)
            for i in results:
                siz = str(obj_num1)
                print(siz)
                x, y, w, h, cf, nc = i 
                classes_name = classes['names'][int(nc)] # yaml classes
                text = " "+siz+": "+str(classes_name)+": {:.1f}%".format(cf * 1000/2) # text
                # 計算文字長寬和縮放比例，再去畫文字背景匡
                text_wh, text_scale  = cv2.getTextSize(text, self.font, self.font_scale,self.font_line_size) # 輸入的文本字符串, font, fontScale, thickness
                cv2.rectangle(frame, (x, y),(w, h), (0, 255, 0), 4) # Draw bbox rectangle 
                # Draw black-background rectangle tp fill
                cv2.rectangle(frame, (int(x), int(y)), (int(x+text_wh[0]), int(y-50)), (255,255,0,100), self.thickness)
                # write text to image
                # cv2.putText(影像, 文字, 座標, 字型, 大小, 顏色, 線條寬度, 線條種類)
                cv2.putText(frame, text, (int(x), int(y-10)), self.font, self.font_scale, (0, 0, 255),self.font_line_size,cv2.LINE_AA)
                obj_num1+=1
            # # cv2_image to image_base64
            base64_str = cv2.imencode('.jpg',frame)[1]
            base64_str = base64.b64encode(base64_str).decode('ascii')
            json_results.append({"base64":base64_str})
            data.append(json_results)
            
        return data # all inference data

api.add_resource(UploadToModelInference, '/UploadToModelInference')

####################################################################################
loop = asyncio.get_event_loop()
# async def live_inference(websocket,path): # 定義一個協程
#     while True:
#         await websocket.send("123")
#         time.sleep(1)
# VideoStreamModelInference Class
class VideoStreamModelInference(Resource):
    def __init__(self):
        self.name = ""
    def get(self):
        return "get"
    def post(self):
        try:
            asyncio.set_event_loop(loop)
            loop.run_until_complete(
                websockets.serve(self.live, 'localhost', 3050))
            asyncio.get_event_loop().run_forever()
        except Exception as e:
            print(e)
        return "flask API return"

    async def live(self,websocket,path):
        # data=[]
        print("....")
        while True:
            ret, frame = cap.read()
            if ret: # 相機有開啟，就往下執行
                #cv2.namedWindow('img', cv2.WINDOW_NORMAL)  #正常視窗大小
                # Inference 
                results = model(frame, size=320)
                json_results = results_to_json(results,model)
                # Results
                results = np.array(results.xyxy[0]) # 每幀辨識資訊 ， 如果沒有物件會是[]
                if len(json_results[0])>0: # 有偵測到物件就畫框  並socket到nodejs
                    # client.send(str(json_results[0][0]).encode("utf-8"))
                    await websocket.send(str(json_results))
                    # font style
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    for i in results:
                        (x, y, w, h, cf, nc) = i 
                        nc = int(nc)
                        text = str(model.model.names[int(i[5])])+": {:.1f}%".format(cf * 100)
                        cv2.rectangle(frame, (x, y),(w, h), (0, 255, 0), 4)
                        cv2.putText(frame, text, (x, int(y-10)), font, 1, (255, 0, 0),1)
                    #client.send(msg.encode('utf-8'))  #发送一条信息 python3 只接收btye流
                    # data = client.recv(1024) #接收一个信息，并指定接收的大小 为1024字节
                    # print('recv:',data.decode()) #输出我接收的信息
                    # client.close() #關閉連接
                    # base64_str = cv2.imencode('.jpg',frame)[1]
                    # base64_str = base64.b64encode(base64_str).decode('ascii')
                    # json_results.append({"base64":base64_str})
                    # data.append(json_results)
                    # await websocket.send(str(data))

                else:
                    print("沒有物件")
                
    def stop(self):
        print("stop")
        return 1

# asyncio.get_event_loop().run_until_complete(
#     websockets.serve(, 'localhost', 3050))
# asyncio.get_event_loop().run_forever()
'''
run_until_complete讓註冊參數裡的任務並執行，等到任務完成就關閉Event Loop
loop.run_forever() 這個函數一執行，Event Loop就會永遠執行不會被關閉，除非在程式中出現loop.stop()就停止

'''

api.add_resource(VideoStreamModelInference, '/VideoStream')

####################################################################################

if __name__ == '__main__':
    app.run(debug=True)







