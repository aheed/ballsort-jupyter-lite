import asyncio
from dataclasses import replace
import sys

sys.path.append("../content/ballsortutils")

from control_factory import get_ch2_control_sim
from ball_control import BallControl
from ch2_scenario import Ch2Scenario
from state_update_model import StateBall, StatePosition, get_default_state


def test_goal_state():
    sc = Ch2Scenario()
    state = get_default_state()
    assert sc.is_in_goal_state(state) == False
    state = sc.get_initial_state()
    assert sc.is_in_goal_state(state) == False

    balls = [
        StateBall(pos=StatePosition(x=0, y=2), color="green"),
        StateBall(pos=StatePosition(x=0, y=3), color="yellow"),
        StateBall(pos=StatePosition(x=0, y=4), color="blue"),
    ]
    state = replace(get_default_state(), balls=balls)
    assert sc.is_in_goal_state(state) == False

    balls = [
        StateBall(pos=StatePosition(x=0, y=2), color="blue"),
        StateBall(pos=StatePosition(x=0, y=3), color="green"),
        StateBall(pos=StatePosition(x=0, y=4), color="yellow"),
    ]
    state = replace(get_default_state(), balls=balls)
    assert sc.is_in_goal_state(state) == True

async def move_ball(bc: BallControl, src: StatePosition, dest: StatePosition):    
    rel_x = src.x - bc.get_position().x
    rel_y = src.y - bc.get_position().y
    await asyncio.gather(
        bc.move_horizontally(rel_x),
        bc.move_vertically(rel_y),
        bc.open_claw())
    await bc.close_claw()
    
    rel_x = dest.x - bc.get_position().x
    rel_y = dest.y - bc.get_position().y
    await asyncio.gather(
        bc.move_horizontally(rel_x),
        bc.move_vertically(rel_y))
    await bc.open_claw()

async def example_solution_no_scales():
    bc = get_ch2_control_sim(delay_multiplier=0.0)
    async with bc:
        await bc.set_scenario(Ch2Scenario())

        # yellow marble
        await move_ball(bc=bc, src=StatePosition(x=1, y=2), dest=StatePosition(x=0, y=4))

        # green marble
        await move_ball(bc=bc, src=StatePosition(x=1, y=3), dest=StatePosition(x=0, y=3))

        # blue marble
        await move_ball(bc=bc, src=StatePosition(x=1, y=4), dest=StatePosition(x=0, y=2))

async def example_solution():
    bc = get_ch2_control_sim(delay_multiplier=0.0)
    async with bc:
        await bc.set_scenario(Ch2Scenario())

        # yellow marble to left scale
        await move_ball(bc=bc, src=StatePosition(x=1, y=2), dest=StatePosition(x=2, y=4))

        # green marble to right scale
        await move_ball(bc=bc, src=StatePosition(x=1, y=3), dest=StatePosition(x=3, y=4))

        yellow_heavier_than_green = await bc.read_scales()
        print(f"yellow vs green weight:  {yellow_heavier_than_green}")

        # todo: processing and shifting to sort marbles
        #       Skip to goal state for now, knowing the hard coded weights

        await move_ball(bc=bc, src=StatePosition(x=2, y=4), dest=StatePosition(x=0, y=4))
        await move_ball(bc=bc, src=StatePosition(x=3, y=4), dest=StatePosition(x=0, y=3))
        await move_ball(bc=bc, src=StatePosition(x=1, y=4), dest=StatePosition(x=0, y=2))


def main():
    test_goal_state()
    asyncio.run(example_solution_no_scales())
    asyncio.run(example_solution())


if __name__ == "__main__":
    import time

    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"\n{__file__} executed in {elapsed:0.2f} seconds.")