import serial

ser = serial.Serial('COM1') 

while (1):
	s = ser.read(10)        # read up to ten bytes (timeout)
	line = ser.readline() 
	print(line)
