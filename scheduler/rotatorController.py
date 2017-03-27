from scheduler.RotatorServices import rotator_services
from scheduler.services import Services
from datetime import date, datetime, timedelta
from scheduler.models import NextPass, TLE, AzEl
from Ardurino_and_Py_demo_files.PTS import write_az_and_el
from time import sleep


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
            sleep(1)
            rs.set_position(item.elevation, item.azimuth)

    def sketchy_arduino_move():

        initAzim = 30
        initElev = 15
        lenOfPass = 45  # someRandomNumber
        azelList = []
        for item in range(lenOfPass):
            initElev += 1
            initAzim += 1

            azel = AzEl(azimuth=initAzim, elevation=initElev)
            azelList.append(azel)

        for item in azelList:
            sleep(1)
            write_az_and_el(item.azimuth, item.elevation)
