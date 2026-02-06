#-*- coding: utf-8 -*-
import const
import subprocess
import threading
from PyQt6 import QtCore

def getstatusoutput(cmd):
    """Return (status, output) of executing cmd in a shell."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    text = (result.stdout or "") + (result.stderr or "")
    return result.returncode, text

class UploadNotifier(QtCore.QObject):
    finished = QtCore.pyqtSignal(int, str)
    
class Uploader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.notifier = UploadNotifier()
        
        self.avrdude = const.avrdude
        self.avrdude_conf = const.avrconf
        self.mcu = 'atmega328p'
        self.speed = "115200"
        self.protocol = "arduino"
        self.comport = "COM3"
        self.flash_bin = ''
        
        self.__buildUploadCmd()
    
    def __buildUploadCmd(self):
        self.upload_cmd = "%s -C%s -v -p%s -c%s -P%s -b%s -D -Uflash:w:%s:i 2>%s" % (
                           self.avrdude,
                           self.avrdude_conf,
                           self.mcu,
                           self.protocol,
                           self.comport,
                           self.speed,
                           self.flash_bin,
                           const.arduloader_log)
    
    def resetUploadArgs(self, argsdict):
        assert type(argsdict) is dict
        
        self.mcu = argsdict["mcu"]
        self.speed = argsdict["speed"]
        self.protocol = argsdict["protocol"]
        self.comport = argsdict["comport"]
        self.flash_bin = argsdict["flash_bin"]
        
        self.__buildUploadCmd()
        
    def run(self):
        self.upload()
        
    def upload(self):
        ret, text = getstatusoutput(self.upload_cmd)
        self.notifier.finished.emit(ret, text)
        
