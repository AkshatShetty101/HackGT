import urllib
from flask import Flask
import sched
import time
s = sched.scheduler(time.time, time.sleep)
app = Flask(__name__)
capture = False


@app.route('/')
def hello_world():
    return 'Hello, World!'


# @app.route('/monitor_stream')
# def monitor_stream():
#     capture = True
#     ct = 0
#     while capture == True:
#         fName = ("local-filename", ct, ".jpg")
#         urllib.urlretrieve("http://143.215.92.236:8080/", fName)
#         ct += 1


# @app.route('/stop_monitor_stream')
# def stop_monitor_stream():
#     capture = False
