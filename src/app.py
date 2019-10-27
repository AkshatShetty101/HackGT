from flask import Flask, request
import cv2
import requests
import base64
import json
import time
from infer import *

app = Flask(__name__)
capture = False
# url = "rtsp://143.215.56.113:8080/video/h264"
url = "rtsp://143.215.92.236:8080/video/h264"
# url = "rtsp://143.215.116.154:8080/video/h264"
@app.route('/')
def hello_world():
    return('Hello, World!')


@app.route('/monitor_stream')
def monitor_stream():
    capture = True
    cap = cv2.VideoCapture(url)
    # cap = cv2.VideoCapture('./inp.mp4')
    ct = 0
    while capture == True:
        # time.sleep(1)
        ret, frame = cap.read()
        if ct == 0:
            print("Creating Map", np.shape(frame))
            ret, jpeg = cv2.imencode('.jpg', frame)
            r = requests.post(url="http://34.83.136.245:5000",
                              data=base64.b64encode(jpeg))
            setFrame(frame)
            getTables(r.json())
            getChairs(r.json())
            ct+=1
            continue
        if(ct % 20 == 0):
            # frame = resize_mjpeg(frame)
            print("Sending request", np.shape(frame))
            ret, jpeg = cv2.imencode('.jpg', frame)
            r = requests.post(url="http://34.83.136.245:5000",
                              data=base64.b64encode(jpeg))
            setFrame(frame)
            run(r.json())
        ct += 1
        if ct > 2000000:
            ct = 0
    cap.release()
    cv2.destroyAllWindows()

@app.route('/layout', methods=['GET'])
def getLayout():
    use_case = request.args.get("id")
    return getAppData(use_case)

@app.route('/stop_monitor_stream')
def stop_monitor_stream():
    capture = False

def resize_mjpeg(frame):
    r = 320.0 / frame.shape[1]
    dim = (320, 200)  # int(frame.shape[0] * r))
    # perform the actual resizing of the image and show it
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    return frame
