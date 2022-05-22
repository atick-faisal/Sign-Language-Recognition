import time
import joblib
import socketio
import pandas as pd

from threading import Thread, Timer
from scipy.stats import mode

FEATURE_NAMES = [
    "time",
    "rpx",
    "rpy",
    "rpz",
    "lpx",
    "lpy",
    "lpz",
    "rf0x",
    "rf0y",
    "rf0z",
    "rf1x",
    "rf1y",
    "rf1z",
    "rf2x",
    "rf2y",
    "rf2z",
    "rf3x",
    "rf3y",
    "rf3z",
    "rf4x",
    "rf4y",
    "rf4z",
    "lf0x",
    "lf0y",
    "lf0z",
    "lf1x",
    "lf1y",
    "lf1z",
    "lf2x",
    "lf2y",
    "lf2z",
    "lf3x",
    "lf3y",
    "lf3z",
    "lf4x",
    "lf4y",
    "lf4z",
]

GESTURES = ["One", "Two"]
inference_started = False

sio = socketio.Client()

buffer = pd.DataFrame([], columns=FEATURE_NAMES)
features = pd.DataFrame()


model = joblib.load("../model/knn-clf.joblib")


def make_prediction():
    global inference_started
    features["drf1"] = ((buffer["rf1x"] - buffer["rpx"]).pow(2) +
                        (buffer["rf1y"] - buffer["rpy"]).pow(2) +
                        (buffer["rf1z"] - buffer["rpz"]).pow(2)).pow(0.5)
    features["drf2"] = ((buffer["rf2x"] - buffer["rpx"]).pow(2) +
                        (buffer["rf2y"] - buffer["rpy"]).pow(2) +
                        (buffer["rf2z"] - buffer["rpz"]).pow(2)).pow(0.5)
    features.dropna(inplace=True)
    X = features.to_numpy()
    y_pred = model.predict(X)
    prediction = mode(y_pred)[0][0]
    print(GESTURES[prediction], buffer.shape[0])
    buffer.drop(buffer.index, inplace=True)
    inference_started = False


@sio.event
def connect():
    print('connection established')


@sio.on("inference")
def my_message(data):
    global inference_started
    # df = pd.DataFrame([[float(val) for val in data.split(",")]],
    #                   columns=FEATURE_NAMES)

    buffer.loc[buffer.shape[0]] = [float(val) for val in data.split(",")]
    if not inference_started:
        inference_started = True
        print("predicting ... ", end="")
        inference = Timer(2.0, make_prediction)
        inference.start()

    # sio.emit('my response', {'response': 'my response'})


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('ws://localhost:8080')
sio.wait()
