const { processFrames, writeBuffer } = require("./process-frames");

var framerate = 0;
var hands = 0;
var fingers = 0;

function setLmcCallbacks(controller, io) {
    controller.on("ready", () => {
        io.emit("status", "LMC is Ready");
        console.log("lmc is ready ... ");
    });
    controller.on("connect", () => {
        io.emit("status", "LMC is Connected");
        console.log("lmc is connected ... ");
    });
    controller.on("disconnect", () => {
        io.emit("status", "LMC is Disconnected");
        console.log("lmc is disconnected! ");
    });
    controller.on("focus", () => {
        io.emit("status", "LMC has Focused");
        console.log("lmc has focused ... ");
    });
    controller.on("blur", () => {
        io.emit("status", "LMC Vision is Blurry. Please Clean the Surface");
        console.log("lmc vision is blurry. please clean the surface ... ");
    });
    controller.on("streamingStarted", () => {
        io.emit("status", "Data Streaming has Started");
        console.log("lmc is streaming data ... ");
        setInterval(() => {
            io.emit("framerate", framerate);
            io.emit("hands", hands);
            io.emit("fingers", fingers);
        }, 100);
    });
    controller.on("streamingStopped", () => {
        io.emit("status", "Data Streaming is Stopped");
        console.log("lmc stopped streaming data ");
    });

    controller.on("frame", (frame) => {
        framerate = frame.currentFrameRate;
        hands = frame.hands.length;
        fingers = frame.fingers.length;
        processFrames(frame);
        // console.log(frame.currentFrameRate);
    });

    controller.connect();
    console.log("waiting for lmc to connect ... ");
}

module.exports = { setLmcCallbacks };
