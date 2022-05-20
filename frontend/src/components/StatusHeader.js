import { Button, ButtonGroup } from "reactstrap";
import { BsSpeedometer } from "react-icons/bs";
import { FaHandPaper, FaFingerprint } from "react-icons/fa";

export default function StatusHeader() {
    return (
        // <div className="d-flex justify-content-center">
        <ButtonGroup>
            <Button className="w-50" outline color="secondary">
                <BsSpeedometer size={40} />
                <br />
                Frame Rate: {110}
            </Button>
            <Button className="w-50" outline color="secondary">
                <FaHandPaper size={40} />
                <br />
                Number of Hands: {2}
            </Button>
            <Button className="w-50" outline color="secondary">
                <FaFingerprint size={40} />
                <br />
                Number of Fingers: {10}
            </Button>
        </ButtonGroup>
        // </div>
    );
}
