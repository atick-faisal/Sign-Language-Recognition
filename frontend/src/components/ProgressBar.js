import { Progress } from "reactstrap";

export default function ProgressBar({
    isRecording,
    preparationProgress,
    recordingProgress,
}) {
    if (isRecording) {
        return (
            <>
                <br />
                <Progress multi>
                    <Progress
                        bar
                        color="warning"
                        max={1}
                        value={preparationProgress}
                    />
                    <Progress
                        bar
                        color="danger"
                        max={1}
                        value={recordingProgress}
                    />
                </Progress>
            </>
        );
    }
}
