from dataclasses import dataclass
from ball_control import IllegalBallControlStateError
from state_utils import (
    get_top_occupied_index,
    get_top_vacant_index,
    is_ball_at_current_pos,
    is_ball_in_claw,
)
from state_update_model import (
    StateModel,
    MIN_X,
    MAX_X,
    MIN_Y,
    MAX_Y,
)


@dataclass
class StateValidator:
    """Validates operations"""

    state: StateModel

    def move_relative(self, x: int, y: int):
        newX = self.state.claw.pos.x + x
        newY = self.state.claw.pos.y + y
        if newX < MIN_X or newY < MIN_Y or newX > MAX_X or newY > MAX_Y:
            raise IllegalBallControlStateError("coordinates out of bounds")

    #    def move_horizontally(self, distance: int):
    #        self.move_relative(x=distance, y=0)
    #
    #    def move_vertically(self, distance: int) -> None:
    #        self.move_relative(x=0, y=distance)

    def open_claw(self):
        if not is_ball_in_claw(self.state):
            return

        if self.state.claw.pos.y != get_top_occupied_index(self.state):
            raise IllegalBallControlStateError(
                "Illegal drop location. Must be topmost vacant position."
            )

    def close_claw(self):
        if not is_ball_at_current_pos(self.state):
            return

        if self.state.claw.pos.y != get_top_vacant_index(self.state):
            raise IllegalBallControlStateError(
                "Illegal grab. Must be topmost marble position."
            )
