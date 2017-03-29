from scheduler.RotatorServices import rotator_services
from scheduler.services import Services
from datetime import date, datetime, timedelta
from scheduler.models import NextPass, TLE, AzEl
# from Ardurino_and_Py_demo_files.PTS import write_az_and_el
from time import sleep
import serial
from struct import *


class rotator_controller():
    """Controller for rotators:
    Take in next pass object which
                    contains TLE object and start and end times of the pass
        """

    def __init__(self, nextPass):
        super(rotator_controller, self).__init__()
        self.nextPass = nextPass


    ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=2)
    #changed to COM8 for Robbies Laptop
    #/dev/ttyACM0 for linux

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


    def sketchy_arduino_move(self):

        initAzim = 0
        initElev = 0
        lenOfPass = 45  # someRandomNumber
        azelList = []

        for item in range(lenOfPass):
            azel = AzEl(azimuth=initAzim, elevation=initElev)
            initElev += 10
            initAzim += 10
            print(azel)
            azelList.append(azel)

        for item in azelList:
            sleep(1)
            self.write_az_and_el(item.azimuth, item.elevation)


    def write_az_and_el(self,az, el):
        """
        Write Azimuth and Elevation
        Values can not be more than 180 because rotator's range is 0-180
        Therefore, if the value is more than 180 write it's modulo
        """

        print("Actual input - " + str(az) + " : " + str(el))
        if (az > 180):
            az = az % 180
        if (el > 180):
            el = el % 180
        print("Servo position - " + str(az) + " : " + str(el))
        # Use a loop that waights whrites the as and el values until it gets an "answer" from the ardurino.
        # A few times it failed to send the values over to the Ardurino side, that's why I use a loop.
        while 1:
            self.ser.write(pack('BB', az, el))
            line = self.ser.readline()
            print(line)
            if (line == b'end'):
                print("break")
                #ser.close()
                break
