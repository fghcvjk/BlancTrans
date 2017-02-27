# -*- coding: UTF-8 -*-

import os
import sys
import re

def getFileLists(path, fl):  #return a list
    try:
        files = os.listdir(path)
        for f in files:
            subPath = path + '/' + f
            if (os.path.isdir(subPath)):
                getFileLists(subPath, fl)
            else:
                if(os.path.splitext(subPath)[1] == '.txt'):
                    fl.append(subPath)
    except: #permission denied
        pass

def readTBL(tblPath):
    #if os.path.isfile(tblPath):
    tbl = {}
    tblFile = open(tblPath)
    for line in tblFile.readlines():
        if (line != '\n'):
            d = line.split('=')
            tblHex, tblWord = d[0], d[1][:-1].decode('utf-8')
            tbl[tblWord] = tblHex
            #line = line.decode('utf-8')
    return tbl

def wordFrequency(fileList):
    # get file list
    # read file
    # calc file word freq
    wordFreq = {}
    for path in fileList:
        ofile = open(path, 'r')
        for line in ofile.readlines():
            line = line.decode('utf-8').strip()
            for word in line:
                if not re.match(ur"[\u4e00-\u9fa5]+", word) == None:    #只匹配汉字
                    if wordFreq.has_key(word):
                        wordFreq[word] += 1
                    else:
                        wordFreq[word] = 1
    return wordFreq

def compareJIS(source, compared): # return result dict
    #read sjis table
    #read wordFreq table
    #compare table
    
    # 方案一 ：遍历匹配另一字典，没有则存到List.
    # 缺点:需要遍历两遍,导出两边未使用的键值对
    notinDict = {}
    for key in source:
        if not compared.has_key(key):
            notinDict[key] = source[key]
    return notinDict
    '''
    # 方案二：遍历，两边存在则删掉该条目。缺点:需要更多内存空间临时存储
    '''

def outputFile(dict, name, objectFile = './'):  # dict change to sorted list
    sortedList = sorted(dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    #sortedList = dict.reverse()
    saveFile = open(objectFile + name + ".txt", 'w')

    for tuples in sortedList:
        str = u'%s\t\tvalue: %s\n' % (tuples[0], tuples[1]) #join()
        saveFile.write(str.encode("utf-8"))

if __name__ == "__main__":
    #run Code
    fileList = []
    pathStr = ''
    
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        pathStr = sys.argv[1]
    else:
        pathStr = os.path.dirname(sys.argv[0]) + '\\script'
    getFileLists(pathStr, fileList)
    
    wF = wordFrequency(fileList)
    tbl = readTBL(os.path.dirname(sys.argv[0]) + '\\tableData.tbl')
    wordNotUse = compareJIS(wF, tbl)
    codeNotUse = compareJIS(tbl, wF)
    outputFile(wF, u'字频')
    outputFile(wordNotUse, u'文本剩字')
    outputFile(codeNotUse, u'码表剩字')
