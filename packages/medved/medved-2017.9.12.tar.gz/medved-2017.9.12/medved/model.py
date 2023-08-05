#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import glob
import concurrent.futures
import numpy as np
from scipy import fftpack
from PyQt5 import QtCore


class MedvedModel(QtCore.QObject):
    sigProgressName = QtCore.pyqtSignal(str)
    sigFinishedLoading = QtCore.pyqtSignal(int, int, int, int, tuple)
    sigLoadingError = QtCore.pyqtSignal(str)
    sigLoadProgress = QtCore.pyqtSignal(int)
    sigMaxProgress = QtCore.pyqtSignal(int)
    sigDataImage = QtCore.pyqtSignal(np.ndarray)
    sigFourierImage = QtCore.pyqtSignal(np.ndarray)
    sigData2Th = QtCore.pyqtSignal(int, str, np.ndarray, np.ndarray)
    sigDataTime = QtCore.pyqtSignal(int, np.ndarray, np.ndarray)
    sigFourier2Th = QtCore.pyqtSignal(int, str, np.ndarray, np.ndarray)
    sigFourierTime = QtCore.pyqtSignal(int, str, np.ndarray, np.ndarray)

    def __init__(self):
        super().__init__()
        self.canceled = True
        self.wavelength = 0.7
        self.units = 't'
        self.fdomain = 'r'
        self.cleanData()
        self.connectSignals()

    def cleanData(self):
        self.data = None
        self.fdata = None
        self.files = []
        self.dataFiles = []
        self.fdata = None
        self.frange1 = None
        self.absolute = None
        self.phase = None
        self.datarange = None
        self.data_d = None
        self.data_dd = None
        self.lastData = lambda: None
        self.lastFourier = lambda: None

    def connectSignals(self):
        pass

    def loadData(self, files):
        if isinstance(files, str) and os.path.isdir(files):
            files = glob.glob(f'{files}/*')
        elif isinstance(files, list):
            pass
        else:
            return
        self.canceled = False
        self.sigProgressName.emit('Reading files...')
        self.sigMaxProgress.emit(len(files))
        self.readFiles(files)
        self.calc()
        if not self.canceled and not self.files:
            self.sigLoadingError.emit('There were no acceptable files')
            self.cleanData()
        self.canceled = True

    def calc(self):
        if not self.dataFiles or self.canceled:
            return
        self.data = np.empty(self.dataFiles[0].shape + (len(self.dataFiles),))
        for i, d in enumerate(self.dataFiles):
            try:
                self.data[:, :, i] = d
            except IndexError:
                self.sigLoadingError.emit('There was an error with loading of files')
                self.cleanData()
                return
        self.calc_d()
        self.calculateFourier()
        if self.data is not None and self.fdata is not None:
            self.sigFinishedLoading.emit(self.data.shape[2] - 1, self.fdata.shape[1] - 1,
                                         self.data.shape[0] - 1, self.fdata.shape[0] - 1,
                                         self.files)
            self.getDataImage()
            self.getFourierImage()

    def calc_d(self):
        if self.data is not None:
            self.datarange = np.arange(self.data.shape[2])
            self.data_d = self.wavelength / 2 / np.sin(np.radians(self.data[:, 0, :]) / 2)
            self.data_dd = self.data_d ** 2

    def calculateFourier(self):
        if self.data is not None:
            self.fdata = fftpack.fft(self.data[:, 1, :])
            self.frange1 = np.arange(self.fdata.shape[1])
            self.absolute = np.absolute(self.fdata)
            self.phase = np.angle(self.fdata, deg=True)

    def cancelLoad(self):
        self.canceled = True

    def readFiles(self, files):
        f, d = [], []
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = {executor.submit(read_file, file): file for file in files}
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                QtCore.QCoreApplication.processEvents()
                if self.canceled:
                    for f in futures:
                        f.cancel()
                    self.cleanData()
                    return
                result = future.result()
                if result is not None:
                    d.append(result[0])
                    f.append(result[1])
                self.sigLoadProgress.emit(i)
        self.files, self.dataFiles = zip(*sorted(zip(f, d)))

    def getData2Th(self, value):
        if self.data is None:
            return
        x, y = self.datarange, self.data[value, 1, :]
        s = str(self.data[value, 0, 0])
        self.sigData2Th.emit(value, s, x, y)
        self.lastData = lambda: self.getData2Th(value)

    def getDataTime(self, value):
        if self.data is None:
            return
        x = self.getDataSlice(value)
        if x is None:
            return
        y = self.data[:, 1, value]
        self.lastData = lambda: self.getDataTime(value)
        self.sigDataTime.emit(value, x, y)

    def getDataSlice(self, value):
        if self.units == 't':
            return self.data[:, 0, value]
        elif self.units == 'd':
            return self.data_d[:, value]
        elif self.units == 'dd':
            return self.data_dd[:, value]

    def getFourierSlice(self, s1, s2):
        if self.fdomain == 'i':
            return self.fdata[s1, s2].imag
        elif self.fdomain == 'a':
            return self.absolute[s1, s2]
        elif self.fdomain == 'p':
            return self.phase[s1, s2]
        elif self.fdomain == 'r':
            return self.fdata[s1, s2].real

    def getFourier2Th(self, value):
        if self.fdata is None:
            return
        y = self.getFourierSlice(value, slice(None))
        if y is None:
            return
        x = self.frange1
        self.sigFourier2Th.emit(value, self.fdomain, x, y)
        self.lastFourier = lambda: self.getFourier2Th(value)

    def getFourierTime(self, value):
        if self.fdata is None:
            return
        x = self.getDataSlice(value)
        y = self.getFourierSlice(slice(None), value)
        if x is None or y is None:
            return
        self.sigFourierTime.emit(value, self.fdomain, x, y)
        self.lastFourier = lambda: self.getFourierTime(value)

    def getFourierImage(self):
        if self.fdata is not None:
            self.sigFourierImage.emit(self.getFourierSlice(slice(None), slice(None)))
            self.lastFourier()

    def getDataImage(self):
        if self.data is not None:
            self.sigDataImage.emit(self.data[:, 1, :])
            self.lastData()

    def dataOrderChanged(self, old, new):
        if old > new:
            s, c = slice(new, old + 1), 1
        elif old < new:
            s, c = slice(old, new + 1), -1
        else:
            return
        self.data[:, 1, s] = np.roll(self.data[:, 1, s], c, axis=1)
        self.calculateFourier()
        self.getDataImage()
        self.getFourierImage()

    def setWavelength(self, wavelength):
        try:
            self.wavelength = float(wavelength)
        except ValueError:
            return
        self.calc_d()
        self.lastData()
        self.lastFourier()

    def setFourierDomain(self, domain):
        self.fdomain = domain

    def setUnits(self, units):
        self.units = units


def read_file(datafile):
    if not os.path.isfile(datafile):
        return
    if datafile.endswith('.hkl'):
        data = read_hkl(datafile)
    else:
        try:
            data = np.loadtxt(datafile)
        except ValueError:
            return
    return data, os.path.basename(datafile)


def read_hkl(datafile):
    # noinspection PyUnresolvedReferences
    header = ff.FortranRecordReader('3I4,2F8.2')
    lst = []
    for line in open(datafile):
        try:
            line = header.readDir(line)
        except ValueError:
            break
        else:
            if None not in line:
                lst.append(line)
    array = np.array(lst)
    array = array[np.lexsort((array[:, 2], array[:, 1], array[:, 0]))]  # sorting by l k h
    b = np.empty_like(array)
    it = np.nditer(array, flags=['multi_index'])
    hkl = np.array([0., 0., 0., 0., 0.])
    j, k = 0, 1
    first = True
    while not it.finished:
        index = it.multi_index[1]
        hkl[index] = it[0]
        if index == 4:
            if first:
                first = False
                _hkl = hkl.copy()
            elif np.array_equal(hkl[:3], _hkl[:3]):
                k += 1
                _hkl[3:] += hkl[3:]
            else:
                _hkl[3:] /= k
                b[j, :] = _hkl
                _hkl = hkl.copy()
                k = 1
                j += 1
        it.iternext()
    array = np.c_[np.arange(j), b[:j, 3:], b[:j, :3]]
    return array
