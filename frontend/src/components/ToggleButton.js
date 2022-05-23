import { Button, ButtonGroup } from "reactstrap";

export default function ToggleButton({ mode, setMode }) {
    const toggle = () => {
        if (mode === "collection") {
            setMode("inference");
        } else {
            setMode("collection");
        }
    };

    return (
        <div className="d-flex justify-content-center">
            <ButtonGroup>
                <Button
                    color="primary"
                    outline={mode === "inference"}
                    onClick={toggle}
                >
                    Collection
                </Button>
                <Button
                    color="primary"
                    outline={mode === "collection"}
                    onClick={toggle}
                >
                    Inference
                </Button>
            </ButtonGroup>
        </div>
    );
}
