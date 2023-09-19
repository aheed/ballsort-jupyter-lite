import asyncio
from dataclasses import replace
import sys

sys.path.append("../content/ballsortutils")

from control_factory import get_ch4_control_sim
from ch4_scenario import Ch4Scenario
from state_update_model import StateBall, StatePosition


def test_goal_state():
    sc = Ch4Scenario()
    
    state = sc.get_initial_state()
    assert sc.is_in_goal_state(state) == False

    balls = [
        StateBall(pos=StatePosition(x=2, y=0), color="gray", value=1),
        StateBall(pos=StatePosition(x=2, y=1), color="gray", value=2),
        StateBall(pos=StatePosition(x=2, y=2), color="gray", value=3),
        StateBall(pos=StatePosition(x=2, y=3), color="gray", value=4),
        StateBall(pos=StatePosition(x=2, y=4), color="gray", value=5),
        StateBall(pos=StatePosition(x=2, y=5), color="gray", value=6),
    ]

    state = replace(sc.get_initial_state(), balls=balls)
    assert sc.is_in_goal_state(state) == True

async def test_validation():
    bc = get_ch4_control_sim(0)
    await bc.set_scenario(Ch4Scenario())

    #todo: check exception is thrown when dropping high ball on low ball

async def example_solution():
    bc = get_ch4_control_sim(0)
    await bc.set_scenario(Ch4Scenario())

    #todo: implement solution

def main():
    test_goal_state()
    asyncio.run(test_validation())
    asyncio.run(example_solution())

if __name__ == "__main__":
    import time

    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"\n{__file__} executed in {elapsed:0.2f} seconds.")
