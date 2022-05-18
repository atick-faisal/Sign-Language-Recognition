const { processFrames, writeBuffer } = require("./process-frames");

function setLmcCallbacks(controller) {
    controller.on("ready", () => {
        console.log("lmc is ready ... ");
    });
    controller.on("connect", () => {
        console.log("lmc is connected ... ");
    });
    controller.on("disconnect", () => {
        console.log("lmc is disconnected! ");
    });
    controller.on("focus", () => {
        console.log("lmc has focused ... ");
    });
    controller.on("blur", () => {
        console.log("lmc vision is blurry. please clean the surface ... ");
    });
    controller.on("streamingStarted", () => {
        console.log("lmc is streaming data ... ");
        setTimeout(() => {
            writeBuffer();
        }, 5000);
    });
    controller.on("streamingStopped", () => {
        console.log("lmc stopped streaming data ");
    });

    controller.on("frame", (frame) => {
        processFrames(frame);
        // console.log(frame.currentFrameRate);
    });

    controller.connect();
    console.log("waiting for lmc to connect ... ");
}

module.exports = { setLmcCallbacks };
