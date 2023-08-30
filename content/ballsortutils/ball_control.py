class IllegalBallControlStateError(Exception):
    "Raised when a control command is issued while a command for movement along the same axis is still being executed"
    pass

class BallControl(object):
    """Interface for controlling a ball manipulator in a grid"""

    async def __aenter__(self):
        pass
    
    async def __aexit__(self, *_):
        pass

    async def move_relative(self, x: int, y: int = 0):
        """Move the manipulator arm"""
        pass

    async def move_horizontally(self, distance: int):
        """Move the manipulator arm horizontally"""
        pass

    async def move_vertically(self, distance: int):
        """Move the manipulator arm vertically"""
        pass

    async def open_claw(self):
        pass

    async def close_claw(self):
        pass
            
    def move_horizontally_sync(self, distance: int):
        """Move the manipulator arm horizontally"""
        pass
    
    def move_vertically_sync(self, distance: int):
        """Move the manipulator arm vertically"""
        pass

    def move_relative_sync(self, x: int, y: int = 0):
        """Move the manipulator arm"""
        pass

    def get_position(self) -> tuple[int, int]: # type: ignore
        pass
