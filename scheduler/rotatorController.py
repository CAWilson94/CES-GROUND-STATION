from RotatorServices import rotator_services
import services
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
        azel = services.getAzElForPeriod(tleEntry, NextPass.riseTime,
                                         NextPass.setTime, NextPass.period)
        rs.set_position(azel.elevation, azel.azimuth)


tleEntry = TLE('0', 'PROMETHEUS 2-3',
               '1 41855U 16067H   17017.17439223 -.00000035  00000-0  22910-5 0  9998',
               '2 41855  97.9660  92.6242 0012070  83.3470 276.9124 14.95885483  9917', )

azelList = Services.getAzElForPeriod(self, tleEntry, datetime(2017, 6, 6, 12, 2, 42),
                                     datetime(2017, 6, 6, 12, 9, 2), 30)

for item in azel:
    print(item.elevation + " : is elevation ")
