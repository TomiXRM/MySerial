#!/usr/bin/env python2
# -*- coding: utf-8 -*-
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

fmt = 0  # format


def ask_for_port():

    sys.stderr.write("\n--- Available ports:\n")
    ports = []
    for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
        sys.stderr.write("--- {:2}: {:20} {!r}\n".format(n, port, desc))
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
        else:
            port = ports[index]
        return port


def ask_baud():
    baud = 230400
    if sys.version_info.major != 3:
        baud = raw_input("--- Enter baudrate: ")
    else:
        baud = input("--- Enter baudrate: ")

    try:
        sys.stdout.write("---  baudrate: ")
        sys.stdout.write(str(int(baud)))
        # print(int(baud))
    except ValueError:
        sys.stdout.write("230400")
        baud = 230400

    return baud


def ask_format():
    sys.stdout.write("\r\n--- bin:1  oct:2  dec:3  hex:4  ASCI:ENTER\r\n")
    if sys.version_info.major != 3:
        format = raw_input("--- Enter format: ")
    else:
        format = input("--- Enter format: ")
    return format


def printAscii(Ser):
    while True:

        if sys.version_info.major != 3:
            string_data = str(Ser.read())
            sys.stdout.write(string_data)
        else:
            string_data = Ser.read()
            sys.stdout.write(str(string_data))


def printBin(Ser):
    while True:

        if sys.version_info.major != 3:
            data = ord(Ser.read())
            sys.stdout.write(bin(data))
            sys.stdout.write("\n")
        else:
            data = ord(Ser.readline())
            print(str(string_data))


def printOct(Ser):
    while True:
        if sys.version_info.major != 3:
            for i in range(8):

                data = ord(Ser.read())
                sys.stdout.write(oct(data))
                sys.stdout.write(" ")
            sys.stdout.write("\n")
        else:
            for i in range(8):
                data = ord(Ser.readline())
                print(oct(data))
                print(" ")
            print("\n")


def printDec(Ser):
    while True:
        if sys.version_info.major != 3:
            data = ord(Ser.read())
            sys.stdout.write(str(data))
            sys.stdout.write("\n")
        else:
            data = ord(Ser.readline())
            print(str(data))
            print("\n")


def printHex(Ser):
    while True:
        if sys.version_info.major != 3:
            for i in range(8):
                string_data = ord(Ser.read())
                sys.stdout.write(hex(string_data))
                sys.stdout.write(" ")
            sys.stdout.write("\n")
        else:
            for i in range(8):
                string_data = ord(Ser.readline())
                print(hex(string_data))
                print(" ")
            sys.stdout.write("\n")


def printData():
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
