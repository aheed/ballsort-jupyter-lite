from ch1_scenario import Ch1Scenario
from scenario_control import ScenarioControl
from state_update_model import StateBall, StatePosition


async def set_scenario1(sc: ScenarioControl):
    balls = [
        StateBall(pos=StatePosition(x=3, y=4), color="blue"),
        StateBall(pos=StatePosition(x=2, y=4), color="blue"),
        StateBall(pos=StatePosition(x=1, y=4), color="green"),
    ]
    await sc.set_scenario(balls)
    print("Goal: All marbles shall be in the leftmost column")

async def set_challenge1_scenario(sc: ScenarioControl):
    scenario = Ch1Scenario()
    await sc.set_scenario(scenario.get_initial_state().balls)
    print(f"Goal:\n{scenario.get_goal_state_description()}")
