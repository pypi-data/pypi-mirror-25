#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui
from . import utils
from .ui.ui_wabout import Ui_WAbout
from .ui.ui_sliders import Ui_QSlidersWidget


class WSliders(QtWidgets.QWidget, Ui_QSlidersWidget):
    def __init__(self, plot, parent):
        super().__init__(parent)
        self.plot = plot
        self.setupUi(self)


class ProgressWindow(QtWidgets.QDialog):
    sigCancel = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUI()
        self.connectSignals()

    # noinspection PyUnresolvedReferences
    def connectSignals(self):
        self.bb.rejected.connect(self.cancel)

    def setupUI(self):
        self.label = QtWidgets.QLabel()
        self.bb = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel)
        self.pb = QtWidgets.QProgressBar()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.pb)
        layout.addWidget(self.bb)
        self.setLayout(layout)
        self.setWindowModality(QtCore.Qt.WindowModal)

    def setValue(self, value):
        self.pb.setValue(value)
        if self.pb.maximum() == value:
            self.hide()

    def setMaximum(self, value):
        self.pb.setMaximum(value)

    def setText(self, text):
        self.label.setText(text)

    def showEvent(self, event):
        self.setValue(0)
        super().showEvent(event)

    def cancel(self):
        self.hide()
        self.sigCancel.emit()


class TreeWidget(QtWidgets.QTreeWidget):
    sigItemMoved = QtCore.pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        # self.setDragAndDrop()

    def setDragAndDrop(self):
        self.oldIndex = None
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

    def dropEvent(self, event: QtGui.QDropEvent):
        droppedIndex = self.indexAt(event.pos())
        if not droppedIndex.isValid() or not self.oldIndex:
            return
        super().dropEvent(event)
        dp = self.dropIndicatorPosition()
        if dp == QtWidgets.QAbstractItemView.BelowItem and self.oldIndex > droppedIndex:
            droppedIndex = droppedIndex.sibling(droppedIndex.row() + 1, droppedIndex.column())
        elif dp == QtWidgets.QAbstractItemView.AboveItem and self.oldIndex < droppedIndex:
            droppedIndex = droppedIndex.sibling(droppedIndex.row() - 1, droppedIndex.column())
        selectionModel = self.selectionModel()
        selectionModel.clearSelection()
        selectionModel.select(droppedIndex, QtCore.QItemSelectionModel.Select)
        self.sigItemMoved.emit(self.oldIndex.row(), droppedIndex.row())
        self.oldIndex = None

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        oldIndex = self.indexAt(event.pos())
        if oldIndex.isValid():
            super().dragEnterEvent(event)
            self.oldIndex = oldIndex


class WAbout(QtWidgets.QDialog, Ui_WAbout):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        lt = self.aboutLabel.text()
        lt = lt.replace('##', utils.get_hg_hash()).replace('@@', utils.get_version())
        self.aboutLabel.setText(lt)
        QtCore.QTimer.singleShot(0, lambda: self.resize(0, 0))

    @QtCore.pyqtSlot()
    def on_closeButton_clicked(self):
        self.close()

    @QtCore.pyqtSlot()
    def on_aboutQtButton_clicked(self):
        QtWidgets.QMessageBox.aboutQt(self)


class WUpdates(QtWidgets.QMessageBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle('Medved updates')
        self.setStandardButtons(self.Ok)
        self.cb = QtWidgets.QCheckBox('Do not check updates automatically')
        self.setCheckBox(self.cb)

    def error(self, text):
        self.setIcon(self.Critical)
        self.setText('There has been an error during update checking')
        self.setInformativeText(text)
        self.exec()

    def success(self, text):
        self.setIcon(self.Information)
        if text:
            self.setText('A new MEDved version is available at <a href=https://soft.snbl.eu/medved.html#download>'
                         'soft.snbl.eu</a>')
            self.setInformativeText(text)
        else:
            self.setText('There are no new updates of MEDved')
        self.exec()
