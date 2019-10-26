from flask import Flask
from flask import request
import tools.infer_simple as ml
import glob
import cv2
import numpy as np
import base64
import json

app = Flask(__name__)
args = ["--cfg", "configs/12_2017_baselines/e2e_mask_rcnn_R-101-FPN_2x.yaml","--output-dir", "/tmp/detectron-visualizations", "--wts", "https://dl.fbaipublicfiles.com/detectron/35861858/12_2017_baselines/e2e_mask_rcnn_R-101-FPN_2x.yaml.02_32_51.SgT4y1cO/output/train/coco_2014_train:coco_2014_valminusminival/generalized_rcnn/model_final.pkl"]
ml.init(args)

@app.route('/', methods=['POST', 'GET'])
def main():
    # path = "./demo/akarshit1.jpg"
    # data = glob.iglob(path)
    # im = cv2.imread(path)
    js = request.get_data()
    jpg_original = base64.b64decode(js)
    
    nparr = np.fromstring(jpg_original, np.uint8)
    im = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return json.dumps(ml.predict(im))

