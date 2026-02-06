#-*- coding: utf-8 -*-
import importlib
import os
import sys
from PyQt6.QtCore import QTimer

def _load_list_ports():
    repo_root = os.path.dirname(os.path.abspath(__file__))
    original_path = list(sys.path)
    sys.path = [path for path in sys.path if os.path.abspath(path or ".") != repo_root]
    try:
        return importlib.import_module("serial.tools.list_ports")
    finally:
        sys.path = original_path

lp = _load_list_ports()

class PortManager(object):
    def __init__(self, ui, queryinterval=1000, startmonitor=False):
        self.ui = ui
        self.queryinterval = queryinterval
        self.querytimer = QTimer()
        self.querytimer.timeout.connect(self.__updateUiComPorts)
        self.com_list = []
        self.__updateUiComPorts(showmsg=False)
        if startmonitor:
            self.startComPortMonitor()
        
    def __updateUiComPorts(self, com_list=None, showmsg=True):
        if com_list is None:
            com_list = self.__getComInfoList()
        
        # NEW ADDED
        for comport in list(set(com_list) - set(self.com_list)):
            self.ui.portCombox.addItem(comport)
            if showmsg:
                self.ui.textEdit.append("New port found: %s" % comport)
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
        
