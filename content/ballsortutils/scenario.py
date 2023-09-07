from state_update_model import StateModel


class Scenario(object):
    """Interface for a specific scenario"""

    def get_initial_state(self) -> StateModel:
        """Returns the initial state for the scenario."""
        raise NotImplementedError

    def is_in_goal_state(self, state: StateModel) -> bool:
        """Returns true only if state fulfills the goal state criteria."""
        raise NotImplementedError

    def get_goal_state_description(self) -> str:
        """Returns a natural language specification of goal state."""
        raise NotImplementedError
