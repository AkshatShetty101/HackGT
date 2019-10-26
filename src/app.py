from flask import Flask
import cv2

app = Flask(__name__)
capture = False
url = "rtsp://143.215.92.236:8080/video/h264"


@app.route('/')
def hello_world():
    return('Hello, World!')


@app.route('/monitor_stream')
def monitor_stream():
    capture = True
    cap = cv2.VideoCapture(url)
    while capture == True:
        ret, frame = cap.read()
        frame = resize_mjpeg(frame)
        
        
    cap.release()
    cv2.destroyAllWindows()


@app.route('/stop_monitor_stream')
def stop_monitor_stream():
    capture = False

def resize_mjpeg(frame):
    r = 320.0 / frame.shape[1]
    dim = (320, 200)#int(frame.shape[0] * r))
    # perform the actual resizing of the image and show it
    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)    
    return frame  
