#-*- coding: utf-8 -*-
from PyQt6.QtCore import QTimer
from serial.tools import list_ports as lp

class PortManager(object):
    def __init__(self, ui, queryinterval=1000, startmonitor=False, only_show_new=True):
        self.ui = ui
        self.queryinterval = queryinterval
        self.only_show_new = only_show_new
        self.querytimer = QTimer()
        self.querytimer.timeout.connect(self.__updateUiComPorts)
        self.com_list = []
        self.ui.portCombox.clear()
        self.ui.portCombox.setPlaceholderText("请插入设备")
        self.ui.textEdit.append("请插入设备")
        self.com_list = self.__getComInfoList()
        if startmonitor:
            self.startComPortMonitor()
        
    def __updateUiComPorts(self, com_list=None, showmsg=True):
        if com_list is None:
            com_list = self.__getComInfoList()
        
        # NEW ADDED
        added = list(set(com_list) - set(self.com_list))
        if added and self.only_show_new:
            self.ui.portCombox.clear()
        for comport in added:
            self.ui.portCombox.addItem(comport)
            if showmsg:
                self.ui.textEdit.append("New port found: %s" % comport)
        if added:
            self.ui.portCombox.setCurrentIndex(self.ui.portCombox.count() - 1)
        # NEW REMOVED
        for comport in list(set(self.com_list) - set(com_list)):
            index = self.ui.portCombox.findText(comport)
            if index == -1:
                continue
            self.ui.portCombox.removeItem(index)
            if showmsg:
                self.ui.textEdit.append("Port removed: %s" % comport)
                
        self.com_list = com_list
        
    def __getComInfoList(self):
        return [port.device for port in list(lp.comports())]
        
    def startComPortMonitor(self):
        self.querytimer.start(self.queryinterval)
    
    def stopComPortMonitor(self):
        self.querytimer.stop()
        
