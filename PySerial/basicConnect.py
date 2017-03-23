# Open port at “9600,8,N,1”, no timeout:

import serial
import time


ser = serial.Serial("COM2", 9600, timeout=2)  # open serial port: windows "COMN" linux "/dev/ttyUSBn" where n is a number

print(ser)

print("writing to COM2")

cmd = "2BG60\n".encode('ascii')
print("command: ", cmd)
ser.flush()



ser.write("\x02".encode())
ser.write("B".encode())
ser.write("G400".encode())
ser.write("\r".encode())

ser.write("\x02".encode())
ser.write("A".encode())
ser.write("G00".encode())
ser.write("\r".encode())



ser.portstr
print("Done writing")


print("Reading response")

line = ser.read() 

while(line != b''):
	print(line)
	line=ser.read()



print("done")

ser.close()



"""

The above just imports the serial library and connects to the COM1 port, sets the port and then prints that out. 

output is: 
Serial<id=0x205f336be10, open=True>(port='COM1', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=None, 
xonxoff=False, rtscts=False, dsrdtr=False)

"""