from ball_control_sim import BallControlSim
#from v1_update_reporter import V1UpdateReporter
#from ably_update_reporter import AblyUpdateReporter
#from ably_rest_update_reporter import AblyRestUpdateReporter
from postmessage_update_reporter import PostMessageUpdateReporter
#from dummy_ur import DummyUpdateReporter

def get_control_sim() -> BallControlSim:
    #reporter = V1UpdateReporter()
    #reporter = AblyUpdateReporter()
    #reporter = AblyRestUpdateReporter()
    reporter = PostMessageUpdateReporter()
    #reporter = DummyUpdateReporter()
    
    return BallControlSim(reporter)
