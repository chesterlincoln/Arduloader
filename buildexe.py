#-*- coding: utf-8 -*-

import sys
from distutils.core import setup
import py2exe

includes = ["PyQt6.QtGui", "PyQt6.QtCore", "PyQt6.QtWidgets"]
            
dll_excludes = ["msvcm90.dll", "msvcp90.dll", "msvcr90.dll"]

if len(sys.argv) == 1:
    sys.argv.append("py2exe")

setup(  version="0.1",
        description = "Arduino Hex Uploader",
        name = "arduloader.exe",
        author = "Apache",
        packages = [],
        py_modules = [],
        zipfile = None,
        windows = [{"script":"main.py", "icon_resources":[(1, "./icons/main/logo.ico")], "dest_base":"arduloader"}],
		options = {   "py2exe":
                        {   "compressed": 2,
                            "bundle_files": 1,
                            "includes": includes,
                            "dll_excludes":dll_excludes
                        }
                })
