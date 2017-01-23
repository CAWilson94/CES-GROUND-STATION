import requests
import serial
import time

"""
 Set and set the position of the ground station rotators: azimuth and elevation

"""

class rotator_services():

	
	
	def get_position():
		""" Get position of ground station: 
			azimuth and elevation
		"""
		ser = serial.Serial("COM2", 9600, timeout=2)  # open serial port: windows "COMN" 
												  # linux "/dev/ttyUSBn" where n is a number

	def set_position(az, el):
		""" Set position of ground station, 
			given azimuth and elevation
		"""
		ser = serial.Serial("COM2", 9600, timeout=2)  # open serial port: windows "COMN" 
												  # linux "/dev/ttyUSBn" where n is a number
		print(ser) # Baud rate info etc: for testing 
		print("writing to COM2")
		ser.flush()
		"""
		Command format: 
				Elevation: 	"2BG<degrees>\r"  
				Azimuth: 	"2AG<degrees>\r"
		"""
		cmdArr = ["\x02","B","A","G","\r"]
		# Change elevation first
		ser.write(cmdArr[0].encode())
		ser.write(cmdArr[1].encode())
		ser.write((cmdArr[-2] + el).encode())
		ser.write(cmdArr[-1].encode())
		# Change azimuth
		ser.write(cmdArr[0].encode())
		ser.write(cmdArr[2].encode())
		ser.write((cmdArr[-2] + az).encode())
		ser.write(cmdArr[-1].encode())

		print("done")
		ser.close()

		"""
		The only difference between both commands is using 
		position 1 or 2 in the array for A and B and changing
		the az and el param input. 

		This could be broken down more to create less repeated code
		TODO: extract code more.

		"""