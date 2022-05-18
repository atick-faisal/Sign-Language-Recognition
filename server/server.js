const server = require("http").createServer();
const io = require("socket.io")(server, {
    cors: { origin: "*" },
});
const leapjs = require("leapjs");
const { setLmcCallbacks } = require("./lmc");

const controller = new leapjs.Controller();
setLmcCallbacks(controller, io);

io.on("connection", (socket) => {
    console.log("a user connected");
    socket.on("message", (content) => {
        console.log(`received message ${content}`);
    });
});

server.listen(8080, () => {
    console.log("listening on http://localhost:8080");
});
