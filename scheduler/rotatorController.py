from scheduler.RotatorServices import rotator_services as rs
from scheduler.services import Services
from datetime import date, datetime, timedelta
from scheduler.models import NextPass, TLE, AzEl

import ephem

# from Ardurino_and_Py_demo_files.PTS import write_az_and_el
from time import sleep
import serial
from struct import *
from django import db


class rotator_controller():
	"""Controller for rotators:
	Take in next pass object which
					contains TLE object and start and end times of the pass
		"""

	# def __init__(self, nextPass):
	# 	super(rotator_controller, self).__init__()
	# 	self.nextPass = nextPass

	ser = None
	try:
		ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=2)
	except:
		print("Port Not Detected. Please connect rotators.")
		
	#changed to COM8 for Robbies Laptop
	#/dev/ttyACM0 for linux

	def normalizeAzEl(self, AzElList):
		over520 = False
		clockwise = False

		# plus180AzelList = Services.getAzElForPeriod(self, tleEntry, datetime(2017, 4, 14, 1, 13, 59),
		# 								 datetime(2017, 4, 14, 1, 21, 37), 1)

		plus180AzelList = AzElList

		for item in (plus180AzelList):
			item.azimuth = ephem.degrees(ephem.degrees(item.azimuth) + ephem.degrees('180:00:00'))
			#plus180AzelList.insert(i, item)
			if (ephem.degrees(item.azimuth) > ephem.degrees('520:00:00')):
				over520 = True

		# print(over520)

		firstItem = plus180AzelList[0]
		lastItem = plus180AzelList[len(plus180AzelList) - 1]
		thirItem = plus180AzelList[3]
		if (ephem.degrees(firstItem.azimuth)> ephem.degrees(thirItem.azimuth)):
			clockwise = True

		if (over520):
			if ((firstItem.azimuth > ephem.degrees('520:00:00')) and (lastItem.azimuth < ephem.degrees('360:00:00'))):
				if (clockwise):
					for i, item in enumerate(plus180AzelList):
						if ((item.azimuth) > ephem.degrees('360:00:00')):
							item.azimuth = ephem.degrees(item.azimuth - ephem.degrees('360:00:00'))
						elif (item.azimuth > ephem.degrees('520:00:00')):
							item.azimuth = ephem.degrees('180:00:00')

			if ((firstItem.azimuth < ephem.degrees('520:00:00')) and (lastItem.azimuth > ephem.degrees('360:00:00'))):
				for i, item in enumerate(plus180AzelList):
					if ((item.azimuth) > ephem.degrees('360:00:00')):
						item.azimuth = ephem.degrees(item.azimuth - ephem.degrees('360:00:00'))
					elif (item.azimuth > ephem.degrees('520:00:00')):
						item.azimuth = ephem.degrees('180:00:00')

		return plus180AzelList


	def moveRotators(self, nextPass):
		"""
				From the AzelForEachSecond function: send commands to rotators to move them.
		"""
		s = Services()

		tleEntry = TLE("1", 'EYESAT-1 (AO-27)',
                   '1 22825U 93061C   17011.87921041 -.00000014  00000-0  12008-4 0  9991',
                   '2 22825  98.7903 335.7306 0009458  70.2997 289.9204 14.29982572215061', )

   		#azelList = Services.getAzElForPeriod(self, tleEntry, datetime(2017, 4, 14, 1, 13, 59),
        #                                datetime(2017, 4, 14, 1, 21, 37), 1)
		
		azel = Services.getAzElForPeriod(self, nextPass.tle, nextPass.riseTime,
										 nextPass.setTime, 1)

		for item in azel:
			print(str(item.azimuth))
		print("---------")
		AzElList = self.normalizeAzEl(azel)
		for item in AzElList:
			print(str(item.azimuth))

		for item in AzElList:
			sleep(1)
			if(self.ser != None):
				while 1:
					self.ser.write(pack('BB', az, el))
					line = self.ser.readline()
					print(line)
					if (line == b'end'):
						print("break")
						#ser.close()
						break


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
		if(ser != None):
			while 1:
				self.ser.write(pack('BB', az, el))
				line = self.ser.readline()
				print(line)
				if (line == b'end'):
					print("break")
					#ser.close()
					break
