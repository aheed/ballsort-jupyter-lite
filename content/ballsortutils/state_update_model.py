from dataclasses import dataclass

MIN_X = 0
MIN_Y = 0
MAX_X = 3
MAX_Y = 4

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
    nofRows: int
    nofCols: int
    balls: list[StateBall]
    claw: Claw
    isInGoalState: bool


@dataclass
class StateUpdateModel:
    userId: str
    state: StateModel


def get_default_state() -> StateModel:
    return StateModel(
        nofRows=4,
        nofCols=5,
        balls=[StateBall(pos=StatePosition(x=2, y=4), color="blue")],
        claw=Claw(pos=StatePosition(x=0, y=0), open=True, ball_color=""),
        isInGoalState=False
    )
