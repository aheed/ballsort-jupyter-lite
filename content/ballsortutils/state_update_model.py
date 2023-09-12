from dataclasses import dataclass

MIN_X = 0
MIN_Y = 0

@dataclass
class StatePosition:
    x: int
    y: int


@dataclass
class StateBall:
    pos: StatePosition
    color: str


@dataclass
class Claw:
    pos: StatePosition
    open: bool
    ball_color: str


@dataclass
class StateModel:
    max_x: int
    max_y: int
    balls: list[StateBall]
    claw: Claw
    isInGoalState: bool
    moving_horizontally: bool
    moving_vertically: bool
    operating_claw: bool


@dataclass
class StateUpdateModel:
    userId: str
    state: StateModel


def get_default_state() -> StateModel:
    return StateModel(
        max_x=3,
        max_y=4,
        balls=[StateBall(pos=StatePosition(x=2, y=4), color="blue")],
        claw=Claw(pos=StatePosition(x=0, y=0), open=True, ball_color=""),
        isInGoalState=False,
        moving_horizontally=False,
        moving_vertically=False,
        operating_claw=False
    )
