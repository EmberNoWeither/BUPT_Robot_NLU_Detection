import os
import cv2
import time
import argparse
import torch
import warnings
import numpy as np
import time
import base64

from inference import *

def decode_image(image):
    image = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_ANYCOLOR)
    return image

    
import flask
app = flask.Flask(__name__)
@app.route("/xuni/inference", methods=["POST"])
def inference_a_img():
    thisid = 0
    data = flask.request.get_json(force=True)
    #print(data)
    action = data['action']
    print('action is {}'.format(action))
    root_dir = './'
    log_dir = '{}/train/{}_run'.format(root_dir, thisid)
    if action == 'initialize net':
        #thisid=str(flask.request.files.get("thisid").read(), 'utf-8')
        thisid = data['thisid']
        weight_path = os.path.join(log_dir, 'weights/best_jiaoyu.pt')
        global net
        net = net_init(weight_path, 'cpu')
        print('{} loading'.format(weight_path))
        try:
            assert net
            astr = 'net initialized'
        except:
            print('training did not end properly')
            return {'code':'-1'}
        print('{} loaded'.format(weight_path))
        return {'code':'0'}
    elif action == 'inference':
        try:
            assert net
        except:
            return {'code':'-1'}
        time0=time.time()
        #image=flask.request.files.get("image").read()
        image=np.asarray(data['image'], dtype=np.uint8)
        ori_im=decode_image(image)
        time1 = time.time()
        print('start inference')
        results = inference(net, ori_im, 'cpu')
        time2 = time.time()
        print('inference done')
        results['request time'] = time1 - time0
        return results
    
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='deployment relatives')
    parser.add_argument('--aip', type=str, default='0.0.0.0',
                        help='deployment ip')
    parser.add_argument('--aport', type=int, default=4003, help='deployment ip')
    args = parser.parse_args()
    aip = args.aip
    aport = args.aport
    app.run(host=aip, port=aport)
