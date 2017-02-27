# -*- coding:utf-8 -*-

import os
import sys
from langconv import *

# line = '你们'.decode('utf-8')
  
# 转换繁体到简体
# line = Converter('zh-hant').convert(line)
# print line
  
  

def getFileList(path, fl): #读取全部文件
    files = os.listdir(path)
    for f in files:
        if(os.path.isdir(path + '\\' + f)):
            getFileList(path + '\\' + f, fl)
        else:
            fl.append(path + '\\' + f)

fileList = []
sourceDir = ".\\old"
targetDir = os.path.dirname(sys.argv[0]) + '\\new'
getFileList(sourceDir, fileList)
for sourcePath in fileList :
    targetPath = targetDir + '\\' + sourcePath.lstrip(sourceDir)
    sourceFile = file(sourcePath , 'r')
    targetPathDir = os.path.dirname(targetPath)
    if not os.path.exists(targetPathDir):
        os.makedirs(targetPathDir)
    targetFile = file(targetPath , 'w')
    for line in sourceFile.readlines() :
        lineStr = Converter('zh-hant').convert(line.decode('utf-8'))
        targetFile.write(lineStr.encode('utf-8'))