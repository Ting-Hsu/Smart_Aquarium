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

app = Flask(__name__)
api = Api(app)

model = torch.hub.load('ultralytics/yolov5', 'custom', path_or_model='best.pt', autoshape=True)  # for file/URI/PIL/cv2/np inputs and NMS
model.conf = 0.10  # confidence threshold (0-1)
model.iou = 0.40  # NMS IoU threshold (0-1)

# camera = cv2.VideoCapture(0)  # use 0 for web camera
camera = cv2.VideoCapture("http://192.168.43.181:8080/?action=stream")  # use 0 for web camera
# camera = cv2.VideoCapture("http://127.0.0.1:5000/live_video")

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
# @app.route("/detect",methods=['POST'])
# def gen_frames():  # generate frame by frame from camera
#     model = torch.hub.load('ultralytics/yolov5', "yolov5s", pretrained=True)
#     while True:
#         # Capture frame-by-frame
#         success, frame = camera.read()  # read the camera frame
#         if not success:
#             break
#         else:
#             results = model(frame, size=160)
#             json_results = results_to_json(results,model)
#                     # Results
#             results = np.array(results.xyxy[0]) # 每幀辨識資訊 ， 如果沒有物件會是[]
#             print(json_results)
#             #return {"data":json_results} # not is return 
#             # font style
#             # font = cv2.FONT_HERSHEY_COMPLEX_SMALL
#             # for i in results:
#             #     (x, y, w, h, cf, nc) = i 
#             #     nc = int(nc)
#             #     text = str(nc)+": {:.1f}%".format(cf * 100)
#             #     cv2.rectangle(frame, (x, y),(w, h), (0, 255, 0), 4)
#             #     cv2.putText(frame, text, (x, y), font, 5, (0, 255, 0  ),cv2.LINE_AA, 1)
#             # # print(json_results)
#             # ret, buffer = cv2.imencode('.jpg', frame)
#             # frame = buffer.tobytes()
#             # yield (b'--frame\r\n'
#             #         b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

#     #cv2.destroyAllWindows()

socket_data = []
def gen_frames1():  # generate frame by frame from camera
    (W, H) = (None, None) # 圖像長寬初始化
    font = cv2.FONT_HERSHEY_SIMPLEX # 字體樣式
    font_scale = 0.8 # 縮放比例
    font_line_size = 1 # 線粗細
    thickness = cv2.FILLED # 填滿(-1) 
    while True:
        success, frame = camera.read()  # read the camera frame
        # frame = cv2.resize(frame, (640, 360))
        if W is None or H is None:
            (H, W) = frame.shape[:2]
        if not success: # 相機沒有開啟
            break
        else: # 讀取到相機
            results = model(frame,size=640) # 辨識
            json_results = results_to_json(results,model) # 將辨識結果轉成json格式
            # Results
            # results = np.array(results.xyxy[0]) # 每幀辨識資訊 ， 如果沒有物件會是[]
            # await websocket.send(str(json_results))
            ################################################################## 方法一
            obj_num1=0
            if len(json_results[0])>0: # 每張frame偵測到有幾個物件，大於0畫框
                for i in json_results[0]: # 將一張圖上的每個物件畫框
                    cs, cn, bbox, cf = i['class'], i['class_name'], i['normalized_box'], i['confidence']
                    text = ""+ str(cn)+": {:.1f}%".format(cf * 100) # 偵測到的物件標籤文字
                    box = bbox[0:4] * np.array([W, H, W, H]) # 把 bbox 還原成實際大小
                    (centerX, centerY, width, height) = box.astype("int") # 然後把 bbox 轉成整數
                    # print([centerX,centerY,width, height])
                    # 要先計算文字長寬和縮放比例，再去畫文字的背景框
                    text_wh, text_scale  = cv2.getTextSize(text, font, font_scale,font_line_size) # 要輸入的字符串, font, fontScale, thickness
                    # 畫物件框線
                    cv2.rectangle(frame, (centerX, centerY),(width ,height), (0, 255, 0), 4) 
                    # 畫標籤背景框-填滿
                    cv2.rectangle(frame, (centerX, centerY), (centerX+text_wh[0], centerY-50), (255,255,0,100), thickness)
                    # cv2.putText(影像, 文字, 座標, 字型, 大小, 顏色, 線條寬度, 線條種類)
                    cv2.putText(frame, text, (centerX, centerY-10), font, font_scale, (0, 0, 255),font_line_size,cv2.LINE_AA)
                # 以下利用cv2影像解碼功能，讀取每幀圖像轉成binary印在網頁上
                ret, buffer = cv2.imencode('.jpg', frame) 
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                # 以下利用cv2影像解碼功能，讀取每幀圖像轉成binary印在網頁上
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


            ################################################################## 方法二



            # if len(json_results[0])>0:
            #     for i in results:
            #         siz = str(obj_num1)
            #         # print(siz)
            #         x, y, w, h, cf, nc = i 
            #         # classes_name = classes['names'][int(nc)] # yaml classes
            #         text = " "+siz+": "+ json_results[0][0]['class_name']+": {:.1f}%".format(cf * 100) # text
            #         # 先計算文字長寬和縮放比例，再去畫文字背景匡
            #         text_wh, text_scale  = cv2.getTextSize(text, font, font_scale,font_line_size) # 輸入的文本字符串, font, fontScale, thickness
            #         cv2.rectangle(frame, (x, y),(w, h), (0, 255, 0), 4) # Draw bbox rectangle 
            #         # Draw black-background rectangle tp fill
            #         cv2.rectangle(frame, (int(x), int(y)), (int(x+text_wh[0]), int(y-50)), (255,255,0,100), thickness)
            #         # write text to image
            #         # cv2.putText(影像, 文字, 座標, 字型, 大小, 顏色, 線條寬度, 線條種類)
            #         cv2.putText(frame,text, (int(x), int(y-10)), font, font_scale, (0, 0, 255),font_line_size,cv2.LINE_AA)
            #         obj_num1+=1

            #     # for i in results:
            #     #     (x, y, w, h, cf, nc) = i 
            #     #     nc = int(nc)
            #     #     text = str(nc)+": {:.1f}%".format(cf * 100)
            #     #     cv2.rectangle(frame, (x, y),(w, h), (255, 0, 0), 4)
            #     #     cv2.putText(frame, text, (x, y), font, 5, (0, 255, 0  ),cv2.LINE_AA, 1)
            #     ret, buffer = cv2.imencode('.jpg', frame) # 利用cv2影像解碼功能，讀取每幀圖像轉乘binary印在網頁上
            #     frame = buffer.tobytes()
            #     yield (b'--frame\r\n'
            #             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            # else:
            #     ret, buffer = cv2.imencode('.jpg', frame) # 利用cv2影像解碼功能，讀取每幀圖像轉乘binary印在網頁上
            #     frame = buffer.tobytes()
            #     yield (b'--frame\r\n'
            #             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cv2.release()
    cv2.destroyAllWindows()


@app.route('/live_video')
def live_video():
    # loop = asyncio.get_event_loop()
    # asyncio.set_event_loop(loop)
    # async def echo(websocket, path):
    #         await websocket.send("123")
    # start_server = websockets.serve(echo, "localhost", 8765)
    # asyncio.get_event_loop().run_until_complete(start_server)
    # asyncio.get_event_loop().run_forever()
    # 影像串流網址 打印在img src tag上
    return Response(gen_frames1(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')




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
        for i in item: # 有幾張圖
            self.count+=1
            im = Image.open(BytesIO(base64.b64decode(i))) # 圖片 base64 解碼
            im.save('../public/inference/pre_inference'+str(self.count)+'.jpg') # 解碼base64後存成實體圖片
            # # base64 to Buffer
            # print(type(item)) # type=str
            # print(type(base64.b64decode(item))) # type=byte
            # # Inference
            results = model(im,size=640) # 
            json_results = results_to_json(results,model)
            print(json_results[0])
            results = np.array(results.xyxy[0]) # result
            # # OpenCV - Draw rectage Image 
            frame = cv2.imread('../public/inference/pre_inference'+str(self.count)+'.jpg')
            obj_num1=0
            for i in results:
                siz = str(obj_num1)
                print(siz)
                x, y, w, h, cf, nc = i 
                classes_name = classes['names'][int(nc)] # yaml classes
                text = " "+siz+": "+str(classes_name)+": {:.1f}%".format(cf * 100) # text
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
if __name__ == '__main__':
    app.run(debug=True)
# 羅計廠牌Camera的異常
# [mjpeg @ 0x7fc1521ab200] unable to decode APP fields: Invalid data found when processing input















