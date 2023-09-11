from ball_control_ch2 import BallControlCh2
from ball_control_sim import BallControlSim
#from v1_update_reporter import V1UpdateReporter
#from ably_update_reporter import AblyUpdateReporter
#from ably_rest_update_reporter import AblyRestUpdateReporter
from postmessage_update_reporter import PostMessageUpdateReporter
#from dummy_ur import DummyUpdateReporter

def get_control_sim(delay_multiplier: float = 1.0) -> BallControlSim:
    #reporter = V1UpdateReporter()
    #reporter = AblyUpdateReporter()
    #reporter = AblyRestUpdateReporter()
    reporter = PostMessageUpdateReporter()
    #reporter = DummyUpdateReporter()
    
    return BallControlSim(update_reporter=reporter, delay_multiplier=delay_multiplier)

def get_ch2_control_sim(delay_multiplier: float = 1.0) -> BallControlSim:
    reporter = PostMessageUpdateReporter()
    return BallControlCh2(update_reporter=reporter, delay_multiplier=delay_multiplier)
