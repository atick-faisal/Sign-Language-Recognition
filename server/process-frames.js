const fs = require("fs");
const path = require("path");
const dfd = require("danfojs-node");
const config = require("../config/config");

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
let filename = "unnamed";

function processFrames(frame, io, isRecording) {
    if (frame.hands.length > 0) {
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
                handFlag = false;
            }
        });
        frame.fingers.forEach((finger) => {
            if (handFlag) {
                rightHandFingerTips[finger.type * 3] = finger.tipPosition[0];
                rightHandFingerTips[finger.type * 3 + 1] =
                    finger.tipPosition[1];
                rightHandFingerTips[finger.type * 3 + 2] =
                    finger.tipPosition[2];
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

        if (isRecording) {
            dataBuffer = dataBuffer.append([newData], [dataBuffer.shape[0]]);
            console.log(newData);
        }

        io.emit(config.FRAME_EVENT, newData.join());
    }
}

function writeBuffer(subjectId, gesture) {
    filename = new Date().getTime();
    let saveDir = path.join("..", "data", "dataset", subjectId, gesture);
    let filePath = path.join(saveDir, `${filename}.csv`);
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
}

function discardLastRecording(subjectId, gesture) {
    let fileDir = path.join("..", "data", "dataset", subjectId, gesture);
    let filePath = path.join(fileDir, `${filename}.csv`);
    try {
        fs.unlinkSync(filePath);
        console.log("last recording removed");
    } catch (e) {
        console.log("file operation failed!");
    }
}

module.exports = { processFrames, writeBuffer, discardLastRecording };
