from ball_control import IllegalBallControlStateError
from ball_control_sim import BallControlSim
from ch2_state_manager import Ch2StateManager
from scenario_control import ScenarioControl
from state_update_model import StatePosition
from state_utils import get_ball_at
from update_reporter import UpdateReporter

class BallControlCh2(BallControlSim, ScenarioControl):

    ch2_state_manager: Ch2StateManager

    def __init__(self, update_reporter: UpdateReporter, delay_multiplier: float = 1.0):
        super().__init__(update_reporter=update_reporter, delay_multiplier=delay_multiplier)
        self.ch2_state_manager = Ch2StateManager()

    async def read_scales(self) -> int:
        """
        Returns negative if left is heavier, positive if right is heavier, 0 if equal.
        Hard coded coordinates: left=(2,4) right=(3,4)
        """

        left_pos = StatePosition(x=2, y=4)
        right_pos = StatePosition(x=3, y=4)
        
        if (self.state.claw.pos == left_pos or self.state.claw.pos == right_pos) and self.state.operating_claw:
            raise IllegalBallControlStateError("Scales can not be used while claw is opening or closing.")
        
        #todo: check that max one ball is present in the column
        #      Or sum the weights of all balls in the scales columns

        await self._delay(0.3)

        # Hard coded weights
        def get_weight_by_color(color: str) -> int:
            match color:
                case "yellow":
                    return 5
                case "green":
                    return 2
                case "blue":
                    return 1
                case _:
                    return 0

        left_ball = get_ball_at(state=self.state, pos=left_pos)
        left_color = left_ball.color if left_ball else ""
        left_weight = get_weight_by_color(left_color)
        right_ball = get_ball_at(state=self.state, pos=right_pos)
        right_color = right_ball.color if right_ball else ""
        right_weight = get_weight_by_color(right_color)
        return right_weight - left_weight
