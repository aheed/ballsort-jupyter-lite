from dataclasses import dataclass, replace
from state_validator import StateValidator
from state_update_model import (
    StateModel,
    StatePosition,
)


@dataclass
class StateManager:
    """Validates operations and keeps state up to date"""

    state: StateModel
    validator: StateValidator

    def __init__(self, state: StateModel):
        self.state = state
        self.validator = StateValidator(state)

    def move_relative(self, x: int, y: int):
        self.validator.move_relative(x, y)
        newX = self.state.claw.pos.x + x
        newY = self.state.claw.pos.y + y
        self.state = replace(self.state, claw=replace(self.state.claw, pos=StatePosition(x = newX, y = newY)))

    def move_horizontally(self, distance: int):
        self.move_relative(x=distance, y=0)

    def move_vertically(self, distance: int) -> None:
        self.move_relative(x=0, y=distance)

    def open_claw(self):
        self.validator.open_claw()
        self.state = replace(self.state, claw=replace(self.state.claw, open=True))
        #todo: update ball-in-claw color and balls collection

    def close_claw(self):
        self.validator.close_claw()
        self.state = replace(self.state, claw=replace(self.state.claw, open=False))
        #todo: update ball-in-claw color and balls collection
