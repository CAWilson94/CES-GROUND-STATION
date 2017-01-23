import requests
import serial
import time

"""
 Set and set the position of the ground station rotators: azimuth and elevation

"""

class rotator_services():

	ser = serial.Serial("COM2", 9600, timeout=2)  # open serial port: windows "COMN" 
												  # linux "/dev/ttyUSBn" where n is a number
	
	def get_position():
		""" Get position of ground station: 
			azimuth and elevation
		"""

	def set_position(az, el):
		""" Set position of ground station, 
			given azimuth and elevation
		"""