import asyncio
from dataclasses import replace

from ball_control import BallControl
from scenario import Scenario
from state_manager import StateManager
from scenario_control import ScenarioControl
from state_update_model import StateModel, StatePosition, StateUpdateModel, get_default_state
from update_reporter import UpdateReporter

class BallControlSim(BallControl, ScenarioControl):

    delay_mult: float
    update_reporter: UpdateReporter
    state_manager: StateManager
    state: StateModel

    def __init__(self, update_reporter: UpdateReporter, delay_multiplier: float = 1.0):
        self.update_reporter = update_reporter
        self.state_manager = StateManager()
        self.delay_mult = delay_multiplier
        self.state = get_default_state()

    async def __aenter__(self):
        pass
    
    async def __aexit__(self, *_):
        await self.update_reporter.shutdown()

    async def __send_update(self, include_balls: bool = False):
        state_to_send = self.state if (include_balls) else replace(self.state, balls = None)

        state_update: StateUpdateModel = StateUpdateModel(
                userId="glen",
                state=state_to_send
            )

        await self.update_reporter.send_update(state_update)
   
    async def __delay(self, duration: float):
        await asyncio.sleep(duration * self.delay_mult)

    async def _move_relative(self, x: int, y: int, delay: float = 1.0):
        delayTask = asyncio.create_task(self.__delay(delay))
        await self.__send_update()
        await delayTask

    async def move_horizontally(self, distance: int):
        if (0 == distance):
            return
        
        try:
            self.state = self.state_manager.move_horizontally_start(state=self.state, distance=distance)
            await self._move_relative(x=distance, y=0, delay=1.0)            
        finally:
            self.state = self.state_manager.move_horizontally_end(state=self.state)
            await self.__send_update()

    async def move_vertically(self, distance: int) -> None:
        if (0 == distance):
            return
        
        try:
            self.state = self.state_manager.move_vertically_start(state=self.state, distance=distance)
            await self._move_relative(x=0, y=distance, delay=1.5)
        finally:
            self.state = self.state_manager.move_vertically_end(state=self.state)
            await self.__send_update()

    def get_position(self) -> StatePosition:
        return self.state.claw.pos

    async def open_claw(self):
        try:
            delayTask = asyncio.create_task(self.__delay(0.3))
            self.state = self.state_manager.open_claw_start(state=self.state)

            await self.__send_update()
            await delayTask
        finally:
            self.state = self.state_manager.open_claw_end(state=self.state)

    async def close_claw(self):
        try:
            delayTask = asyncio.create_task(self.__delay(0.3))
            self.state = self.state_manager.close_claw_start(state=self.state)

            await self.__send_update()
            await delayTask
        finally:
            self.state = self.state_manager.close_claw_end(state=self.state)

    async def set_scenario(self, scenario: Scenario):
        self.state = self.state_manager.set_scenario(state=self.state, scenario=scenario)
        await self.__send_update(include_balls = True)
