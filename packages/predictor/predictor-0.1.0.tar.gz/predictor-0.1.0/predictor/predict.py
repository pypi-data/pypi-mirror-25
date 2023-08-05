"""
Flask API serving as UI backend or standalone API endpoint serving
scikit-learn models up for prediction.  
"""

import argparse
import os
import boto3
import random
import pickle
import traceback
from flask import Flask, request, jsonify

tmpdir = "/tmp"

# Instantiate app and nav bar
app = Flask(__name__)

def load_model(loc):
    """ Load and return pickled model object from S3 or local """

    # If location is in S3, copy to local, then unpickle
    to_delete = False
    if "s3" in loc:
        tmp_loc = "{0}/tmp_file_{1}.obj".format(
            tmpdir, random.randint(1,1000))
        s3 = boto3.client('s3')
        bucket = loc.split("/")[2]
        key = "/".join(loc.split("/")[3:])
        with open(tmp_loc, "wb") as data:
            s3.download_fileobj(bucket, key, data)
        loc = tmp_loc
        to_delete = True
    with open(loc, "rb") as f:
        model = pickle.load(f)
    if to_delete:
        os.remove(tmp_loc)
    return model

# Predictor endpoint
@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    """ Make prediction according to posted data input """

    # Parse input data
    if request.method == "POST":
        input = request.get_json(force=True)
    elif request.method == "GET":
        input = request.args
    input = input.to_dict()

    # Get prediction method
    if input["method"] == "predict":
        method = model.predict
    elif input["method"] == "predict_proba":
        method = model.predict_proba
    else:
        raise ValueError("Unknown prediction method")   

    # Assemble input features
    features = [input[x] for x in model.features] 

    # Attempt prediction
    try:
        prediction = method([features])
        status = "SUCCESS"
        tb = None
    except Exception as e:
        prediction = None
        status = "FAILURE"
        tb = traceback.format_exc()

    output = [
        {
         'input': input, 
         'prediction': [list(x) for x in prediction],
         'status': status,
         'traceback': tb
        }
    ]
    return jsonify(results=output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-loc',
                        dest='model_loc',
                        default=None, 
                        help='location of pickled model object')
    parser.add_argument('--port',
                        dest='port',
                        default='8080',
                        help='port to serve application')
    parser.add_argument('--host',
                        dest='host',
                        default='0.0.0.0',
                        help='host to serve application')
    args = parser.parse_args()
    if not args.model_loc:
        raise Exception("Please supply valid model location argument")
    model = load_model(args.model_loc)
    app.run(
        host=args.host,
        port=int(args.port)
    )

