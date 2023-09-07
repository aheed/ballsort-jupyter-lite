import asyncio
from dataclasses import replace

from ball_control import BallControl, IllegalBallControlStateError
from state_manager import StateManager
from scenario_control import ScenarioControl
from state_update_model import StateBall, StateUpdateModel, get_default_state
from update_reporter import UpdateReporter

class BallControlSim(BallControl, ScenarioControl):

    delay_mult: float
    moving_horizontally = False
    moving_vertically = False
    operating_claw = False
    update_reporter: UpdateReporter
    state_manager: StateManager

    def __init__(self, update_reporter: UpdateReporter, delay_multiplier: float = 1.0):
        self.update_reporter = update_reporter
        self.state_manager = StateManager(get_default_state())
        self.delay_mult = delay_multiplier

    async def __aenter__(self):
        pass
    
    async def __aexit__(self, *_):
        await self.update_reporter.shutdown()

    async def __send_update(self, include_balls: bool = False):
        state_to_send = self.state_manager.state if (include_balls) else replace(self.state_manager.state, balls = None)

        state_update: StateUpdateModel = StateUpdateModel(
                userId="glen",
                state=state_to_send
            )

        await self.update_reporter.send_update(state_update)
   
    async def __delay(self, duration: float):
        await asyncio.sleep(duration * self.delay_mult)

    async def move_relative(self, x: int, y: int = 0, delay: float = 1.0):
        self.state_manager.move_relative(x, y)

        delayTask = asyncio.create_task(self.__delay(delay))

        await self.__send_update()
        await delayTask

    async def move_horizontally(self, distance: int):
        if (0 == distance):
            return
        if (self.moving_horizontally):
            raise IllegalBallControlStateError("Already moving horizontally")
        self.moving_horizontally = True
        try:
            await self.move_relative(distance, delay=1.0)
        finally:
            self.moving_horizontally = False

    async def move_vertically(self, distance: int) -> None:
        if (0 == distance):
            return
        if (self.moving_vertically):
            raise IllegalBallControlStateError("Already moving vertically")
        self.moving_vertically = True
        try:
            await self.move_relative(0, distance, delay=1.5)
        finally:
            self.moving_vertically = False
            
    def move_horizontally_sync(self, distance: int):
        asyncio.run(self.move_horizontally(distance))
    
    def move_vertically_sync(self, distance: int):
        asyncio.run(self.move_vertically(distance))

    def move_relative_sync(self, x: int, y: int = 0):
        asyncio.run(self.move_relative(x, y))

    def get_position(self) -> tuple[int, int]:
        return self.state_manager.state.claw.pos.x, self.state_manager.state.claw.pos.y

    async def __operate_claw(self, open: bool):
        if (self.operating_claw):
            raise IllegalBallControlStateError("Claw already opening or closing")
        self.operating_claw = True
        try:
            delayTask = asyncio.create_task(self.__delay(0.3))
            self.state_manager.open_claw() if open else self.state_manager.close_claw()

            await self.__send_update()
            await delayTask
        finally:
            self.operating_claw = False

    async def open_claw(self):
        await self.__operate_claw(True)

    async def close_claw(self):
        await self.__operate_claw(False)

    async def set_scenario(self, balls: list[StateBall]):
        self.state_manager.state = replace(get_default_state(), balls = balls)
        await self.__send_update(include_balls = True)
