# Open port at “9600,8,N,1”, no timeout:

import serial
import time


ser = serial.Serial("COM2", 9600, timeout=10)  # open serial port: windows "COMN" linux "/dev/ttyUSBn" where n is a number
ser.flushInput()
ser.flushOutput()
print(ser)

print("writing to COM2")

cmd = "2AG30\r\n".encode('ascii')
print("command: ", cmd)

ser.write(cmd)


ser.portstr
print("Done writing")


print("Reading response")

line = ser.read() 
#line.portstr
print(line)

print("done")
time.sleep(10)
ser.close()



"""

The above just imports the serial library and connects to the COM1 port, sets the port and then prints that out. 

output is: 
Serial<id=0x205f336be10, open=True>(port='COM1', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=None, 
xonxoff=False, rtscts=False, dsrdtr=False)

"""