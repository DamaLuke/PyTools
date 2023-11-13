import os
import sys
from datetime import date

#提供当前日期、脚本根路径以及输出文件路径等常见信息
#
today = date.today().strftime("%Y-%m-%d")
rootpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
outpath = os.path.join(rootpath, "output")

if not os.path.exists(outpath):
    os.mkdir(outpath)
