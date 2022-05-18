const { processFrames, writeBuffer } = require("./process-frames");

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
        setTimeout(() => {
            writeBuffer();
        }, 5000);
    });
    controller.on("streamingStopped", () => {
        io.emit("status", "Data Streaming is Stopped");
        console.log("lmc stopped streaming data ");
    });

    controller.on("frame", (frame) => {
        io.emit("framerate", `Frame Rate: ${frame.currentFrameRate}`);
        processFrames(frame);
        // console.log(frame.currentFrameRate);
    });

    controller.connect();
    console.log("waiting for lmc to connect ... ");
}

module.exports = { setLmcCallbacks };
