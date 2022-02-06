#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys

import atexit
import csv
import time
from datetime import datetime

import serial
from serial.tools.list_ports import comports


fmt = 0  # format:1 bin:2 oct:3 dec:4 hex:5 csvexport:6
default_baud = 1000000  # baudrate
csv_directory = ''  # CSVファイルの保存先
fileName = 'datalog'   # CSVファイルの保存名を決定


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
        sys.stdout.write(str(baud)+"\r\n")
        baud = int(baud)
    except ValueError:
        sys.stdout.write("default:"+str(default_baud)+"\r\n")
        baud = default_baud

    return baud


def ask_format():
    global fmt
    if fmt == 0:
        sys.stdout.write(
            "--- bin:1  oct:2  dec:3  hex:4  makecsv:5 ASCI:ENTER\r\n")
        if sys.version_info.major != 3:
            format = raw_input("--- Enter format: ")
        else:
            format = input("--- Enter format: ")
        try:
            fmt = int(format)
            if not 1 <= fmt <= 5:
                sys.stderr.write("--- Invalid format!\n")
                fmt = 0  # format
        except ValueError:
            fmt = 0  # format
        return format
    else:
        return fmt


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
            sys.stdout.write(str(data)+" OCT:"+oct(data)+"\r\n")
        else:
            data = ord(Ser.read())
            print(format(str(data)+" OCT:"+oct(data)+"\r\n"))


def printDec(Ser):
    while True:
        if sys.version_info.major != 3:
            data = ord(Ser.read())
            sys.stdout.write(str(data)+" DEC:"+dec(data)+"\r\n")
        else:
            data = ord(Ser.read())
            print(str(data)+" DEC:"+dec(data)+"\r\n")


def printHex(Ser):
    while True:
        if sys.version_info.major != 3:
            data = ord(Ser.read())
            sys.stdout.write(str(data)+" HEX:"+hex(data)+"\r\n")
        else:
            data = ord(Ser.read())
            print(str(data)+" HEX:"+hex(data)+"\r\n")


def printAsciiWithCSVOutput(Ser):
    global fileName
    fileName = csv_directory + fileName + \
        datetime.now().strftime("%Y%m%d-%H%M%S")+".csv"
    print(fileName)
    strLine = ""
    while True:
        if sys.version_info.major != 3:
            bytes_data = Ser.read()
        else:
            bytes_data = Ser.read()
            string_data = bytes_data.decode("utf-8")
            sys.stdout.write(string_data)
            strLine += string_data
            if string_data == '\n':
                strLine = str(' Time:' +
                              datetime.now().strftime("%Y%m%d.%H%M%S"))+strLine
                strLine = strLine.replace(':', ',').replace(
                    ' ', ',').replace('\t', ',').replace('\r', '').replace('\n', '')
                dataList = strLine.split(',')
                # print(dataList) #リスト化されたやつ
                addCSV(dataList)
                strLine = ''


def addCSV(list):
    global csv_directory
    with open(fileName, 'a', newline='') as data:
        csv.writer(data, lineterminator='\n').writerow(list)
        data.close()


def exit():
    global Ser
    print('----------------------------------------------')
    print('✨finish!!✨')
    Ser.close()


def printData():
    global fmt
    global Ser
    global serialBaud
    global serialPort
    Ser = serial.Serial(serialPort, serialBaud, timeout=None)
    if fmt == 1:  # bin
        printBin(Ser)
    elif fmt == 2:  # oct
        printOct(Ser)
    elif fmt == 3:  # dec
        printDec(Ser)
    elif fmt == 4:  # hex
        printHex(Ser)
    elif fmt == 5:  # csv
        printAsciiWithCSVOutput(Ser)
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
        elif args[1] == "csv":
            fmt = 5
        else:
            fmt = 0


if __name__ == "__main__":
    atexit.register(exit)
    parseArgs()
    serialPort = ask_for_port()
    serialBaud = ask_baud()
#     fmt = ask_format()
    printData()
