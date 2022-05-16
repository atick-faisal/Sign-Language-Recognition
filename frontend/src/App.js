import { useEffect, useState } from "react";
import io from "socket.io-client";

function App() {
    const [message, setMessage] = useState("Hello");

    useEffect(() => {
        const socket = io("ws://localhost:8080");
        socket.on("message", (content) => {
            setMessage(content);
        });
        return () => socket.close();
    }, []);
    return (
        <div className="App">
            <h1>{message}</h1>
        </div>
    );
}

export default App;
