
"""This script opens a .csv file in the format:

xxx.x,yyy.y,f
xxx.x,yyy.y,f
xxx.x,yyy.y,f

where x is the x coordinate (e.g. 100.2, 034.0, 001.5), y is the y coordinate (same formatting), and flag is an
integer (0 for normal stepping speed, 1 for microstepping).

It is critical in this version that the x and y
coordinates have 3 digits, followed by a period, followed by one more digit.

Version: Python 3
Packages required: PySerial
"""

# import dependencies
import serial
import csv
import time
import msvcrt as m
def wait():
    m.getch()

# in place of 'COM9', put whatever COM port the Arduino is connected to on this computer
port = 'COM3'

# initialize serial connection
ser = serial.Serial(port,timeout=0.1)
time.sleep(2)
ser.write('H'.encode('utf-8'))
while True:
	msg = ser.read()
	if msg == b'\x00':
		print("Connected. Homing...")
	elif msg == b'\x01':
		print('Homed!')
		break
	else:
		time.sleep(0.1)


time.sleep(0.5)
# set up main loop
# list to contain descriptions of flags

filename = r'C:\Users\camera_2\Desktop\test.csv'


count=0
# main loop
with open(filename) as csvfile:
	point_dict = csv.DictReader(csvfile)
	for row in csv.DictReader(csvfile):
		# The first line puts the motor in main position so the peg can be screwed in
		if count == 1:
			print('Press any key to start sequence')
			wait()
		
		# Send X coordinate and wait until arduino says it has been received
		ser.write(str(row['X']).encode('utf-8'))
		# print('Sent X: {}'.format(row['X']))
		while not ser.read() == b'\x01':
			time.sleep(0.1)
		# Send Y coordinate and wait until arduino says it has been received
		ser.write(str(row['Y']).encode('utf-8'))
		# print('Sent Y: {}'.format(row['Y']))
		while not ser.read() == b'\x01':
			time.sleep(0.1)
		# Send Mode and wait until arduino says it has been received
		ser.write(str(row['mode']).encode('utf-8'))
		# print('Sent mode: {}'.format(row['mode']))
		while not ser.read() == b'\x01':
			time.sleep(0.1)

		#Read the poosition at which the arduino believes it is
		for ii in range(4):
			msg = msg+ser.readline()
		print(msg.decode('utf-8'))
		# Wait until the arduino says it has finished moving the motors
		while True:
			msg = ser.read()
			if msg == b'\x02':
				break
		if count>0:
			print('Pausing for {} seconds'.format(row['delay']))
			time.sleep(float(row['delay']))
		count+=1
		
	ser.close()
	print('Arduino Closed!')
