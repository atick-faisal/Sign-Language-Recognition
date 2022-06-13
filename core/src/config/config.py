INFERENCE_TIME = 3.0  # ... Segment duration
HOLD_TIME = 2.0  # ... Time before next prediction session
SEGMENT_LEN = 256
IMG_LEN = 75  # 1/9 of the 224x224 image
LEARNING_RATE = 0.001
INFERENCE_FEATURES = ["rpx", "rpy", "rpz", "drf0x",
                      "drf0y", "drf0z", "drf1x", "drf1y", "drf1z"]
MODEL_PREDICTION = "dev.atick.slr.model.prediction"
FRAME_EVENT = "dev.atick.slr.frame"
GESTURES = ["Good", "Bad", "Deaf", "Fine", "Hello", "Yes",
            "No", "Please", "Sorry", "Thank You", "Me", "You", "Hungry", "Goodbye"]
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
