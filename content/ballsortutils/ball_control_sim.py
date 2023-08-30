import asyncio
from dataclasses import replace

from ball_control import BallControl, IllegalBallControlStateError
from scenario_control import ScenarioControl
from state_update_model import StateBall, StatePosition, StateUpdateModel, get_default_state
from update_reporter import UpdateReporter

class BallControlSim(BallControl, ScenarioControl):

    MIN_X = 0
    MIN_Y = 0
    MAX_X = 3
    MAX_Y = 4
    delay_mult = 1.0
    state = get_default_state()
    moving_horizontally = False
    moving_vertically = False
    operating_claw = False
    update_reporter: UpdateReporter

    def __init__(self, update_reporter: UpdateReporter):
        self.update_reporter = update_reporter

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

    def __set_position(self, x: int, y: int = 0):
        if (x < self.MIN_X or y < self.MIN_Y or x > self.MAX_X or y > self.MAX_Y):
            raise Exception("coordinates out of bounds")
        self.state = replace(self.state, claw=replace(self.state.claw, pos=StatePosition(x = x, y = y)))
        print(f"new position: {x}, {y}")
    
    async def __delay(self, duration: float):
        await asyncio.sleep(duration * self.delay_mult)

    async def move_relative(self, x: int, y: int = 0, delay: float = 1.0):
        
        newX = self.state.claw.pos.x + x
        newY = self.state.claw.pos.y + y
        self.__set_position(newX, newY)
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
        return self.state.claw.pos.x, self.state.claw.pos.y

    async def __operate_claw(self, open: bool):
        if (self.operating_claw):
            raise IllegalBallControlStateError("Claw already opening or closing")
        self.operating_claw = True
        try:
            self.claw_open = open
            delayTask = asyncio.create_task(self.__delay(0.3))
            
            self.state = replace(self.state, claw=replace(self.state.claw, open=open))
            print(f"new claw open state: {open}")

            await self.__send_update()
            await delayTask
        finally:
            self.operating_claw = False

    async def open_claw(self):
        await self.__operate_claw(True)

    async def close_claw(self):
        await self.__operate_claw(False)

    async def set_scenario(self, balls: list[StateBall]):
        self.state = get_default_state()
        self.state = replace(self.state, balls = balls)
        await self.__send_update(include_balls = True)
