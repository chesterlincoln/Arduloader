#-*- coding: utf-8 -*-
from os import path as OSPath
from Ui_MainWindow import Ui_MainWindow
from Uploader import Uploader
from PortManager import PortManager
from ConfigHelper import ConfigHelper
from icons import *
import const
import BoardHelper

from PyQt6 import QtCore, QtGui, QtWidgets
from serial.tools import list_ports
import serial

def tostr(text):
    return str(text)

def togbk(text):
    return str(text)

class ArduloaderWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.portManager = PortManager(self.ui, startmonitor=True)
        self.configHelper = ConfigHelper(self.ui)
        self.initSignal()
        self.setupUi_Ex()        
               
    def setupUi_Ex(self):
        self.setWindowTitle(const.windowtitle)
        self.ui.textEdit.append(const.aboutinfo)
        self.ui.headLabel.setPixmap(QtGui.QPixmap(":/main/icons/main/arduloader.png"))
        self.setWindowIcon(QtGui.QIcon(":/main/icons/main/logo.png"))
        self.setBoards()
        
        self.configHelper.updateUiByConfig()
    
    def setBoards(self):
        ret, self.__boardsinfodict = BoardHelper.getBoardsInfo()
        if not ret:
            self.__boardsinfodict = {}
            return

        self.ui.mcuCombox.clear()
        self.ui.mcuCombox.addItem("Arduino Leonardo")
        self.ui.mcuCombox.setEnabled(False)

    def onUploadFinish(self, ret, text):
        self.timer.stop()
        try:
            res = ret == 0 and "Upload SUCCESS:)" or ("%s\nUpload FAILED:(" % text)
        except IOError:
            res = "Read tmp file error"
        except:
            res = "Unknown error"
            
        self.ui.textEdit.append(res)
    
    def onUploading(self):
        prev_cursor = self.ui.textEdit.textCursor()
        self.ui.textEdit.moveCursor(QtGui.QTextCursor.MoveOperation.End)
        self.ui.textEdit.insertPlainText (".")
        self.ui.textEdit.setTextCursor(prev_cursor)
    
    def getUploadArgs(self):
        infodict = self.__boardsinfodict.get(tostr(self.ui.mcuCombox.currentText()))
        if not infodict:
            return
            
        mcu = infodict["mcu"]
        speed = infodict["speed"]
        protocol = infodict["protocol"]
        maximum_size = infodict["maximum_size"]
        comport = tostr(self.ui.portCombox.currentText())
        flash_bin = togbk(self.ui.hexfileCombox.currentText())
        
        return {"mcu": mcu,
                "speed": speed,
                "protocol": protocol,
                "maximum_size": maximum_size,
                "comport": comport, 
                "flash_bin": flash_bin
                }
    
    def checkUploadArgs(self, argsdict):
        if not argsdict:
            self.ui.textEdit.append("Get chip data error")
            return False
            
        if not OSPath.exists(argsdict.get("flash_bin", "")):
            self.ui.textEdit.append("Hex file not exists")
            return False
            
        # TODO: ¼ì²éÎÄ¼þ´óÐ¡ÊÇ·ñ³¬¶àµ±Ç°Ð¾Æ¬ÔÊÐíµÄ×î´óÖµ
        return True
        
    def startUpload(self):
        argsdict = self.getUploadArgs()
        if not self.checkUploadArgs(argsdict):
            return

        self.__pending_upload_args = argsdict
        self.__boot_start_ports = self.__list_ports()
        self.__boot_timer = QtCore.QElapsedTimer()
        self.__boot_timer.start()
        self.ui.textEdit.append("Waiting for bootloader port...")
        self.__touch_bootloader(argsdict.get("comport"))
        self.__boot_wait_timer = QtCore.QTimer()
        self.__boot_wait_timer.timeout.connect(self.__checkBootloaderPort)
        self.__boot_wait_timer.start(200)

    def __list_ports(self):
        return {p.device for p in list_ports.comports()}

    def __touch_bootloader(self, port):
        if not port:
            return
        try:
            ser = serial.Serial(port, 1200)
            ser.close()
        except Exception as exc:
            self.ui.textEdit.append("Bootloader touch failed: %s" % exc)

    def __checkBootloaderPort(self):
        current_ports = self.__list_ports()
        added = list(current_ports - self.__boot_start_ports)
        if added:
            self.__boot_wait_timer.stop()
            self.__pending_upload_args["comport"] = added[-1]
            self.ui.textEdit.append("Bootloader port: %s" % added[-1])
            self.__beginUpload(self.__pending_upload_args)
            return

        if self.__boot_timer.elapsed() > 5000:
            self.__boot_wait_timer.stop()
            self.ui.textEdit.append("Bootloader port not detected, using current port.")
            self.__beginUpload(self.__pending_upload_args)

    def __beginUpload(self, argsdict):
        self.uploader = Uploader()
        self.uploader.notifier.finished.connect(self.onUploadFinish)
        self.uploader.resetUploadArgs(argsdict)

        self.ui.textEdit.clear()
        self.ui.textEdit.append("Start uploading\n")
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.onUploading)
        self.uploader.start()
        self.timer.start(const.process_interval)
    
    def onOpenHexFile(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Choose a HEX file",
            ".",
            "HEX (*.hex)",
        )
        if filename == "":
            return
        index = self.ui.hexfileCombox.findText(filename)
        if index < 0:
            self.ui.hexfileCombox.insertItem(0, filename)
            index = 0
        self.ui.hexfileCombox.setCurrentIndex(index)
    
    def closeEvent(self, e):
        hex = tostr(self.ui.hexfileCombox.currentText())
        com = tostr(self.ui.portCombox.currentText())
        board = tostr(self.ui.mcuCombox.currentText())
        self.configHelper.updateConfig(hex, com, board)
        e.accept()
        
    def initSignal(self):
        self.ui.exitButton.clicked.connect(self.close)
        self.ui.uploadButton.clicked.connect(self.startUpload)
        self.ui.openHexButton.clicked.connect(self.onOpenHexFile)
        
