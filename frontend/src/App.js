import io from "socket.io-client";
import { useEffect, useState } from "react";
import { Card, CardSubtitle, CardTitle, Collapse } from "reactstrap";
import StatusHeader from "./components/StatusHeader";
import Form from "./components/Form";
import config from "./config/config";
import ToggleButton from "./components/ToggleButton";
import Prediction from "./components/Prediction";

let socket = null;

function App() {
    const [status, setStatus] = useState("Not Connected");
    const [framerate, setFramerate] = useState(0);
    const [hands, setHands] = useState(0);
    const [fingers, setFingers] = useState(0);
    const [mode, setMode] = useState("collection");

    useEffect(() => {
        socket = io(`ws://localhost:${config.PORT}`);

        socket.on(config.STATUS_EVENT, (content) => {
            setStatus(content);
        });

        socket.on(config.FRAMERATE_EVENT, (content) => {
            setFramerate(content);
        });

        socket.on(config.HANDS_EVENT, (content) => {
            setHands(content);
        });

        socket.on(config.FINGERS_EVENT, (content) => {
            setFingers(content);
        });

        return () => socket.close();
    }, []);

    const startRecordingData = (subjectId, gesture) => {
        let requestBody = {
            subjectId: subjectId,
            gesture: gesture,
        };
        console.log(requestBody);
        socket.emit(config.RECORD_EVENT, JSON.stringify(requestBody));
    };

    return (
        <div className="container w-50">
            <Card className="formContainer">
                <ToggleButton mode={mode} setMode={setMode} />
                <br />
                <CardTitle className="title" color="primary">
                    {mode.toUpperCase()}
                </CardTitle>
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
                <Collapse isOpen={mode === "collection"}>
                    <Form onSubmit={startRecordingData} />
                </Collapse>
                <Collapse isOpen={mode !== "collection"}>
                    <Prediction prediction="Predicting ... " />
                </Collapse>
            </Card>
        </div>
    );
}

export default App;
