import asyncio
from dataclasses import replace

from ball_control import BallControl
from ball_control_sim import BallControlSim
from ch2_state_manager import Ch2StateManager
from scenario import Scenario
from state_manager import StateManager
from scenario_control import ScenarioControl
from state_update_model import StateModel, StateUpdateModel, get_default_state
from update_reporter import UpdateReporter

class BallControlCh2(BallControlSim, ScenarioControl):

    ch2_state_manager: Ch2StateManager

    def __init__(self, update_reporter: UpdateReporter, delay_multiplier: float = 1.0):
        super().__init__(update_reporter=update_reporter, delay_multiplier=delay_multiplier)
        self.ch2_state_manager = Ch2StateManager()

