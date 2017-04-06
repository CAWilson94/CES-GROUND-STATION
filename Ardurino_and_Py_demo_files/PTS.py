import time
import serial
from struct import *


"ser.write(pack('\x02','B','G180','\r'))http://arduino.stackexchange.com/questions/9627/send-multiple-int-values-from-python-to-arduino-using-pyserial"
ser = serial.Serial('COM3', baudrate=9600, timeout=2)  # Establish the connection on a specific port


def write_az_and_el(az, el):
    """
    Write Azimuth and Elevation
    Values can not be more than 180 because rotator's range is 0-180
    Therefore, if the value is more than 180 write it's modulo
    """

    print(str(az) + " : " + str(el))
    if(az>180):
        az = az % 180
    if(el>180):
        el = el % 180

    #Use a loop that waights whrites the as and el values until it gets an "answer" from the ardurino.
    #A few times it failed to send the values over to the Ardurino side, that's why I use a loop.
    while 1:
        ser.write(pack('BB', az, el))
        line = ser.readline()
        print(line)
        if (line == b'end'):
            print("break")
            #ser.close()
            break

write_az_and_el(0, 0)
#time.sleep(1)
write_az_and_el(30, 30)
#time.sleep(1)
write_az_and_el(60, 60)
#time.sleep(1)
write_az_and_el(90, 90)
#time.sleep(1)
write_az_and_el(120, 120)
#time.sleep(1)
write_az_and_el(150, 150)
#time.sleep(1)
write_az_and_el(180, 180)
#time.sleep(1)
write_az_and_el(210, 210)
#time.sleep(1)
