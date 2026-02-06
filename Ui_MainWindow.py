# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui/mainwindow.ui'
# Updated for PyQt6 compatibility.
#
# WARNING! All changes made in this file will be lost!

from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(447, 556)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.headLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.headLabel.setText("")
        self.headLabel.setObjectName("headLabel")
        self.gridLayout.addWidget(self.headLabel, 0, 0, 1, 5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.hexfileCombox = QtWidgets.QComboBox(parent=self.centralwidget)
        self.hexfileCombox.setMinimumSize(QtCore.QSize(311, 0))
        self.hexfileCombox.setEditable(True)
        self.hexfileCombox.setObjectName("hexfileCombox")
        self.horizontalLayout.addWidget(self.hexfileCombox)
        self.openHexButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.openHexButton.setObjectName("openHexButton")
        self.horizontalLayout.addWidget(self.openHexButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 5)
        self.portCombox = QtWidgets.QComboBox(parent=self.centralwidget)
        self.portCombox.setEditable(False)
        self.portCombox.setObjectName("portCombox")
        self.gridLayout.addWidget(self.portCombox, 2, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.textEdit.setStyleSheet("")
        self.textEdit.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 3, 0, 1, 5)
        spacerItem = QtWidgets.QSpacerItem(
            260,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 3)
        self.uploadButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.uploadButton.setObjectName("uploadButton")
        self.gridLayout.addWidget(self.uploadButton, 4, 3, 1, 1)
        self.exitButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.exitButton.setObjectName("exitButton")
        self.gridLayout.addWidget(self.exitButton, 4, 4, 1, 1)
        self.mcuCombox = QtWidgets.QComboBox(parent=self.centralwidget)
        self.mcuCombox.setEnabled(True)
        self.mcuCombox.setEditable(False)
        self.mcuCombox.setObjectName("mcuCombox")
        self.gridLayout.addWidget(self.mcuCombox, 2, 1, 1, 4)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Arduloader"))
        self.openHexButton.setText(_translate("MainWindow", "Browser"))
        self.uploadButton.setText(_translate("MainWindow", "Upload"))
        self.exitButton.setText(_translate("MainWindow", "Exit"))
