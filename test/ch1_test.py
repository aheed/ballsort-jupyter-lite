from dataclasses import replace
import sys
sys.path.append("../content/ballsortutils")

from ch1_scenario import Ch1Scenario
from state_update_model import StateBall, StatePosition, get_default_state

def test_goal_state():
    sc = Ch1Scenario()
    state = get_default_state()
    assert(sc.is_in_goal_state(state) == False)
    state = sc.get_initial_state()
    assert(sc.is_in_goal_state(state) == False)

    balls = [
            StateBall(pos=StatePosition(x=0, y=4), color="pink"),
            StateBall(pos=StatePosition(x=0, y=3), color="pink"),
            StateBall(pos=StatePosition(x=2, y=3), color="yellow"),
            StateBall(pos=StatePosition(x=1, y=4), color="yellow"),
        ]
    state = replace(get_default_state(), balls = balls)
    assert(sc.is_in_goal_state(state) == False)

    balls = [
            StateBall(pos=StatePosition(x=0, y=4), color="pink"),
            StateBall(pos=StatePosition(x=0, y=3), color="pink"),
            StateBall(pos=StatePosition(x=2, y=3), color="yellow"),
            StateBall(pos=StatePosition(x=2, y=4), color="yellow"),
        ]
    state = replace(get_default_state(), balls = balls)
    assert(sc.is_in_goal_state(state) == True)

def main():
    test_goal_state()

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"\n{__file__} executed in {elapsed:0.2f} seconds.")

