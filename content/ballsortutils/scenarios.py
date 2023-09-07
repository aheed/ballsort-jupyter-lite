from ch0_scenario import Ch0Scenario
from ch1_scenario import Ch1Scenario
from scenario_control import ScenarioControl

async def set_scenario1(sc: ScenarioControl):
    await sc.set_scenario(Ch0Scenario())

async def set_challenge1_scenario(sc: ScenarioControl):
    await sc.set_scenario(Ch1Scenario())
