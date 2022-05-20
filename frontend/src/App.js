import io from "socket.io-client";
import { useEffect, useState } from "react";
import Form from "./components/Form";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
    const [status, setStatus] = useState("Not Connected");
    const [framerate, setFramerate] = useState(0);
    const [hands, setHands] = useState(0);
    const [fingers, setFingers] = useState(0);

    useEffect(() => {
        const socket = io("ws://localhost:8080");

        socket.on("status", (content) => {
            setStatus(content);
        });

        socket.on("framerate", (content) => {
            setFramerate(content);
        });

        socket.on("hands", (content) => {
            setHands(content);
        });

        socket.on("fingers", (content) => {
            setFingers(content);
        });

        return () => socket.close();
    }, []);
    return (
        <Form
            status={status}
            framerate={framerate}
            hands={hands}
            fingers={fingers}
        />
    );
}

export default App;
