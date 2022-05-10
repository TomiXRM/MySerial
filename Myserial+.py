from cmath import nan
import sys
from time import sleep
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QPushButton, QTextEdit
from PyQt6 import QtCore

import serial
from serial.tools.list_ports import comports
import atexit
from datetime import datetime
import threading
import subprocess
import os
import csv
import configparser


inifile = configparser.ConfigParser()
inifile.read('./config.ini', 'UTF-8')
serialPort = inifile.get('Serial', 'port')
baud = int(inifile.get('Serial', 'baud'))
csv_directory = inifile.get('CSV', 'directory')
fileName = inifile.get('CSV', 'fileName')
fmt = inifile.get('Serial', 'fmt')

print("Default Setup", serialPort, baud, csv_directory, fileName, fmt)
print("You can change setup with open change 'config.ini'")


class Madoka(QWidget):
    global serialPort, baud, fmt

    def __init__(self):
        global serialPort, baud, fmt
        self.serialLogState = False
        self.fmts = ['bin', 'oct', 'dec', 'hex', 'csv', 'csv+', 'ascii']
        self.baudList = [4800, 7200, 9600, 14400,
                         19200, 28800, 38400, 57600, 76800, 115200, 230400, 460800, 921600, 1000000, 2000000, 4000000]
        fmt = self.fmts.index(fmt)
        super().__init__()
        layoutA = QHBoxLayout()

        self.baudBox = QComboBox()
        self.getBaud()
        layoutA.addWidget(self.baudBox)

        self.formatBox = QComboBox()
        self.getFormat()
        layoutA.addWidget(self.formatBox)

        layoutB = QHBoxLayout()
        self.portBox = QComboBox()
        self.getPorts()
        layoutB.addWidget(self.portBox)

        parentLayout = QVBoxLayout()
        parentLayout.addLayout(layoutB)
        parentLayout.addLayout(layoutA)

        self.setLayout(parentLayout)

        self.portBox.currentTextChanged.connect(self.portSelected)
        self.portBox.setCurrentIndex(len(self.ports)-1)

        self.baudBox.currentTextChanged.connect(self.baudSelected)
        try:
            self.baudBox.setCurrentIndex(self.baudList.index(baud))
        except:
            self.baudBox.setCurrentIndex(-1)

        self.formatBox.currentTextChanged.connect(self.formatSelected)
        self.formatBox.setCurrentIndex(fmt)

        self.button1 = QPushButton()
        self.button1.setText("start")
        self.button1.released.connect(self.btn1Clicked)
        layoutA.addWidget(self.button1)

    def portSelected(self, text):
        global serialPort
        if(text != ''):
            serialPort = self.ports[self.portsIndex.index(text)]
            # print(serialPort)
            # self.erandano.setText(self.port)

    def baudSelected(self, text):
        global baud
        if(text != ''):
            baud = text
            # print(baud)

    def formatSelected(self, text):
        global fmt
        if(text != ''):
            fmt = self.fmts.index(text)
            # print(text)

    def getPorts(self):
        global serialPort
        # sys.stderr.write("\n--- Available ports:\n")
        self.ports = []
        self.portsIndex = []
        for n, (port, desc, devid) in enumerate(sorted(comports()), 1):
            # sys.stderr.write("--- {:2}: {:20} {!r} \n".format(n, port, desc))
            self.ports.append(port)
            print(port)
            self.portsIndex.append("{:2}: {:20} {!r}".format(n, port, desc))
        try:
            serialPort = self.ports.index(serialPort)
        except:
            serialPort = self.ports[len(self.ports)-1]
        for s in self.portsIndex:
            self.portBox.addItem(s)

    def getBaud(self):
        for b in self.baudList:
            self.baudBox.addItem(str(b))

    def getFormat(self):
        global fmt
        for f in self.fmts:
            self.formatBox.addItem(f)

    def btn1Clicked(self):
        if(self.button1.text() == 'start'):
            self.baudBox.setDisabled(True)
            self.formatBox.setDisabled(True)
            self.button1.setText('stop')
            self.serialLogState = True
            th = threading.Thread(target=printData, daemon=True)
            th.start()
        elif(self.button1.text() == 'stop'):
            self.button1.setText('start')
            self.baudBox.setDisabled(False)
            self.formatBox.setDisabled(False)
            self.serialLogState = False
            # th.sleep()


def printAscii(Ser):
    while(mado.serialLogState):
        string_data = ''
        try:
            string_data = Ser.read().decode("utf-8")
            sys.stdout.write(string_data)
        except:
            pass


def printBin(Ser):
    while(mado.serialLogState):
        data = ''
        try:
            data = ord(Ser.read())
            sys.stdout.write(str(data)+" BIN:"+format(data, '#08b')+"\r\n")
        except:
            pass


def printOct(Ser):
    while(mado.serialLogState):
        data = ''
        try:
            data = ord(Ser.read())
            sys.stdout.write(str(data)+" OCT:"+oct(data)+"\r\n")
        except:
            pass


def printDec(Ser):
    while(mado.serialLogState):
        data = ''
        try:
            data = ord(Ser.read())
            sys.stdout.write(str(data)+" HEX:"+dec(data)+"\r\n")
        except:
            pass


def printHex(Ser):
    while(mado.serialLogState):
        data = ''
        try:
            data = ord(Ser.read())
            sys.stdout.write(str(data)+" DEC:"+hex(data)+"\r\n")
        except:
            pass


def printAsciiWithCSVOutput(Ser):
    global fileName
    fileName = csv_directory + fileName + \
        datetime.now().strftime("%Y%m%d-%H%M%S")+".csv"
    print(fileName)
    strLine = ""
    while (mado.serialLogState):
        bytes_data = Ser.read()
        string_data = ''
        try:
            string_data = bytes_data.decode("utf-8")
        except UnicodeDecodeError:
            string_data = ''
        sys.stdout.write(string_data)

        strLine += string_data
        if string_data == '\n':
            strLine = strLine.replace(':', ',').replace(
                ' ', ',').replace('\t', ',').replace('\r', '').replace('\n', '')
            # print(dataList) #リスト化されたやつ
            strLine = str(' Time:' +
                          datetime.now().strftime("%Y-%m-%d.%H:%M:%S.%f,"))+strLine
            addCSV(list(filter(None, strLine.split(','))))
            strLine = ''


def addCSV(list):
    with open(fileName, 'a', newline='') as data:
        csv.writer(data, lineterminator='\n').writerow(list)
        data.close()


def csvFinish():
    global fileName
    dict = {}
    maxlen = 0
    csvData = 0
    with open(fileName, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        l = [row for row in csvreader]
        maxlen = 0
        num = 0

        for i in range(10):
            # print(l[i+10])
            if(maxlen < len(l[i])):
                maxlen = len(l[i])

        # print("maxlen:" + str(maxlen))

        a = [[0]]*maxlen
        b = [[0]]*maxlen

        for i in range(maxlen):
            for j in range(20):
                try:
                    # print(l[j+10][i])
                    a = l[j+10][i]
                    b = l[j+11][i]
                    if(a == b):
                        if(a in dict):
                            dict[a]['count'] += 1
                        else:
                            dict[a] = {"row": i, "count": 1}
                except:
                    # print("error")
                    pass

            for key in list(dict):
                if(dict[key]['count'] < 18 or key == ''):
                    dict.pop(key)

            # pprint.pprint(dict)
        keyValue_GoingToRemove = []
        count = 0
        text = ','
        for key in range(maxlen):
            for key2 in list(dict):
                if(dict[key2]['row'] == key):
                    text += key2
                    keyValue_GoingToRemove.append(count)
                    if(key != maxlen-1):
                        text += ','
            count += 1
        text = text.split(',')
        # print(l[20])
        # print(text)
        # print("goint to remove", end='')
        # print(keyValue_GoingToRemove)

        with open(fileName, 'r') as csvfile:
            reader = csv.reader(csvfile)
            os.remove(fileName)
            with open(fileName, "w") as result:
                writer = csv.writer(result)
                writer.writerow(text)
                for r in reader:
                    count = 0
                    myList = []
                    for value in r:
                        if((count in keyValue_GoingToRemove) != True):
                            myList.append(value)
                        count += 1
                    # print(myList)
                    writer.writerow(myList)
    print("open "+fileName)


def exit():
    global fmt, fileName

    if(fmt == 4 or fmt == 5):
        csvFinish()
        print('csv finish')
    if(fmt == 5):
        result = subprocess.run('python graph.py '+fileName, shell=True)
        if result.returncode != 0:
            print("couldn't open file...")
    print("open "+fileName)
    print('----------------------------------------------')
    print('✨finish!!✨')


def printData():
    global serialPort, baud, fmt

    while(mado.serialLogState == False):
        pass
    try:
        Ser = serial.Serial(str(serialPort), baud, timeout=None)
        Ser.flushInput()
        Ser.flushOutput()
    except:
        pass

    if fmt == 0:  # bin
        printBin(Ser)
    elif fmt == 1:  # oct
        printOct(Ser)
    elif fmt == 2:  # dec
        printDec(Ser)
    elif fmt == 3:  # hex
        printHex(Ser)
    elif fmt == 4 or fmt == 5:  # csv
        printAsciiWithCSVOutput(Ser)
    else:  # ascii
        printAscii(Ser)
    Ser.flushInput()
    Ser.flushOutput()
    Ser.close()
    # Ser.close()


if __name__ == "__main__":
    atexit.register(exit)
    print(fmt)
    qAp = QApplication(sys.argv)
    mado = Madoka()
    mado.show()
    qAp.exec()
