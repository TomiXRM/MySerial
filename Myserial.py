#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from curses import baudrate
# from email.policy import default

import sys

import serial
from serial.tools.list_ports import comports
from serial.tools import hexlify_codec

fmt = 0  # format
default_baud = 1000000


def ask_for_port():

    sys.stderr.write("\n--- Available ports:\n")
    ports = []
    for n, (port, desc, devid) in enumerate(sorted(comports()), 1):
        sys.stderr.write(
            "--- {:2}: {:20} {!r} \n".format(n, port, desc))
        ports.append(port)
    while True:
        if sys.version_info.major != 3:
            port = raw_input("--- Enter port index or full name: ")
        else:
            port = input("--- Enter port index or full name: ")
        try:
            index = int(port) - 1
            if not 0 <= index < len(ports):
                sys.stderr.write("--- Invalid index!\n")
                continue
        except ValueError:
            #     pass
            port = ports[len(ports)-1]
            sys.stderr.write("---  Use: "+str(ports[len(ports)-1])+"\n")
        else:
            port = ports[index]
            sys.stderr.write("---  Use: "+str(ports[index])+"\n")
        return port


def ask_baud():
    baud = default_baud
    if sys.version_info.major != 3:
        baud = raw_input("--- Enter baudrate: ")
    else:
        baud = input("--- Enter baudrate: ")

    try:
        sys.stdout.write("---  baudrate: ")
        sys.stdout.write(str(int(baud)))
        # print(int(baud))
    except ValueError:
        sys.stdout.write("default:"+str(default_baud)+"\r\n")
        baud = default_baud

    return baud


def ask_format():
    sys.stdout.write("--- bin:1  oct:2  dec:3  hex:4  ASCI:ENTER\r\n")
    if sys.version_info.major != 3:
        format = raw_input("--- Enter format: ")
    else:
        format = input("--- Enter format: ")
    return int(format)


def printAscii(Ser):
    while True:
        if sys.version_info.major != 3:
            string_data = str(Ser.read())
            sys.stdout.write(string_data)
        else:
            bytes_data = Ser.read()
            string_data = bytes_data.decode("utf-8")
            sys.stdout.write(str(string_data))


def printBin(Ser):
    while True:
        if sys.version_info.major != 3:
            data = ord(Ser.read())
            sys.stdout.write(str(data)+" BIN:"+format(data, '#08b')+"\r\n")
        else:
            data = ord(Ser.read())
            print(str(data)+" BIN:"+format(data, '#08b')+"\r\n")


def printOct(Ser):
    while True:
        if sys.version_info.major != 3:
            data = ord(Ser.read())
            sys.stdout.write(str(data)+" OCT:"+format(data, '#08o')+"\r\n")
        else:
            data = ord(Ser.read())
            print(format(str(data)+" OCT:"+format(data, '#08o')+"\r\n"))


def printDec(Ser):
    while True:
        if sys.version_info.major != 3:
            data = ord(Ser.read())
            sys.stdout.write(str(data)+" DEC:"+format(data, '#08d')+"\r\n")
        else:
            data = ord(Ser.read())
            print(str(data)+" DEC:"+format(data, '#08d')+"\r\n")


def printHex(Ser):
    while True:
        if sys.version_info.major != 3:
            data = ord(Ser.read())
            sys.stdout.write(str(data)+" HEX:"+format(data, '#08x')+"\r\n")
        else:
            data = ord(Ser.read())
            print(str(data)+" HEX:"+format(data, '#08x')+"\r\n")


def printData():
    global fmt
    Ser = serial.Serial(serialPort, serialBaud, timeout=None)
    if fmt == 1:  # bin
        printBin(Ser)
    elif fmt == 2:  # oct
        printOct(Ser)
    elif fmt == 3:  # dec
        printDec(Ser)
    elif fmt == 4:  # hex
        printHex(Ser)
    else:  # ascii
        printAscii(Ser)
    Ser.close()


def parseArgs():
    global fmt
    args = sys.argv
    if len(args) > 1:
        if args[1] == "bin":
            fmt = 1
        elif args[1] == "oct":
            fmt = 2
        elif args[1] == "dec":
            fmt = 3
        elif args[1] == "hex":
            fmt = 4
        else:
            fmt = 0


if __name__ == "__main__":
    parseArgs()
    serialPort = ask_for_port()
    serialBaud = ask_baud()
    fmt = ask_format()
    printData()
