import asyncio
from dataclasses import replace
import sys

sys.path.append("../content/ballsortutils")

from control_factory import get_control_sim
from ch1_scenario import Ch1Scenario
from state_update_model import StateBall, StatePosition, get_default_state


def test_goal_state():
    sc = Ch1Scenario()
    state = get_default_state()
    assert sc.is_in_goal_state(state) == False
    state = sc.get_initial_state()
    assert sc.is_in_goal_state(state) == False

    balls = [
        StateBall(pos=StatePosition(x=0, y=4), color="pink"),
        StateBall(pos=StatePosition(x=0, y=3), color="pink"),
        StateBall(pos=StatePosition(x=2, y=3), color="yellow"),
        StateBall(pos=StatePosition(x=1, y=4), color="yellow"),
    ]
    state = replace(get_default_state(), balls=balls)
    assert sc.is_in_goal_state(state) == False

    balls = [
        StateBall(pos=StatePosition(x=0, y=4), color="pink"),
        StateBall(pos=StatePosition(x=0, y=3), color="pink"),
        StateBall(pos=StatePosition(x=2, y=3), color="yellow"),
        StateBall(pos=StatePosition(x=2, y=4), color="yellow"),
    ]
    state = replace(get_default_state(), balls=balls)
    assert sc.is_in_goal_state(state) == True


async def example_solution():
    bc = get_control_sim(0)
    async with bc:
        #await set_challenge1_scenario(bc)
        await bc.set_scenario(Ch1Scenario())

        # pink marble
        t2 = asyncio.create_task(bc.move_vertically(2))
        await t2
        await bc.close_claw()
        t1 = asyncio.create_task(bc.move_horizontally(2))
        t2 = asyncio.create_task(bc.move_vertically(2))
        await t1
        await t2
        await bc.open_claw()

        # yellow marble
        t1 = asyncio.create_task(bc.move_horizontally(-2))
        t2 = asyncio.create_task(bc.move_vertically(-1))
        await t1
        await t2
        await bc.close_claw()
        t3 = asyncio.create_task(bc.move_vertically(0))
        t4 = asyncio.create_task(bc.move_horizontally(1))
        await t3
        await t4
        await bc.open_claw()

        # pink marble
        t1 = asyncio.create_task(bc.move_horizontally(1))
        t2 = asyncio.create_task(bc.move_vertically(1))
        await t1
        await t2
        await bc.close_claw()
        t1 = asyncio.create_task(bc.move_horizontally(-2))
        t2 = asyncio.create_task(bc.move_vertically(-1))
        await t1
        await t2
        await bc.open_claw()


def main():
    test_goal_state()
    asyncio.run(example_solution())


if __name__ == "__main__":
    import time

    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"\n{__file__} executed in {elapsed:0.2f} seconds.")
