import { Button, Modal, ModalBody, ModalFooter, ModalHeader } from "reactstrap";

const TITLE = "Gesture Recorded Correctly?";
const DESCRIPTION =
    'If "Yes" then the recording will be stored otherwise it will be discarded. Please click "No" if there was any issue with the recording process.';

export default function Confirmation({
    isOpen,
    toggle,
    onPositiveClick,
    onNegativeClick,
}) {
    return (
        <Modal isOpen={isOpen} toggle={toggle}>
            <ModalHeader>
                <p className="title">{TITLE}</p>
            </ModalHeader>
            <ModalBody>{DESCRIPTION}</ModalBody>
            <ModalFooter>
                <Button color="danger" onClick={onNegativeClick}>
                    No, Discard Recording
                </Button>
                <Button color="primary" onClick={onPositiveClick}>
                    Yes, Save Recording
                </Button>
            </ModalFooter>
        </Modal>
    );
}
