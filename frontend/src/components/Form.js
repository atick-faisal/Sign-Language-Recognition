import { useState } from "react";
import { Card, CardTitle } from "reactstrap";
import { Label, Input, InputGroup } from "reactstrap";
import { Button } from "reactstrap";
import {
    Dropdown,
    DropdownToggle,
    DropdownMenu,
    DropdownItem,
} from "reactstrap";

const gestures = ["A", "B", "C"];

export default function Form({ message }) {
    const [gesture, setGesture] = useState();
    const [toggle, setToggle] = useState(false);

    return (
        <div className="container w-50">
            <Card className="formContainer">
                <CardTitle tag="h3">Hello</CardTitle>
                <Label>Subject ID</Label>
                <Input
                    id="subjectId"
                    name="subject-id"
                    placeholder="Unique ID of the Subject. Example: 007"
                    type="text"
                />
                <br />
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
                        <DropdownToggle caret>Select Gesture</DropdownToggle>
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
            </Card>
        </div>
    );
}
