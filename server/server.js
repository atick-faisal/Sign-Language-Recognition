const leapjs = require("leapjs");
const server = require("http").createServer();
const io = require("socket.io")(server, {
    cors: { origin: "*" },
});

const { setLmcCallbacks, startRecording } = require("./lmc");
const config = require("../config/config");

const controller = new leapjs.Controller();
setLmcCallbacks(controller, io);

io.on(config.SOCKET_CONNECTION, (socket) => {
    console.log("a user connected");
    socket.on(config.MESSAGE_EVENT, (content) => {
        console.log(`received message ${content}`);
    });

    socket.on(config.RECORD_EVENT, (content) => {
        try {
            let recordRequest = JSON.parse(content);
            console.log(recordRequest);
            startRecording(recordRequest.subjectId, recordRequest.gesture);
        } catch (e) {
            console.log("could not parse JSON object");
        }
    });
});

server.listen(config.PORT, () => {
    console.log(`listening on http://localhost:${config.PORT}`);
});
