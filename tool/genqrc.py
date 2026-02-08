#-*- coding: utf-8 -*-
#1.如何在基于PyQt6的Python代码中使用图标资源文件(qrc文件)
#答: QtGui.QIcon(":/app/icons/app/logo.ico")
#其中:/app标识图标在qrc文件中的分支, 后面的icons/app/logo.ico标识图标在qrc文件中的路径
#2.如何在使用py2exe转换后的exe文件中使用这些图标
#答: 使用pyrcc6命令(安装PyQt6后会有此工具)通过命令pyrcc6 -py3 sample.qrc > sample.py
#将qrc文件中的图标编译为二进制数据存放到py文件中, 然后在你需要使用图标的python文件中
#使用from sample.py import *加载图标资源即可

__author__ = "apache"
__version__ = "0.1"

import sys
from os import path, listdir
from glob import glob
from shutil import which
import subprocess

get_subdir_list = lambda _dir: [d for d in listdir(_dir) if path.isdir("%s/%s" % (_dir, d))]
    
def get_qresource_xml_bydir(topdir, _dir, filter="*.*"):
    items = ['\t<qresource prefix="/%s">' % _dir]
    for f in glob("%s/%s/%s" % (topdir, _dir, filter)):
        items.append('\t\t<file>%s</file>' % f.replace("\\", "/"))
    items.append("\t</qresource>")
    
    return '\n'.join(items)
    
def get_qrc_xml(topdir):
    subdirs = get_subdir_list(topdir)
    qresources = ["<RCC>"]
    for _dir in subdirs:
        qresources.append(get_qresource_xml_bydir(topdir, _dir))
    qresources.append("</RCC>")
    
    return '\n'.join(qresources)

def main(topdir, qrcfile):
    rcc_xml = get_qrc_xml(topdir)
    tmp_qrc = "tmp.qrc"
    with open(tmp_qrc, "w", encoding="utf-8") as fh:
        fh.write(rcc_xml)
    pyrcc = which("pyrcc6")
    if not pyrcc:
        print("pyrcc6 not found. Please install PyQt6 tools.")
        return 1
    result = subprocess.run([pyrcc, "-py3", tmp_qrc], capture_output=True, text=True)
    if result.returncode != 0:
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)
        return result.returncode
    with open(qrcfile, "w", encoding="utf-8") as out:
        out.write(result.stdout)
    return 0
    
if __name__ == "__main__":
    argc = len(sys.argv)
    if 1 < argc < 3:
        print(
            "生成二进制的图标资源文件\n"
            "usage: genqrc.py icon-dir qrc-pyfile\n"
            "sample: genqrc.py icons icons.py"
        )
        sys.exit(1)
    elif argc == 1:
        topdir, qrcfile = "icons", "icons.py"
    else:
        topdir, qrcfile = sys.argv[1], sys.argv[2]
        
    if main(topdir, qrcfile) == 0:
        print("ok:)")
    else:
        print("failed:(")
