import { Button, ButtonGroup } from "reactstrap";
import { BsSpeedometer } from "react-icons/bs";
import { FaRegHandPaper, FaFingerprint } from "react-icons/fa";

export default function StatusHeader({ framerate, hands, fingers }) {
    return (
        // <div className="d-flex justify-content-center">
        <ButtonGroup>
            <Button className="w-50" outline color="success">
                <BsSpeedometer size={40} style={{ margin: "8px" }} />
                <br />
                <h6>Frame Rate: {parseInt(framerate)}</h6>
            </Button>
            <Button className="w-50" outline color="success">
                <FaRegHandPaper size={40} style={{ margin: "8px" }} />
                <br />
                <h6>Number of Hands: {hands}</h6>
            </Button>
            <Button className="w-50" outline color="success">
                <FaFingerprint size={40} style={{ margin: "8px" }} />
                <br />
                <h6>Number of Fingers: {fingers}</h6>
            </Button>
        </ButtonGroup>
        // </div>
    );
}
