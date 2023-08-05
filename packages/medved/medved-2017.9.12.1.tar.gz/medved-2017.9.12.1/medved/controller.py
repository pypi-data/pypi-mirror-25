#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from .model import MedvedModel
from .wmedeval import QWMEDeval
from . import utils, widgets


class MedvedController(QtCore.QObject):
    sigCancel = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.settings = QtCore.QSettings()
        self.threadUpdateChecker = None
        self.createModel()
        self.createWindows()
        self.deleteThreadUpdateChecker()
        self.connectSignals()

    def createUpdateChecker(self):
        self.checkUpdatesByUser = False
        self.threadUpdateChecker = QtCore.QThread()
        self.updateChecker = utils.UpdateChecker()
        self.updateChecker.moveToThread(self.threadUpdateChecker)
        # noinspection PyUnresolvedReferences
        self.threadUpdateChecker.started.connect(self.updateChecker.check)
        self.updateChecker.sigNewVersion.connect(self.showNewVersion)
        self.updateChecker.sigFinished.connect(self.deleteThreadUpdateChecker)

    def deleteThreadUpdateChecker(self):
        self.checkUpdatesByUser = False
        if self.threadUpdateChecker:
            self.threadUpdateChecker.quit()
            self.threadUpdateChecker.wait()
        self.threadUpdateChecker = None
        self.updateChecker = None

    def createModel(self):
        self.mthread = QtCore.QThread()
        self.model = MedvedModel()
        self.model.moveToThread(self.mthread)

    def loadSettings(self):
        s = self.settings
        self.wupdates.cb.setChecked(utils.pyqt2bool(s.value('Controller/doNotCheckUpdates', False)))
        self.wmedved.loadSettings(s)

    def saveSettings(self):
        s = self.settings
        s.setValue('Controller/doNotCheckUpdates', self.wupdates.cb.isChecked())
        self.wmedved.saveSettings(s)

    def createWindows(self):
        self.wmedved = QWMEDeval()
        self.wprogress = widgets.ProgressWindow(self.wmedved)
        self.wabout = widgets.WAbout(self.wmedved)
        self.wupdates = widgets.WUpdates(self.wmedved)

    def connectSignals(self):
        self.connectGUISignals()
        self.connectModelSignals()

    def connectGUISignals(self):
        self.wmedved.sigClose.connect(self.closeAll)
        self.wmedved.sigDir.connect(self.wprogress.show)
        self.wmedved.sigDir.connect(self.model.loadData)
        self.wmedved.sigData2Th.connect(self.model.getData2Th)
        self.wmedved.sigDataTime.connect(self.model.getDataTime)
        self.wmedved.sigFourier2Th.connect(self.model.getFourier2Th)
        self.wmedved.sigFourierTime.connect(self.model.getFourierTime)
        self.wmedved.sigUpdateFourierPlot.connect(self.model.getFourierImage)
        self.wmedved.sigUpdateDataPlot.connect(self.model.getDataImage)
        self.wmedved.sigFourierDomain.connect(self.model.setFourierDomain)
        self.wmedved.sigUnits.connect(self.model.setUnits)
        self.wmedved.sigWavelength.connect(self.model.setWavelength)
        self.wmedved.sigOpenFiles.connect(self.model.loadData)
        self.wmedved.sigClean.connect(self.model.cleanData)
        self.wmedved.sigClean.connect(self.clean)
        self.sigCancel.connect(self.model.cancelLoad)
        self.wprogress.sigCancel.connect(self.sigCancel.emit)
        self.wmedved.dataTree.sigItemMoved.connect(self.model.dataOrderChanged)
        self.wmedved.actionAbout.triggered.connect(self.wabout.exec)
        self.wmedved.actionCheckUpdates.triggered.connect(self.checkNewVersionByUser)
        self.wabout.buttonUpdate.clicked.connect(self.checkNewVersionByUser)

    def connectModelSignals(self):
        self.model.sigLoadingError.connect(self.wmedved.showModelError)
        self.model.sigLoadingError.connect(self.finishedLoad)
        self.model.sigFinishedLoading.connect(self.wmedved.finishedLoad)
        self.model.sigFinishedLoading.connect(self.finishedLoad)
        self.model.sigDataImage.connect(self.plotDataImage)
        self.model.sigFourierImage.connect(self.plotFourierImage)
        self.model.sigData2Th.connect(self.showData2Th)
        self.model.sigDataTime.connect(self.showDataTime)
        self.model.sigFourier2Th.connect(self.showFourier2Th)
        self.model.sigFourierTime.connect(self.showFourierTime)
        self.model.sigLoadProgress.connect(self.wprogress.setValue)
        self.model.sigMaxProgress.connect(self.wprogress.setMaximum)
        self.model.sigProgressName.connect(self.wprogress.setText)

    def finishedLoad(self):
        self.wprogress.hide()
        self.wmedved.dataSliders.timeSlider.valueChanged.emit(0)
        self.wmedved.fourierSliders.timeSlider.valueChanged.emit(0)

    def plotDataImage(self, data):
        self.wmedved.dataSliders.imageView.setImage(data)

    def plotFourierImage(self, data):
        self.wmedved.fourierSliders.imageView.setImage(data)

    def showData2Th(self, value, s, x, y):
        self.wmedved.dataSliders.plot.plot(x, y, pen='g', clear=True)
        self.wmedved.dataSliders.twothEdit.setText(s)
        self.wmedved.dataSliders.imageView.drawArea(value, self.wmedved.dataSliders.twothSlider.orientation())

    def showDataTime(self, value, x, y):
        self.wmedved.dataSliders.timeEdit.setText(str(value))
        self.wmedved.dataSliders.plot.plot(x, y, pen='g', clear=True)
        self.wmedved.dataSliders.imageView.drawArea(value, self.wmedved.dataSliders.timeSlider.orientation())

    def showFourier2Th(self, value, units, x, y):
        self.wmedved.fourierSliders.twothEdit.setText(str(value))
        self.wmedved.fourierSliders.plot.plot(x, y, clear=True, **self.getPlotParams(units))
        self.wmedved.fourierSliders.plot.plotItem.axes['left']['item'].setTicks(self.getPlotTicks(units))
        self.wmedved.fourierSliders.imageView.drawArea(value, self.wmedved.fourierSliders.twothSlider.orientation())

    def showFourierTime(self, value, units, x, y):
        self.wmedved.fourierSliders.timeEdit.setText(str(value))
        self.wmedved.fourierSliders.plot.plot(x, y, clear=True, **self.getPlotParams(units))
        self.wmedved.fourierSliders.plot.plotItem.axes['left']['item'].setTicks(self.getPlotTicks(units))
        self.wmedved.fourierSliders.imageView.drawArea(value, self.wmedved.fourierSliders.timeSlider.orientation())

    def getPlotTicks(self, units):
        if units == 'p':
            return [[(-180, '-π'), (-90, '-π/2'), (0, '0'), (90, 'π/2'), (180, 'π')]]

    def getPlotParams(self, units):
        if units == 'p':
            return {'pen': None, 'symbol': 'o'}
        else:
            return {'pen': 'g', 'symbol': None}

    def start(self):
        self.loadSettings()
        self.mthread.start()
        self.wmedved.start()
        self.checkNewVersion()

    def closeAll(self):
        self.saveSettings()
        self.sigCancel.emit()
        self.wmedved.hide()
        self.mthread.quit()
        self.deleteThreadUpdateChecker()
        self.mthread.wait()

    def clean(self):
        pass

    def checkNewVersion(self):
        if not self.wupdates.cb.isChecked():
            self.createUpdateChecker()
            self.threadUpdateChecker.start()

    def showNewVersion(self, text, error):
        if self.checkUpdatesByUser:
            self.wupdates.error(text) if error else self.wupdates.success(text)
        else:
            if not error and not self.wupdates.cb.isChecked() and text:
                self.wupdates.success(text)

    def checkNewVersionByUser(self):
        self.createUpdateChecker()
        self.checkUpdatesByUser = True
        self.threadUpdateChecker.start()
