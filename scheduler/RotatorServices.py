import serial
import datetime as dt
"""
Created: 23/01/2017
Last modified: 23/01/2017
-------------------------

 Set and set the position of the ground station rotators: azimuth and elevation

 set_position: 
		The only difference between both commands is using 
		position 1 or 2 in the array for A and B and changing
		the az and el param input. 

		This could be broken down more to create less repeated code
		TODO: extract code more.
	
	***	May also not need this in a class format: seems like modules and functions are good enough here. ***
"""

#class rotator_services():

"""
Command format: 
	Elevation: 	"2BG<degrees>\r"  
	Azimuth: 	"2AG<degrees>\r"
"""
cmdArr = ["B","A","G"]
cmdStart = "\x02"
cmdEnd = "\r"

def write_elevation(el, ser):
	"""
	Write elevation commands for combi track
	using command Array, given elevation and serial port

	Not sure if serial port will work in this way: 
	If not, rebase to last commmit
	"""
	ser.write(cmdStart.encode())
	ser.write(cmdArr[0].encode())
	ser.write((cmdArr[-1] + str(el)).encode())
	ser.write(cmdEnd.encode())

def write_azimuth(az, ser):
	"""
	Write azimuth commands for combi track
	using command Array, given azimuth and serial port

	Not sure if serial port will work in this way: 
	If not, rebase to last commmit
	"""
	ser.write(cmdStart.encode())
	ser.write(cmdArr[1].encode())
	ser.write((cmdArr[-1] + str(az)).encode())
	ser.write(cmdEnd.encode())


def get_position():
	""" Get position of ground station: 
		azimuth and elevation
	"""
	ser = serial.Serial("COM2", 9600, timeout=2)  # open serial port: windows "COMN" 
											  # linux "/dev/ttyUSBn" where n is a number
	ser.portstr										  
	line = ser.read() 

	while(line != b''):
		print(line)
		line=ser.read()

	print("done")
	ser.close()

def set_position(az, el):
	""" Set position of ground station, 
		given azimuth and elevation
	"""
	ser = serial.Serial("COM2", 9600, timeout=2)  # open serial port: windows "COMN" 
											  # linux "/dev/ttyUSBn" where n is a number
	print(ser) # Baud rate info etc: for testing 
	print("writing to COM2")
	ser.flush()
	# Change elevation first
	write_elevation(el, ser)
	# Change azimuth
	write_azimuth(az, ser)
	print("done")
	ser.close()

start = dt.datetime.now()		
set_position(0, 0)
get_position()
end = dt.datetime.now()

time = end-start
print(time)



