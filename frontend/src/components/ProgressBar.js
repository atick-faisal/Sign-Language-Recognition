import { Progress } from "reactstrap";

export default function ProgressBar({
    preparationProgress,
    recordingProgress,
}) {
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
