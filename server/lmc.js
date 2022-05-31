const config = require("../config/config");
const { processFrames, writeBuffer } = require("./process-frames");

let framerate = 0;
let hands = 0;
let fingers = 0;
let isRecording = false;

function startRecording(subjectId, gesture) {
    isRecording = true;
    setTimeout(() => {
        isRecording = false;
        writeBuffer(subjectId, gesture);
    }, config.RECORDING_DURATION);
}

function setLmcCallbacks(controller, io) {
    controller.on(config.LMC_EVENT_READY, () => {
        io.emit(config.STATUS_EVENT, "LMC is Ready");
        console.log("lmc is ready ... ");
    });
    controller.on(config.LMC_EVENT_CONNECT, () => {
        io.emit(config.STATUS_EVENT, "LMC is Connected");
        console.log("lmc is connected ... ");
    });
    controller.on(config.LMC_EVENT_DISCONNECT, () => {
        io.emit(config.STATUS_EVENT, "LMC is Disconnected");
        console.log("lmc is disconnected! ");
    });
    controller.on(config.LMC_EVENT_FOCUS, () => {
        io.emit(config.STATUS_EVENT, "LMC has Focused");
        console.log("lmc has focused ... ");
    });
    controller.on(config.LMC_EVENT_BLUR, () => {
        io.emit(
            config.STATUS_EVENT,
            "LMC Vision is Blurry. Please Clean the Surface"
        );
        console.log("lmc vision is blurry. please clean the surface ... ");
    });
    controller.on(config.LMC_EVENT_STREAMING_STARTED, () => {
        io.emit(config.STATUS_EVENT, "Data Streaming has Started");
        console.log("lmc is streaming data ... ");
        setInterval(() => {
            io.emit(config.FRAMERATE_EVENT, framerate);
            io.emit(config.HANDS_EVENT, hands);
            io.emit(config.FINGERS_EVENT, fingers);
        }, config.STATUS_UPDATE_INT);
    });
    controller.on(config.LMC_EVENT_STREAMING_STOPPED, () => {
        io.emit(config.STATUS_EVENT, "Data Streaming is Stopped");
        console.log("lmc stopped streaming data ");
    });

    controller.on(config.LMC_EVENT_FRAME, (frame) => {
        framerate = frame.currentFrameRate;
        hands = frame.hands.length;
        fingers = frame.fingers.length;
        processFrames(frame, io, isRecording);
    });

    controller.connect();
    console.log("waiting for lmc to connect ... ");
}

module.exports = { setLmcCallbacks, startRecording };
