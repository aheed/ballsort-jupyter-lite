from dataclasses import dataclass, replace
from scenario import Scenario
from state_update_model import (
    StateBall,
    StateModel,
    StatePosition,
    get_default_state,
)


@dataclass
class Ch4Scenario(Scenario):
    """Challenge Implementation"""

    def get_goal_state_description(self) -> str:
        return f"Hanoi Tower\nMove all marbles from the leftmost column to the rightmost column. A marble can not be placed on top of a marble of lower value.\n{self.get_dimensions_description()}"
    
    def get_initial_state(self) -> StateModel:
        balls: list[StateBall] = []
        max_x = 2
        max_y = 5
        balls = [StateBall(pos=StatePosition(x=0, y=y), color="lightgreen", value=y+1) for y in range(max_y)]
        
        return replace(get_default_state(), balls = balls, max_x=max_x, max_y=max_y)

    def is_in_goal_state(self, state: StateModel) -> bool:

        # No ball in claw
        if state.claw.ball_color:
            return False
        
        def validate_ball(ball: StateBall) -> bool:
            # ball must be in rightmost column
            if ball.pos.x != state.max_x:
                return False
            return True

        return not next((True for ball in state.balls if not validate_ball(ball)), False)
    
    