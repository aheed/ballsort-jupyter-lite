from scenario_control import ScenarioControl
from state_update_model import StateBall, StatePosition


async def set_scenario1(sc: ScenarioControl):
    balls = [
        StateBall(pos=StatePosition(x=3, y=4), color="blue"),
        StateBall(pos=StatePosition(x=2, y=4), color="blue"),
        StateBall(pos=StatePosition(x=1, y=4), color="green"),
    ]
    await sc.set_scenario(balls)

async def set_scenario2(sc: ScenarioControl):
    balls = [
        StateBall(pos=StatePosition(x=0, y=2), color="yellow"),
        StateBall(pos=StatePosition(x=0, y=3), color="yellow"),
        StateBall(pos=StatePosition(x=0, y=4), color="pink"),
    ]
    await sc.set_scenario(balls)    
