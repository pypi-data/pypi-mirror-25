# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'medved/ui//ui_sliders.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QSlidersWidget(object):
    def setupUi(self, QSlidersWidget):
        QSlidersWidget.setObjectName("QSlidersWidget")
        QSlidersWidget.resize(653, 388)
        self.gridLayout = QtWidgets.QGridLayout(QSlidersWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.twothEdit = QtWidgets.QLineEdit(QSlidersWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.twothEdit.sizePolicy().hasHeightForWidth())
        self.twothEdit.setSizePolicy(sizePolicy)
        self.twothEdit.setMaximumSize(QtCore.QSize(75, 75))
        self.twothEdit.setMaxLength(10)
        self.twothEdit.setObjectName("twothEdit")
        self.horizontalLayout.addWidget(self.twothEdit)
        self.twothSlider = QtWidgets.QSlider(QSlidersWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.twothSlider.sizePolicy().hasHeightForWidth())
        self.twothSlider.setSizePolicy(sizePolicy)
        self.twothSlider.setOrientation(QtCore.Qt.Horizontal)
        self.twothSlider.setObjectName("twothSlider")
        self.horizontalLayout.addWidget(self.twothSlider)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.timeEdit = QtWidgets.QLineEdit(QSlidersWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeEdit.sizePolicy().hasHeightForWidth())
        self.timeEdit.setSizePolicy(sizePolicy)
        self.timeEdit.setMaximumSize(QtCore.QSize(75, 75))
        self.timeEdit.setMaxLength(10)
        self.timeEdit.setObjectName("timeEdit")
        self.verticalLayout.addWidget(self.timeEdit)
        self.timeSlider = QtWidgets.QSlider(QSlidersWidget)
        self.timeSlider.setOrientation(QtCore.Qt.Vertical)
        self.timeSlider.setInvertedAppearance(True)
        self.timeSlider.setInvertedControls(False)
        self.timeSlider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.timeSlider.setObjectName("timeSlider")
        self.verticalLayout.addWidget(self.timeSlider)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.imageView = ImageView(QSlidersWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageView.sizePolicy().hasHeightForWidth())
        self.imageView.setSizePolicy(sizePolicy)
        self.imageView.setObjectName("imageView")
        self.gridLayout.addWidget(self.imageView, 1, 1, 1, 1)

        self.retranslateUi(QSlidersWidget)
        QtCore.QMetaObject.connectSlotsByName(QSlidersWidget)

    def retranslateUi(self, QSlidersWidget):
        _translate = QtCore.QCoreApplication.translate
        QSlidersWidget.setWindowTitle(_translate("QSlidersWidget", "Form"))

from ..pgwidgets import ImageView
