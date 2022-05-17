const leapjs = require("leapjs");
const controller = new leapjs.Controller();
const fs = require("fs");

controller.on("ready", function () {
    console.log("ready");
});
controller.on("connect", function () {
    console.log("connect");
});
controller.on("disconnect", function () {
    console.log("disconnect");
});
controller.on("focus", function () {
    console.log("focus");
});
controller.on("blur", function () {
    console.log("blur");
});
controller.on("deviceConnected", function () {
    console.log("deviceConnected");
});
controller.on("deviceDisconnected", function () {
    console.log("deviceDisconnected");
});

var frameCount = 0;
var buffer = "";
controller.on("frame", function (frame) {
    // console.log(frame.currentFrameRate);
    frame.hands.map((hand) => {
        buffer += hand.palmPosition.join() + "\n";
        console.log(hand.direction);
    });
    frameCount++;
});

// setInterval(function () {
//     var time = frameCount / 2;
//     console.log("received " + frameCount + " frames @ " + time + "fps");
//     frameCount = 0;
// }, 2000);

setTimeout(() => {
    fs.appendFile("../data/dataset/data.csv", buffer, (e) => {
        if (e) throw e;
        console.log("saved file!");
    });
}, 5000);

controller.connect();
console.log("\nWaiting for device to connect...");
