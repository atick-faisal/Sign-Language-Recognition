import io from "socket.io-client";
import { useEffect, useState } from "react";
import { Card, CardSubtitle, CardTitle } from "reactstrap";
import StatusHeader from "./components/StatusHeader";
import Form from "./components/Form";

let socket = null;

function App() {
    // const [socket, setSocket] = useState();
    const [status, setStatus] = useState("Not Connected");
    const [framerate, setFramerate] = useState(0);
    const [hands, setHands] = useState(0);
    const [fingers, setFingers] = useState(0);

    useEffect(() => {
        socket = io("ws://localhost:8080");

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

    const startRecordingData = (duration, subjectId, gesture) => {
        let requestBody = {
            duration: duration,
            subjectId: subjectId,
            gesture: gesture,
        };
        console.log(requestBody);
        socket.emit("record", JSON.stringify(requestBody));
    };

    return (
        <div className="container w-50">
            <Card className="formContainer">
                <CardTitle tag="h3">Data Collector</CardTitle>
                <CardSubtitle className="mb-2 text-muted" tag="h6">
                    Leap Motion Controller Status:
                    <b> {status} </b>
                </CardSubtitle>
                <br />
                <StatusHeader
                    framerate={framerate}
                    hands={hands}
                    fingers={fingers}
                />
                <br />
                <Form onSubmit={startRecordingData} />
            </Card>
        </div>
    );
}

export default App;
