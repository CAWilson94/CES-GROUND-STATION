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

		print(ser)
		print("writing to COM2")
		"""
		Command format: 
				Elevation: 	"2BG<degrees>\r"  
				Azimuth: 	"2AG<degrees>\r"
		"""
		cmdArr = ["\x02","B","A","G","\r"]
		# Change elevation first
		cmdE = "2BG60\n".encode('ascii')
		# Change azimuth second
		cmdA = "2AG60\n".encode('ascii')
		ser.flush()
		"""
		Need each part of the command in an array so 
		it can be written one section at a time: 
		pySerial doesn't seem to work with one string command
		"""
