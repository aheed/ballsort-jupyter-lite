from dataclasses import dataclass, replace
from scenario import Scenario
from state_utils import get_ball_at_current_pos, is_ball_in_claw
from state_validator import StateValidator
from state_update_model import (
    StateBall,
    StateModel,
    StatePosition,
)


@dataclass
class StateManager:
    """Validates operations and keeps state up to date"""

    state: StateModel
    validator: StateValidator
    scenario: Scenario | None

    def __init__(self, state: StateModel, scenario : Scenario | None = None):
        self.state = state
        self.validator = StateValidator()
        self.scenario = scenario

    def _check_goal_state(self):
        if self.scenario is None:
            return
        isInGoalState = self.scenario.is_in_goal_state(self.state)
        if (isInGoalState and not self.state.isInGoalState):
            print("Goal accomplished! 😁")
        self.state.isInGoalState = isInGoalState

    def set_scenario(self, scenario: Scenario):
        self.scenario = scenario
        self.state = scenario.get_initial_state()
        print(f"Goal:\n{scenario.get_goal_state_description()}")

    def _move_relative(self, x: int, y: int):
        newX = self.state.claw.pos.x + x
        newY = self.state.claw.pos.y + y
        self.state = replace(self.state, claw=replace(self.state.claw, pos=StatePosition(x = newX, y = newY)))
        print(f"new position: {newX}, {newY}")

    def move_horizontally_start(self, distance: int):
        self.validator.move_horizontally(state=self.state, distance=distance)
        self.moving_horizontally = True
        self._move_relative(x=distance, y=0)
    
    def move_horizontally_end(self):
        self.moving_horizontally = False

    def move_vertically_start(self, distance: int) -> None:
        self.validator.move_vertically(state=self.state, distance=distance)
        self._move_relative(x=0, y=distance)

    def move_vertically_end(self) -> None:
        self.moving_vertically = False

    def open_claw_start(self):
        self.validator.open_claw(self.state)
        self.state.operating_claw = True
        self.state.claw.open = True
        print(f"opening claw")
        if not is_ball_in_claw(self.state):
            return
        print(f"dropping {self.state.claw.ball_color} marble")
        newBall = StateBall(pos=self.state.claw.pos, color=self.state.claw.ball_color)
        self.state.claw.ball_color = ""
        self.state.balls.append(newBall)
        self._check_goal_state()

    def close_claw_start(self):
        self.validator.close_claw(self.state)
        self.state.operating_claw = True
        self.state.claw.open = False
        print(f"closing claw")
        ball_to_grab = get_ball_at_current_pos(self.state)
        if not ball_to_grab:
            return
        print(f"grabbing {ball_to_grab.color} marble")
        self.state.claw.ball_color = ball_to_grab.color
        #remove ball from list
        self.state.balls = [ball for ball in self.state.balls if ball.pos != ball_to_grab.pos]
        self._check_goal_state()

    def open_claw_end(self):
        self.state.operating_claw = False

    def close_claw_end(self):
        self.state.operating_claw = False
