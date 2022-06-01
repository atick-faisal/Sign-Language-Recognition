const fs = require("fs");

const config = {
    PORT: 8080,
    MESSAGE_EVENT: "dev.atick.slr.message",
    RECORD_EVENT: "dev.atick.slr.record",
    DISCARD_EVENT: "dev.atick.slr.discard",
    STATUS_EVENT: "dev.atick.slr.status",
    FRAMERATE_EVENT: "dev.atick.slr.framerate",
    HANDS_EVENT: "dev.atick.slr.hands",
    FINGERS_EVENT: "dev.atick.slr.fingers",
    MODEL_PREDICTION: "dev.atick.slr.model.prediction",
    PREDICTION_EVENT: "dev.atick.slr.prediction",
    STATUS_UPDATE_INT: 100,
    HAND_TYPE_RIGHT: "right",
    HAND_TYPE_LEFT: "left",
    SOCKET_CONNECTION: "connection",
    LMC_EVENT_READY: "ready",
    LMC_EVENT_CONNECT: "connect",
    LMC_EVENT_DISCONNECT: "disconnect",
    LMC_EVENT_STREAMING_STARTED: "streamingStarted",
    LMC_EVENT_STREAMING_STOPPED: "streamingStopped",
    LMC_EVENT_BLUR: "blur",
    LMC_EVENT_FOCUS: "focus",
    LMC_EVENT_FRAME: "frame",
    PROGRESS_UPDATE_INT: 100,
    PREPARATION_DURATION: 3000,
    RECORDING_DURATION: 5000,

    FEATURE_NAMES: [
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
    ],
};

module.exports = function updateConfig(path) {
    try {
        let configJson = JSON.stringify(config);
        fs.writeFileSync(path, configJson);
    } catch (e) {
        console.log("error updating config!");
    }
};
