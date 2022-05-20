import { Button, ButtonGroup } from "reactstrap";
import { BsSpeedometer } from "react-icons/bs";
import { FaRegHandPaper, FaFingerprint } from "react-icons/fa";

export default function StatusHeader({ framerate, hands, fingers }) {
    return (
        <ButtonGroup>
            <Button className="w-100" outline color="dark">
                <FaRegHandPaper size={30} style={{ margin: "0.7rem" }} />
                <br />
                <h6>Number of Hands: {hands}</h6>
            </Button>
            <Button className="w-100" outline color="dark">
                <BsSpeedometer size={30} style={{ margin: "0.7rem" }} />
                <br />
                <h6>Frame Rate: {parseInt(framerate)}</h6>
            </Button>
            <Button className="w-100" outline color="dark">
                <FaFingerprint size={30} style={{ margin: "0.7rem" }} />
                <br />
                <h6>Number of Fingers: {fingers}</h6>
            </Button>
        </ButtonGroup>
    );
}
