from flask import Flask, request
import cv2
import requests
import base64
import json
import time
from infer import *

app = Flask(__name__)
capture = False
url = "rtsp://143.215.56.113:8080/video/h264"
# url = "rtsp://143.215.92.236:8080/video/h264"
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
        if not ret:
            continue
        if ct == 0:
            print("Creating Map", np.shape(frame))
            ret, jpeg = cv2.imencode('.jpg', frame)
            r = requests.post(url="http://34.83.136.245:5000",
                              data=base64.b64encode(jpeg))
            if r.status_code == 200:
                setFrame(frame)
                rjs = None
                try:
                    rjs = r.json()
                except:
                    continue
                getTables(rjs)
                getChairs(rjs)
                ct += 1
            continue
        elif(ct % 20 == 0):
            # frame = resize_mjpeg(frame)
            print("Sending request", np.shape(frame))
            ret, jpeg = cv2.imencode('.jpg', frame)
            r = requests.post(url="http://34.83.136.245:5000",
                              data=base64.b64encode(jpeg))
            if r.status_code == 200:
                setFrame(frame)
                rjs = None
                try:
                    rjs = r.json()
                except:
                    continue
                run(rjs)
        ct += 1
        if ct > 2000000:
            ct = 0
    cap.release()
    cv2.destroyAllWindows()
    return "a"


@app.route('/layout', methods=['GET'])
def getLayout():
    use_case = request.args.get("id")
    return getAppData(use_case)


@app.route('/stop_monitor_stream')
def stop_monitor_stream():
    capture = False


@app.route('/predictedTime')
def predictTime():
    tid = request.args.get("tid")
    table = getDeets(tid)
    if not 'time' in table:
        return ""
    data = {
        "Inputs": {
            "input1":
            [
                {
                    'occupied_for': "1",
                    'num': table['num'],
                    'table_id': tid,
                    'time': table['time'],
                }
            ],
        },
        "GlobalParameters":  {
        }
    }
    body = str.encode(json.dumps(data))
    url = 'https://ussouthcentral.services.azureml.net/workspaces/3de4ce95d35d47828e6e865801b96010/services/d68a728a17264d5685156fea3ae55e64/execute?api-version=2.0&format=swagger'
    api_key = 'abcx=='  # Replace this with the API key for the web service
    headers = {'Content-Type': 'application/json',
               'Authorization': ('Bearer ' + api_key)}
    r = requests.post(url=url,
                      data=body, headers=headers)
    print(r.status_code)
    print('shiz')
    if r.status_code == 200:
        print(r.json())
        return r.json()
    return ""

def resize_mjpeg(frame):
    r = 320.0 / frame.shape[1]
    dim = (320, 200)  # int(frame.shape[0] * r))
    # perform the actual resizing of the image and show it
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    return frame
