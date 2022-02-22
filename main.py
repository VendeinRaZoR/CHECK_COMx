#!/usr/bin/python
# coding=utf-8

import sys #for args
import serial #for serial COM port
import time #for COM port speed calculation
from termcolor import colored #for color words in terminal

SERIAL_SPEED = 115200 #serial COM port current speed
SERIAL_TIMEOUT = 1 #serial COM port timeout
TESTWORD="symbols from 0 to 255"
#all procedures in main function
def main(args):
    if(len(args) == 1): #if we haven't any arguments
        print "Wrong arguments! Type sudo -E comCheck.py tty*"
        return
    #initializaton of serial COM port (UART)
    serialPort = serial.Serial("/dev/" + args[1],SERIAL_SPEED,timeout=SERIAL_TIMEOUT)

    print "Checking RX/TX lines..."
    print "Trying to send " + TESTWORD
    x = range(0,255) #symbols to send
    currTime = time.time() #get current time for deltaTime calculation
    serialPort.write(x) #write symbols into COM port
    readData = serialPort.read(255) #on last symbol speed 200-300 bod
    deltaTime = time.time() - currTime #deltaTime between send and receive
    print "Trancieve RX/TX time " + str(deltaTime)
    print "Tranceive real speed " + str(int(255/deltaTime))
    if(readData != ''.join(chr(i) for i in x)): #if we don't get equal values
        print "RX/TX not connected on " + args[1] + " port"
        print "Get [" + readData + "] from RX instead \n[" + ''.join(chr(i) for i in x) + "]\n" + colored(" FAILED","red")
    else:
        print "Get [" + readData + "]\n" + colored(" SUCCEEDED","green")
        print "RX/TX connected successfully"

    print "Checking DSR/DTR/CD lines..."
    print "Set DTR value '1'"
    serialPort.setDTR(1) #set DTR signal on COM port
    dtrValue = serialPort.getDSR() & serialPort.getCD() #received DTR value on DSR (shorted)
    if (dtrValue == 1):
        print "DSR/DTR/CD test '1'" + colored(" SUCCEEDED","green")
    else:
        print "DSR/DTR/CD test '1'" + colored(" FAILED","red")
    print "Set DTR value '0'"
    serialPort.setDTR(0) #analogue like before
    dtrValue = serialPort.getDSR() & serialPort.getCD()
    if (dtrValue == 0):
        print "DSR/DTR/CD test '0'" + colored(" SUCCEEDED","green")
    else:
        print "DSR/DTR/CD test '0'" + colored(" FAILED","red")

    print "Checking RTS/CTS lines..."
    print "Set RTS value '1'"
    serialPort.setRTS(1) #set RTS signal (RTS and CTS shorted)
    rtsValue = serialPort.getCTS() #get RTS value on CTS signal on COM port
    if (rtsValue == 1):
        print "RTS/CTS test '1'" + colored(" SUCCEEDED","green")
    else:
        print "RTS/CTS test '1'" + colored(" FAILED","red")
    print "Set RTS value '0'"
    serialPort.setRTS(0)
    rtsValue = serialPort.getCTS()
    if (rtsValue == 0):
        print "RTS/CTS test '0'" + colored(" SUCCEEDED","green")
    else:
        print "RTS/CTS test '0'" + colored(" FAILED","red")

    serialPort.close() #close serial COM port

# Press the green button in the gutter to run the script.
if __name__ == '__main__': #access point of script
    main(sys.argv) #main function
