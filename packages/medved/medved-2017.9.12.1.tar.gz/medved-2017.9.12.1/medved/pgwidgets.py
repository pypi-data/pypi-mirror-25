#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg


class ImageView(pg.ImageView):
    def __init__(self, *args, **kwargs):
        super(ImageView, self).__init__(*args, **kwargs)
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
        color = QtGui.QColor(255, 0, 0, 150)
        self.varea = QtWidgets.QGraphicsRectItem(0, 0, 1, 1)
        self.varea.setPen(QtGui.QPen(color))
        self.varea.setBrush(QtGui.QBrush(color))
        self.harea = QtWidgets.QGraphicsRectItem(0, 0, 1, 1)
        self.harea.setPen(QtGui.QPen(color))
        self.harea.setBrush(QtGui.QBrush(color))
        self.varea.setVisible(False)
        self.harea.setVisible(False)
        self.view.addItem(self.varea)
        self.view.addItem(self.harea)

    def setImage(self, *args, **kwargs):
        pg.ImageView.setImage(self, *args, **kwargs)
        levelMax = self.quickMinMax(self.image)[1]
        self.setLevels(-levelMax / 20, levelMax / 4)
        self.rescaleImage()

    def rescaleImage(self):
        if self.image is None:
            return
        viewRect = self.view.rect()
        self.imageItem.setRect(viewRect)
        self.view.autoRange()
        width, height = viewRect.width(), viewRect.height()
        self.hstep = height / self.imageItem.height()
        self.vstep = width / self.imageItem.width()
        self.harea.setRect(0, self.hstep, width, self.hstep + 1)
        self.varea.setRect(self.vstep, 0, self.vstep + 1, height)

    def drawArea(self, n, orientation):
        if self.image is None:
            return
        if orientation == QtCore.Qt.Vertical:
            self.varea.setVisible(False)
            self.harea.setVisible(True)
            self.harea.setY(self.hstep * (n - 1))
        elif orientation == QtCore.Qt.Horizontal:
            self.varea.setVisible(True)
            self.harea.setVisible(False)
            self.varea.setX(self.vstep * (n - 1))


class PlotWidget(pg.PlotWidget):
    sigWatchMouse = QtCore.pyqtSignal(float, float)

    def __init__(self, parent=None, background='default', **kargs):
        super().__init__(parent, background, **kargs)
        self.proxy = pg.SignalProxy(self.plotItem.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

    def mouseMoved(self, evt):
        pos = evt[0]
        if self.sceneBoundingRect().contains(pos):
            mousePoint = self.plotItem.vb.mapSceneToView(pos)
            self.sigWatchMouse.emit(mousePoint.x(), mousePoint.y())
