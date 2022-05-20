const server = require("http").createServer();
const io = require("socket.io")(server, {
    cors: { origin: "*" },
});
const leapjs = require("leapjs");
const { setLmcCallbacks, startRecording } = require("./lmc");

const controller = new leapjs.Controller();
setLmcCallbacks(controller, io);

io.on("connection", (socket) => {
    console.log("a user connected");
    socket.on("message", (content) => {
        console.log(`received message ${content}`);
    });

    socket.on("record", (content) => {
        try {
            let recordRequest = JSON.parse(content);
            startRecording(
                recordRequest.duration,
                recordRequest.subjectId,
                recordRequest.gesture
            );
        } catch (e) {
            console.log("could not parse JSON object");
        }
    });
});

server.listen(8080, () => {
    console.log("listening on http://localhost:8080");
});
