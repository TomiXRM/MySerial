
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


def printData():
    Ser = serial.Serial(serialPort, serialBaud, timeout = None)
    while(True):
        string_data = Ser.read()
        sys.stdout.write(str(string_data))
        # print(str(string_data),end="")
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
    print(fmt)
    printData()
