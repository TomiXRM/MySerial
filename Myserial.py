from __future__ import absolute_import

import codecs
import os
import sys
import threading
import sys
from enum import Enum

import serial
from serial.tools.list_ports import comports
from serial.tools import hexlify_codec
fmt=0


def ask_for_port():

    sys.stderr.write('\n--- Available ports:\n')
    ports = []
    for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
        sys.stderr.write('--- {:2}: {:20} {!r}\n'.format(n, port, desc))
        ports.append(port)
    while True:
        port = raw_input('--- Enter port index or full name: ')
        try:
            index = int(port) - 1
            if not 0 <= index < len(ports):
                sys.stderr.write('--- Invalid index!\n')
                continue
        except ValueError:
            pass
        else:
            port = ports[index]
        return port

def ask_baud():
    baud = raw_input('--- Enter baudrate: ')
    return baud


def ask_format():
    sys.stdout.write("\r\n\r\n--- bin:1  oct:2  dec:3  hex:4  ASCI:ENTER\r\n")
    format = raw_input("--- Enter format: ")
    return format
def printAscii(Ser):
    while(True):
        string_data = Ser.read()
        sys.stdout.write(str(string_data))

def printBin(Ser):
    while(True):
        data = ord(Ser.read())
        sys.stdout.write(bin(data))
        sys.stdout.write("\n")

def printOct(Ser):
    while(True):
        for i in range(8):
            data = ord(Ser.read())
            sys.stdout.write(oct(data))
            sys.stdout.write(" ")
        sys.stdout.write("\n")


def printDec(Ser):
    while(True):
        data = ord(Ser.read())
        sys.stdout.write(str(data))
        sys.stdout.write("\n")


def printHex(Ser):
    while(True):
        for i in range(8):
            string_data = ord(Ser.read())
            sys.stdout.write(hex(string_data))
            sys.stdout.write(" ")
        sys.stdout.write("\n")



def printData():
    Ser = serial.Serial(serialPort, serialBaud, timeout = None)

    if fmt==1: # bin
        printBin(Ser)
    elif fmt==2: # oct
        printOct(Ser)
    elif fmt==3: # dec
        printDec(Ser)
    elif fmt==4: # hex
        printHex(Ser)
    else: # ascii
        printAscii(Ser)
    Ser.close()


def parseArgs():
    global fmt
    args=sys.argv
    if len(args)>1:
        if args[1]=='bin':
            fmt=1
        elif args[1]=='oct':
            fmt=2
        elif args[1]=='dec':
            fmt=3
        elif args[1]=='hex':
            fmt=4
        else :
            fmt=0


if __name__ == "__main__":
    parseArgs()
    serialPort = ask_for_port()
    serialBaud = ask_baud()
    fmt = ask_format()
    printData()
