# import dependencies
import serial
import csv
import time
import msvcrt as m
import sys
import signal
import sys

# catch control c and exit gracefully
#def signal_handler(signal, frame):
    #if True:
        #break
#
    #print('You pressed Ctrl+C!')
    #time.sleep(4)
    #ser.write(b'\x03')
    ## close the arduino
    #ser.close()
    #print('Arduino Closed!')
    #sys.exit(0)


# in place of 'COM9', put whatever COM port the Arduino is connected to on this computer
def main(filename,port='COM3'):
    # initialize serial connection
    ser = serial.Serial(port,timeout=0.1)

    # Wait for arduino to come online
    while ser.read() != b'\x01':
        time.sleep(0.1)

    # Send a message to let arduino know to home the device
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
    count=0
    # main loop
    with open(filename) as csvfile:
        point_dict = csv.DictReader(csvfile)
        for row in csv.DictReader(csvfile):
            # The first line puts the motor in main position so the peg can be screwed in
            if count == 1:
                print('Press any key to start sequence')
                m.getch()
                print('Starting recording and peg sequence')
                # Send the start record signal from the arduino
                ser.write(b'\x02')
            else:
                # do not send the start record signal
                ser.write(b'\x00')

            # Wait for receipt signal
            while ser.read() != b'\x01':
                time.sleep(0.1)

            # =============================== #
            # ========= Send coords ========= # 
            # =============================== #


            # Send X coordinate and wait until arduino says it has been received
            ser.write(str(row['X']).encode('utf-8'))
            while ser.read() != b'\x01':
                time.sleep(0.1)

            # Send Y coordinate and wait until arduino says it has been received
            ser.write(str(row['Y']).encode('utf-8'))
            while ser.read() != b'\x01':
                time.sleep(0.1)

            # Send Mode and wait until arduino says it has been received
            ser.write(str(row['mode']).encode('utf-8'))
            while ser.read() != b'\x01':
                time.sleep(0.1)

            # =============================== #
            # ========= Update user ========= # 
            # =============================== #

            #Read the poosition at which the arduino believes it is
            for ii in range(4):
                msg = msg+ser.readline()
            print(msg.decode('utf-8'))
            # Wait until the arduino says it has finished moving the motors
            while ser.read() != b'\x02':
                time.sleep(0.1)

            # pause the peg at this position for the desired time if it is not
            # the first (Major) move
            if count>0:
                print('Pausing for {} seconds'.format(row['delay']))
                time.sleep(float(row['delay']))
            count+=1

        # Tell the arduino to send the record toggle to stop the recording
        ser.write(b'\x03')

        # close the arduino
        ser.close()
        print('Arduino Closed!')
        return(0)

if __name__ == '__main__':
    point_list = sys.argv[1]
    if len(sys.argv)>2:
    	com_port = sys.argv[2]
    else:
    	com_port = 'COM3'

    #signal.signal(signal.SIGINT, signal_handler)
    main(point_list,com_port)
