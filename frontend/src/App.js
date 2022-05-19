import { useEffect, useState } from "react";
import io from "socket.io-client";

import Form from "./components/Form";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
    const [message, setMessage] = useState("Hello");

    useEffect(() => {
        const socket = io("ws://localhost:8080");
        socket.on("status", (content) => {
            setMessage(content);
        });
        return () => socket.close();
    }, []);
    return <Form message={message} />;
}

export default App;
