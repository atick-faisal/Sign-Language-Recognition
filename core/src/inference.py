import os
import config
import joblib
import socketio
import numpy as np
import pandas as pd

from threading import Timer
from scipy.stats import mode
from scipy.signal import resample
from tensorflow.keras.models import load_model

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# ... global state
inference_started = False

sio = socketio.Client()
# model = joblib.load("../model/knn-clf.joblib")
model = load_model("../model/stack_cnn")
scaler = joblib.load("../model/scaler.joblib")
buffer = pd.DataFrame([], columns=config.FEATURE_NAMES)


def reset_inference():
    global inference_started
    buffer.drop(buffer.index, inplace=True)
    inference_started = False


def make_prediction():
    features = pd.DataFrame()
    features[
        ["rpx", "rpz", "lpx", "lpz"]
    ] = buffer[["rpx", "rpz", "lpx", "lpz"]]
    features["drf1"] = ((buffer["rf1x"] - buffer["rpx"]).pow(2) +
                        # (buffer["rf1y"] - buffer["rpy"]).pow(2) +
                        (buffer["rf1z"] - buffer["rpz"]).pow(2)).pow(0.5)

    features["drf2"] = ((buffer["rf2x"] - buffer["rpx"]).pow(2) +
                        # (buffer["rf2y"] - buffer["rpy"]).pow(2) +
                        (buffer["rf2z"] - buffer["rpz"]).pow(2)).pow(0.5)

    features.dropna(inplace=True)

    X = features.to_numpy()
    X = resample(X, 512, axis=0)
    X = scaler.transform(X)
    print(X.shape)
    X = X.reshape(-1, 512, 6)
    # y_pred = model.predict(X)
    y_pred = np.argmax(model.predict(np.split(X, 6, axis=-1))[0])
    # prediction = config.GESTURES[mode(y_pred)[0][0]]
    prediction = config.GESTURES[y_pred]

    sio.emit(config.MODEL_PREDICTION, prediction)
    print(prediction, buffer.shape[0])

    cleanup = Timer(2.0, reset_inference)
    cleanup.start()


@sio.event
def connect():
    print('connection established')


@sio.on(config.FRAME_EVENT)
def my_message(data):
    global inference_started

    buffer.loc[buffer.shape[0]] = [float(val) for val in data.split(",")]
    if not inference_started:
        inference_started = True

        print("predicting ... ", end="")
        sio.emit(config.MODEL_PREDICTION, "Predicting ... ")

        inference = Timer(config.INFERENCE_TIME, make_prediction)
        inference.start()


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('ws://localhost:8080')
sio.wait()
