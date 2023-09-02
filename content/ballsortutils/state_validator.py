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

    def move_relative(self, state: StateModel, x: int, y: int):
        #print("state: ", state)
        newX = state.claw.pos.x + x
        newY = state.claw.pos.y + y
        if newX < MIN_X or newY < MIN_Y or newX > MAX_X or newY > MAX_Y:
            raise IllegalBallControlStateError("coordinates out of bounds")

    #    def move_horizontally(self, distance: int):
    #        self.move_relative(x=distance, y=0)
    #
    #    def move_vertically(self, distance: int) -> None:
    #        self.move_relative(x=0, y=distance)

    def open_claw(self, state: StateModel):
        #print("state: ", state)
        if not is_ball_in_claw(state):
            return

        if state.claw.pos.y != get_top_vacant_index(state):
            raise IllegalBallControlStateError(
                f"Illegal drop location. Must be topmost vacant position ({get_top_vacant_index(state)}). Y={state.claw.pos.y}."
            )

    def close_claw(self, state: StateModel):
        #print("state: ", state)
        if not is_ball_at_current_pos(state):
            return

        if state.claw.pos.y != get_top_occupied_index(state):
            raise IllegalBallControlStateError(
                f"Illegal grab. Must be topmost marble position ({get_top_occupied_index(state)}). Y={state.claw.pos.y}."
            )
