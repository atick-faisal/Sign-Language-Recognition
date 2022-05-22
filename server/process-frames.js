const fs = require("fs");
const path = require("path");
const dfd = require("danfojs-node");
const config = require("../config/config");

let buffer = config.FEATURE_NAMES;
let dataBuffer = new dfd.DataFrame(
    [Array(config.FEATURE_NAMES.length).fill(0)],
    {
        columns: config.FEATURE_NAMES,
    }
);

let timestamp = 0;
let rightPalmPosition = new Array(3).fill(0);
let leftPalmPosition = new Array(3).fill(0);
let rightHandFingerTips = new Array(15).fill(0);
let leftHandFingerTips = new Array(15).fill(0);
let handFlag = true; // rightHand -> true leftHand -> false

function initialize() {
    rightPalmPosition.fill(0);
    leftPalmPosition.fill(0);
    rightHandFingerTips.fill(0);
    leftHandFingerTips.fill(0);
}

function processFrames(frame, io) {
    timestamp = frame.timestamp;
    frame.hands.forEach((hand) => {
        if (hand.type === config.HAND_TYPE_RIGHT) {
            rightPalmPosition[0] = hand.palmPosition[0];
            rightPalmPosition[1] = hand.palmPosition[1];
            rightPalmPosition[2] = hand.palmPosition[2];
            handFlag = true;
        } else {
            leftPalmPosition[0] = hand.palmPosition[0];
            leftPalmPosition[1] = hand.palmPosition[1];
            leftPalmPosition[2] = hand.palmPosition[2];
            // leftPalmPosition = [...hand.palmVelocity];
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

    let newData = [timestamp].concat(
        rightPalmPosition,
        leftPalmPosition,
        rightHandFingerTips,
        leftHandFingerTips
    );

    dataBuffer = dataBuffer.append([newData], [dataBuffer.shape[0]]);
    if (frame.hands.length > 0) {
        console.log("sending");
        io.emit("inference", newData.join());
    }

    // buffer +=
    //     timestamp.toString() +
    //     "," +
    //     rightPalmPosition.join() +
    //     "," +
    //     leftPalmPosition.join() +
    //     // "," +
    //     // rightHandFingerTips.join() +
    //     // "," +
    //     // leftHandFingerTips.join() +
    //     "\n";
}

function writeBuffer(subjectId, gesture) {
    let timestamp = new Date().getTime();
    let saveDir = path.join("..", "data", "dataset", subjectId, gesture);
    let filePath = path.join(saveDir, `${timestamp}.csv`);
    if (!fs.existsSync(saveDir)) {
        fs.mkdirSync(saveDir, { recursive: true });
    }
    dfd.toCSV(dataBuffer, { filePath: filePath });
    dataBuffer = new dfd.DataFrame(
        [Array(config.FEATURE_NAMES.length).fill(0)],
        {
            columns: config.FEATURE_NAMES,
        }
    );
    console.log(`recording saved: ${filePath}`);

    // fs.writeFile(filePath, buffer, (e) => {
    //     if (e) throw e;
    //     console.log("file written to disk!");
    //     buffer = config.FEATURE_NAMES;
    //     initialize();
    // });
}

module.exports = { processFrames, writeBuffer };
