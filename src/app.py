import requests
import shutil
from flask import Flask
app = Flask(__name__)
capture = False
url = "http://143.215.92.236:8080/"


@app.route('/')
def hello_world():
    return('Hello, World!')


@app.route('/monitor_stream')
def monitor_stream():
    capture = True
    ct = 12
    filePath = "./local-filename{}.jpg".format(ct)
    print(filePath, url)
    response = requests.get(url)
    print("response")
    if response.status_code == 200:
        print(response.content)
        with open(filePath, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
    return 100


@app.route('/stop_monitor_stream')
def stop_monitor_stream():
    capture = False
