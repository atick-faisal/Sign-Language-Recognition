INFERENCE_TIME = 3.0  # ... Segment duration
HOLD_TIME = 2.0  # ... Time before next prediction session
SEGMENT_LEN = 150
IMG_LEN = 160  # 1/9 of the 224x224 image
N_CHANNELS = 3
LEARNING_RATE = 0.0003
BATCH_SIZE = 32
MAX_EPOCHS = 300
PATIENCE = 30
LINE_WIDTH = 2
PROJECTION_LANDMARKS = ["rp", "rf0", "rf1"]
AUGMENTATION_LEVELS = [13, 11, 9, 7, 5, 0]
INFERENCE_FEATURES = [
    "rpx",
    "rpy",
    "rpz",
    "rf0x",
    "rf0y",
    "rf0z",
    "rf1x",
    "rf1y",
    "rf1z"
]
MODEL_PREDICTION = "dev.atick.slr.model.prediction"
FRAME_EVENT = "dev.atick.slr.frame"
GESTURES = ["Good", "Bad", "Fine", "Hello", "Yes", "Deaf", "Me",
            "No", "Please", "Sorry", "Thank You", "You", "Hungry", "Goodbye"]
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

# ... Scaling distance features
DIST_FEATURES = ["drf0x", "drf0y", "drf0z", "drf1x", "drf1y", "drf1z"]
SCALER_MIN = [-108.80884021,  -72.35677707,  -75.40455647, -105.06504236,
              -91.38009326, -110.18809635]
SCALER_RANGE = [209.08497391, 178.58391672, 169.26662137, 174.0735184,
                194.11552266, 166.07192772]
