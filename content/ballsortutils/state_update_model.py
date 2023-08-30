from dataclasses import dataclass


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


@dataclass
class StateModel:
    nofRows: int
    nofCols: int
    balls: list[StateBall]
    claw: Claw


@dataclass
class StateUpdateModel:
    userId: str
    state: StateModel


def get_default_state() -> StateModel:
    return StateModel(
        nofRows=4,
        nofCols=5,
        balls=[StateBall(pos=StatePosition(x=3, y=4), color="blue")],
        claw=Claw(pos=StatePosition(x=0, y=0), open=True),
    )
