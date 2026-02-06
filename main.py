#-*- coding: utf-8 -*-
#Author:    Uname
#Date:      2014/2/11
#Version:   0.2
#Copyright: uname.github.io

import sys

from PyQt6.QtWidgets import QApplication

from ArduloaderWindow import ArduloaderWindow

sys.dont_write_bytecode = True

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ArduloaderWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
