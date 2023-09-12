from dataclasses import dataclass, replace
from scenario import Scenario
from state_update_model import (
    MIN_X,
    StateBall,
    StateModel,
    StatePosition,
    get_default_state,
)


@dataclass
class Ch2Scenario(Scenario):
    """Challenge Implementation"""

    def get_goal_state_description(self) -> str:
        return "Sort balls by weight in leftmost column. Heaviest at the bottom."
    
    def get_initial_state(self) -> StateModel:
        balls = [
            StateBall(pos=StatePosition(x=1, y=2), color="yellow"),
            StateBall(pos=StatePosition(x=1, y=3), color="green"),
            StateBall(pos=StatePosition(x=1, y=4), color="blue"),
        ]
        return replace(get_default_state(), balls = balls)

    def is_in_goal_state(self, state: StateModel) -> bool:

        # No ball in claw
        if state.claw.ball_color:
            return False
        
        # yellow at bottom
        if not next((True for y_ball in state.balls if y_ball.color == "yellow" and y_ball.pos == StatePosition(x=MIN_X, y=state.max_y)), False):
            return False

        # green in the middle
        if not next((True for g_ball in state.balls if g_ball.color == "green" and g_ball.pos == StatePosition(x=MIN_X, y=state.max_y-1)), False):
            return False
        
        # blue on top
        if not next((True for b_ball in state.balls if b_ball.color == "blue" and b_ball.pos == StatePosition(x=MIN_X, y=state.max_y-2)), False):
            return False
        
        return True
    
    