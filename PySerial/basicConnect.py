# Open port at “9600,8,N,1”, no timeout:

import serial

ser = serial.Serial('COM1')  # open serial port: windows "COMN" linux "/dev/ttyUSBn" where n is a numbe
ser.write(str(10128).encode())
ser.portstr
print(ser)


print("yer maw")

line = ser.read(10) 
print(line)

print("done")

ser.close()



"""

The above just imports the serial library and connects to the COM1 port, sets the port and then prints that out. 

output is: 
Serial<id=0x205f336be10, open=True>(port='COM1', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=None, 
xonxoff=False, rtscts=False, dsrdtr=False)

"""