from scheduler.RotatorServices import rotator_services
from scheduler.services import Services
from datetime import date, datetime, timedelta
from scheduler.models import NextPass, TLE


class rotator_controller():
    """Controller for rotators:
                Take in next pass object which
                contains TLE object and start and end times of the pass
    """

    def __init__(self, nextPass):
        super(rotator_controller, self).__init__()
        self.nextPass = nextPass

    def moveRotators(tleEntry):
        """
                From the AzelForEachSecond function: send commands to rotators to move them.
        """
        s = Services()

        azel = Services.getAzElForPeriod(self, tleEntry, nextPass.riseTime,
                                         nextPass.setTime, nextPass.period)
        for item in azel:
            # wait?
            rs.set_position(item.elevation, item.azimuth)
