from dataclasses import dataclass
from ball_control import IllegalBallControlStateError
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

    def _is_ball_in_claw(self) -> bool:
        return not not self.state.claw.ball_color
    
    def _is_ball_at_current_pos(self) -> bool:
        return next(
            (True for ball in self.state.balls if ball.pos == self.state.claw.pos),
            False,
        )
        # balls_at_current_pos = filter(lambda ball: ball.pos == self.state.claw.pos, self.state.balls)
        # return any(balls_at_current_pos)

    def _get_top_occupied_index(self) -> int:
        y_indexes_in_current_column = [
            ball.pos.y
            for ball in self.state.balls
            if ball.pos.x == self.state.claw.pos.x
        ]
        top_occupied_y_index = (
            max(y_indexes_in_current_column) if y_indexes_in_current_column else MAX_Y
        )
        return top_occupied_y_index

    def _get_top_vacant_index(self) -> int:
        return self._get_top_occupied_index() - 1

    def move_relative(self, x: int, y: int):
        newX = self.state.claw.pos.x + x
        newY = self.state.claw.pos.y + y
        if newX < MIN_X or newY < MIN_Y or newX > MAX_X or newY > MAX_Y:
            raise IllegalBallControlStateError("coordinates out of bounds")

    def move_horizontally(self, distance: int):
        self.move_relative(x=distance, y=0)

    def move_vertically(self, distance: int) -> None:
        self.move_relative(x=0, y=distance)

    def open_claw(self):
        if not self._is_ball_in_claw():
            return

        if self.state.claw.pos.y != self._get_top_occupied_index():
            raise IllegalBallControlStateError(
                "Illegal drop location. Must be topmost vacant position."
            )

    def close_claw(self):
        if not self._is_ball_at_current_pos():
            return

        if self.state.claw.pos.y != self._get_top_vacant_index():
            raise IllegalBallControlStateError(
                "Illegal grab. Must be topmost marble position."
            )
