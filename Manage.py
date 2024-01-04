import os
from datetime import date

# 提供当前日期、脚本根路径以及输出文件路径，并在当前目录生成output文件夹用于存放输出的结果
#
today = date.today().strftime("%Y-%m-%d")
rootpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
outpath = os.path.join(rootpath, "output")

if not os.path.exists(outpath):
    os.mkdir(outpath)

SUBJID = '受试者代码'
SITEID = '中心编号'
VISIT = '访视名称'
FORMNM = '表名称'
RECREP = '序号'