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

    def move_horizontally(self, state: StateModel, distance: int):
        newX = state.claw.pos.x + distance
        if newX < MIN_X or newX > MAX_X:
            raise IllegalBallControlStateError(f"X coordinate out of bounds x={newX} minX={MIN_X} maxX={MAX_X}")
    
    def move_vertically(self, state: StateModel, distance: int) -> None:
        newY = state.claw.pos.y + distance
        if newY < MIN_Y or newY > MAX_Y:
            raise IllegalBallControlStateError(f"Y coordinate out of bounds y={newY} minY={MIN_Y} maxY={MAX_Y}")

    def open_claw(self, state: StateModel):
        #print("state: ", state)
        if not is_ball_in_claw(state):
            return
        
        #todo: check for ongoing claw movement
        ##if state.claw.

        if state.claw.pos.y != get_top_vacant_index(state):
            raise IllegalBallControlStateError(
                f"Illegal drop location. Must be topmost vacant position ({get_top_vacant_index(state)}). Y={state.claw.pos.y}."
            )

    def close_claw(self, state: StateModel):
        #print("state: ", state)
        if not is_ball_at_current_pos(state):
            return
        
        #todo: check for ongoing claw movement

        if state.claw.pos.y != get_top_occupied_index(state):
            raise IllegalBallControlStateError(
                f"Illegal grab. Must be topmost marble position ({get_top_occupied_index(state)}). Y={state.claw.pos.y}."
            )
