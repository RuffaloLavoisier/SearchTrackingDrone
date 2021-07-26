import serial

ser = serial.Serial('/dev/ttyUSB0',9600)
i=9090.2
#i = i * 0.0001
#i="$"+str(i)+"^"
while True:

	ser.write(str(i).encode("utf-8"))
	#i=i+1
	read = ser.readline()
#	read = read.decode()[:2]
	print (str(read))
