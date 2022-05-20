import { useState } from "react";
import { Label, Input, InputGroup } from "reactstrap";
import {
    Dropdown,
    DropdownToggle,
    DropdownMenu,
    DropdownItem,
} from "reactstrap";

const gestures = ["A", "B", "C"];

export default function GestureSelector({ gesture, setGesture }) {
    const [toggle, setToggle] = useState(false);

    return (
        <div className="d-flex-vertical">
            <Label>Name of the Gesture</Label>
            <Dropdown isOpen={toggle} toggle={() => setToggle(!toggle)}>
                <InputGroup>
                    <Input
                        id="gesture"
                        name="gesture"
                        placeholder="Please Select the Name of The Gesture"
                        type="text"
                        value={gesture}
                        onChange={(e) => setGesture(e.target.value)}
                    />
                    <DropdownToggle color="primary" caret>
                        Select
                    </DropdownToggle>
                    <DropdownMenu children={null}>
                        <DropdownItem>Hello</DropdownItem>
                        {gestures.map((gesture) => (
                            <DropdownItem
                                key={gesture}
                                onClick={() => setGesture(gesture)}
                            >
                                {gesture}
                            </DropdownItem>
                        ))}
                    </DropdownMenu>
                </InputGroup>
            </Dropdown>
        </div>
    );
}
