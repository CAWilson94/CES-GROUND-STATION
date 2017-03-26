import rotator_services as rs
from services import getAzElTLE
from datetime import date, datetime, timedelta
from models import NextPass


class rotator_controller(NextPass):
    """Controller for rotators:
                Take in next pass object which 
                contains TLE object and start and end times of the pass
    """

    def __init__(self, arg):
        super(rotator_controller, self).__init__()
        self.arg = arg

    def moveRotators(tleEntry):
    """ 
	From the AzelForEachSecond function: send commands to rotators to move them. 
    """
        azel = getAzElForPeriod(tleEntry, NextPass.riseTime,
                                NextPass.setTime, NextPass.period)


        rs.set_position(azel.elevation, azel.azimuth)
