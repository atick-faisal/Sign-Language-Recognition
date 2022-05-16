const server = require("http").createServer();
const io = require("socket.io")(server, {
    cors: { origin: "*" },
});

let counter = 0;

io.on("connection", (socket) => {
    console.log("a user connected");
    socket.on("message", (content) => {
        console.log(`received message ${content}`);
    });
});

server.listen(8080, () => {
    console.log("listenning on http://localhost:8080");
});

setInterval(() => {
    console.log(`counter: ${counter}`);
    io.emit("message", `Counter = ${counter}`);
    counter++;
}, 1000);
