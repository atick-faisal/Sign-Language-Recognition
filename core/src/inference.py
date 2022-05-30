import config
import joblib
import socketio
import pandas as pd

from threading import Timer
from scipy.stats import mode

# ... global state
inference_started = False

sio = socketio.Client()
model = joblib.load("../model/knn-clf.joblib")
buffer = pd.DataFrame([], columns=config.FEATURE_NAMES)
features = pd.DataFrame()


def reset_inference():
    global inference_started
    buffer.drop(buffer.index, inplace=True)
    inference_started = False


def make_prediction():
    features["drf1"] = ((buffer["rf1x"] - buffer["rpx"]).pow(2) +
                        (buffer["rf1y"] - buffer["rpy"]).pow(2) +
                        (buffer["rf1z"] - buffer["rpz"]).pow(2)).pow(0.5)

    features["drf2"] = ((buffer["rf2x"] - buffer["rpx"]).pow(2) +
                        (buffer["rf2y"] - buffer["rpy"]).pow(2) +
                        (buffer["rf2z"] - buffer["rpz"]).pow(2)).pow(0.5)

    features.dropna(inplace=True)

    X = features.to_numpy()
    y_pred = model.predict(X)
    prediction = config.GESTURES[mode(y_pred)[0][0]]

    sio.emit(config.MODEL_PREDICTION, prediction)
    print(prediction, buffer.shape[0])

    cleanup = Timer(2.0, reset_inference)
    cleanup.start()


@sio.event
def connect():
    print('connection established')


@sio.on("inference")
def my_message(data):
    global inference_started

    buffer.loc[buffer.shape[0]] = [float(val) for val in data.split(",")]
    if not inference_started:
        inference_started = True

        print("predicting ... ", end="")
        sio.emit(config.MODEL_PREDICTION, "Predicting ... ")

        inference = Timer(2.0, make_prediction)
        inference.start()


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('ws://localhost:8080')
sio.wait()
