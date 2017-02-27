# -*- coding: utf8 -*-

import os
import sys

SRCDIR = ".\\scriptCN"
TGTDIR = os.path.dirname(sys.argv[0]) + '\\scriptTarget'
TBLFILE = os.path.dirname(sys.argv[0]) + '\\tableData.tbl'
ERRPATH = os.path.dirname(sys.argv[0]) + '\\err.log'
LOG_FILE_NAME = '/err.log'

if len(sys.argv) > 1 :
    arg1 = sys.argv[1]
    SRCDIR = arg1
#    if os.path.isdir(arg1):
    TGTDIR = arg1 + 'Target'
'''
    elif os.path.isfile(arg1):
        pathSplit = os.path.splitext(arg1)
        TGTDIR = pathSplit[0] + 'Target' + pathSplit[1]
    else:
        pass
'''

def getFileList(path, fl): #读取全部文件
    files = os.listdir(path)
    for f in files:
        if(os.path.isdir(path + '\\' + f)):
            getFileList(path + '\\' + f, fl)
        else:
            fl.append(path + '\\' + f)

# create code table
def loadTbl(tableFile):
    tableData = file(tableFile, 'r')
    tbl = {}
    for tableLine in tableData.readlines():
        if not tableLine == '\n' :
            d = tableLine.split('=')
            tableHex , tableWord = d[0], d[1][:-1].decode('utf-8')
            tbl[tableWord] = tableHex
    return tbl


# read file, convert file
def convertFile(sourceDir, targetDir, tblDir, tbl):
    fileList = []
    getFileList(sourceDir, fileList)
    errFile = file(os.path.dirname(tblDir) + LOG_FILE_NAME, 'w')
    for sourcePath in fileList :
        targetPath = targetDir + sourcePath.split(sourceDir)[-1]
        print 'Converting : ' + targetPath
        
        sourceFile = file(sourcePath , 'r')
        targetPathDir = os.path.dirname(targetPath)
        if not os.path.exists(targetPathDir):
            os.makedirs(targetPathDir)
        targetFile = file(targetPath , 'w')
        
        writebuf = ''
        for line in sourceFile.readlines() :
            lineStr = line.decode('utf-8').strip(u'\ufeff')  #anti UTF-8 BOM
            for sourceWord in lineStr :
                if sourceWord == u'\n' :
                    targetWord = '\n'
                else:
                    try:
                        targetWord = tbl[sourceWord].decode('hex')
                    except:
                        errFile.write(sourcePath + '\n' + sourceWord.encode('utf-8') + '\n')
                        targetWord = '????'
                writebuf += targetWord
        targetFile.write(writebuf)

if __name__ == "__main__" :
    '''
    #打开码表
    #读取源文件 - 转换 - 目标文件
    '''
    tbl = loadTbl(TBLFILE)
    convertFile(SRCDIR, TGTDIR, os.path.dirname(sys.argv[0]), tbl)