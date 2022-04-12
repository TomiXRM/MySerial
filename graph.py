# -*- coding: utf-8 -*-
"""
Demonstrates some customized mouse interaction by drawing a crosshair that follows 
the mouse.


"""

# Add path to library (just for examples; you do not need this)
# import initExample
import pandas as pd
from pyqtgraph.Point import Point
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import sys
file = "/Users/tomixrm/Desktop/datalog20220411-192102.csv"


c = '#0CC9D3'
m = '#EC2BAB'
y = '#E8BC1C'
r = '#EC516B'
g = '#00D970'
b = '#008EFF'
v = '#8756EC'


args = sys.argv
if len(args) > 1:
    file = str(args[1])
    print(file)
# generate layout
app = pg.mkQApp("Myserial graph")
win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('Myserial graph')
label = pg.LabelItem(justify='right')
win.addItem(label)
win.setBackground('w')
p1 = win.addPlot(row=1, col=0)
p2 = win.addPlot(row=2, col=0)

region = pg.LinearRegionItem()
region.setZValue(10)
# Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this
# item when doing auto-range calculations.
p2.addItem(region, ignoreBounds=True)

# pg.dbg()
p1.setAutoVisible(y=True)


# create numpy arrays
# make the numbers large to show that the range shows data from 10000 to all the way 0
df = pd.read_csv(file)
# 非数値の列のみ選択
df = df.select_dtypes(include='number')
colors = [c, m, y, r, g, b, v]
columnlist = df.columns
qty = 0
for col in columnlist:
    if(qty <= len(colors)-1):
        p1.plot(df[col], pen=pg.mkPen(colors[qty], width=1))
        p2d = p2.plot(df[col], pen=pg.mkPen(colors[qty], width=1))
        # bound the LinearRegionItem to the plotted data
        region.setClipItem(p2d)
        qty += 1
    else:
        qty = 0


def update():
    region.setZValue(10)
    minX, maxX = region.getRegion()
    p1.setXRange(minX, maxX, padding=0)


region.sigRegionChanged.connect(update)


def updateRegion(window, viewRange):
    rgn = viewRange[0]
    region.setRegion(rgn)


p1.sigRangeChanged.connect(updateRegion)

region.setRegion([100, 400])

# cross hair
vLine = pg.InfiniteLine(angle=90, movable=False)
hLine = pg.InfiniteLine(angle=0, movable=False)
p1.addItem(vLine, ignoreBounds=True)
p1.addItem(hLine, ignoreBounds=True)


vb = p1.vb


def mouseMoved(evt):
    pos = evt[0]  # using signal proxy turns original arguments into a tuple
    if p1.sceneBoundingRect().contains(pos):
        mousePoint = vb.mapSceneToView(pos)
        index = int(mousePoint.x())

        for col in columnlist:
            if index > 0 and index < len(df[col]):
                label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" %
                              (mousePoint.x(), df[col][index], df[col][index]))

        vLine.setPos(mousePoint.x())
        hLine.setPos(mousePoint.y())


proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
# p1.scene().sigMouseMoved.connect(mouseMoved)


if __name__ == '__main__':
    pg.exec()
