const fs = require("fs");
const path = require("path");

var buffer =
    "time,rpx,rpy,rpz,lpx,lpy,lpx,rf0x,rf0y,rf0z," +
    "rf1x,rf1y,rf1z,rf2x,rf2y,rf2z,rf3x,rf3y,rf3z,rf4x,rf4y,rf4z," +
    "lf0x,lf0y,lf0z,lf1x,lf1y,lf1z,lf2x,lf2y,lf2z,lf3x,lf3y,lf3z," +
    "lf4x,lf4y,lf4z\n";

var timestamp = 0;
var rightPalmPosition = new Array(3).fill(0);
var leftPalmPosition = new Array(3).fill(0);
var rightHandFingerTips = new Array(15).fill(0);
var leftHandFingerTips = new Array(15).fill(0);
var handFlag = true; // rightHand -> true leftHand -> false

function processFrames(frame) {
    timestamp = frame.timestamp;
    frame.hands.forEach((hand) => {
        if (hand.type === "right") {
            rightPalmPosition = [...hand.palmPosition];
            handFlag = true;
        } else {
            leftPalmPosition = [...hand.palmPosition];
            handFlag = false;
        }
    });
    frame.fingers.forEach((finger) => {
        if (handFlag) {
            rightHandFingerTips[finger.type * 3] = finger.tipPosition[0];
            rightHandFingerTips[finger.type * 3 + 1] = finger.tipPosition[1];
            rightHandFingerTips[finger.type * 3 + 2] = finger.tipPosition[2];
        } else {
            leftHandFingerTips[finger.type * 3] = finger.tipPosition[0];
            leftHandFingerTips[finger.type * 3 + 1] = finger.tipPosition[1];
            leftHandFingerTips[finger.type * 3 + 2] = finger.tipPosition[2];
        }
    });

    buffer +=
        timestamp.toString() +
        "," +
        rightPalmPosition.join() +
        "," +
        leftPalmPosition.join() +
        "," +
        rightHandFingerTips.join() +
        "," +
        leftHandFingerTips.join() +
        "\n";
}

function writeBuffer(subjectId, gesture) {
    let timestamp = new Date().getTime();
    let saveDir = path.join("..", "data", "dataset", subjectId, gesture);
    let filePath = path.join(saveDir, `${timestamp}.csv`);
    if (!fs.existsSync(saveDir)) {
        fs.mkdirSync(saveDir, { recursive: true });
    }
    fs.writeFile(filePath, buffer, (e) => {
        if (e) throw e;
        console.log("file written to disk!");
    });
}

module.exports = { processFrames, writeBuffer };
