import asyncio
import sys

sys.path.append("../content/ballsortutils")

from ball_control import BallControl
from state_update_model import StatePosition

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
