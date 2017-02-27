#!/usr/bin/env Python
# -*- coding:utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from PySide.QtCore import *
from PySide.QtGui import *
from formUi import Ui_MainWindow
import newtran
import langconv
import wordFreq

class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.ui= Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("BlancTrans")
        try:
            self.setWindowIcon(QIcon('res/ico64.ico'))
        except:
            pass
        self.FilePath = os.getcwd()
        try:
            self.FilePath = self.FilePath.decode('GBK')
        except:
            pass

        self.ui.lineEditTab1Tbl.setText(self.getInitTbl())
        self.ui.lineEditTab1Source.setText(self.FilePath)
        self.ui.lineEditTab1Object.setText(self.FilePath)
        self.connect(self.ui.pushButtonTab1Tbl, SIGNAL("clicked()"),self.tbl_button_click)
        self.connect(self.ui.pushButtonTab1Source, SIGNAL("clicked()"),self.tab1_tf_button_click)
        self.connect(self.ui.pushButtonTab1Object, SIGNAL("clicked()"),self.tab1_of_button_click)
        self.connect(self.ui.pushButtonTab1Go, SIGNAL("clicked()"),self.go_button_click)

        self.transChineseType = 0
        self.ui.lineEditTab2Source.setText(self.FilePath)
        self.ui.lineEditTab2Object.setText(self.FilePath)
        self.connect(self.ui.pushButtonTab2Source, SIGNAL("clicked()"),self.tab2_tf_button_click)
        self.connect(self.ui.pushButtonTab2Object, SIGNAL("clicked()"),self.tab2_of_button_click)
        self.connect(self.ui.radioButtonTab2Cht2Chs, SIGNAL("clicked()"),self.transChineseTypeChs)
        self.connect(self.ui.radioButtonTab2Chs2Cht, SIGNAL("clicked()"),self.transChineseTypeCht)
        self.connect(self.ui.pushButtonTab2Go, SIGNAL("clicked()"),self.transChinese)

        self.ui.lineEditTab3Text1.setText(self.getInitFirstTxt())
        self.ui.lineEditTab3Text2.setText(self.getInitSecondTxt())
        self.ui.lineEditTab3Index.setText('―――|－－－'.decode('utf-8'))
        self.ui.lineEditTab3Object.setText(self.getInitThirdTxt())
        self.connect(self.ui.pushButtonTab3Text1, SIGNAL("clicked()"),self.text1_button_click)
        self.connect(self.ui.pushButtonTab3Text2, SIGNAL("clicked()"),self.text2_button_click)
        self.connect(self.ui.pushButtonTab3Object, SIGNAL("clicked()"),self.tab3_of_button_click)
        self.connect(self.ui.pushButtonTab3Go, SIGNAL("clicked()"),self.mergeText)

        self.ui.lineEditTab4Source.setText(self.FilePath)
        self.ui.lineEditTab4Object.setText(self.FilePath)
        self.ui.lineEditTab4Tbl.setText(self.getInitTbl())
        self.connect(self.ui.pushButtonTab4Tbl, SIGNAL("clicked()"),self.tbl_button_click_tab4)
        self.connect(self.ui.pushButtonTab4Source, SIGNAL("clicked()"),self.tab4_tf_button_click)
        self.connect(self.ui.pushButtonTab4Object, SIGNAL("clicked()"),self.tab4_of_button_click)
        self.connect(self.ui.pushButtonTab4Go, SIGNAL("clicked()"),self.calculateWord)

    def setCentralWidget(self, a):
        pass

    def setStatusBar(self, a):
        pass

    #获得文件
    def tbl_button_click(self):
        self.file_button_click(self.ui.lineEditTab1Tbl, "tbl files (*.tbl)")

    def tbl_button_click_tab4(self):
        self.file_button_click(self.ui.lineEditTab4Tbl, "tbl files (*.tbl)")

    def text1_button_click(self):
        self.file_button_click(self.ui.lineEditTab3Text1)

    def text2_button_click(self):
        self.file_button_click(self.ui.lineEditTab3Text2)

    def tab3_of_button_click(self):
        self.file_button_click(self.ui.lineEditTab3Object)

    def file_button_click(self, lineEdit, fileTypeStr = "txt files (*.txt)"):
        absolute_path = QFileDialog.getOpenFileName(self, 'Open file', '.', fileTypeStr) 
        if absolute_path[0]:
            showTest = absolute_path[0]
            lineEdit.setText(showTest)

    #获得文件目录
    def tab1_tf_button_click(self):
        self.tf_button_click(self.ui.lineEditTab1Source)

    def tab2_tf_button_click(self):
        self.tf_button_click(self.ui.lineEditTab2Source)

    def tab4_tf_button_click(self):
        self.tf_button_click(self.ui.lineEditTab4Source)

    def tf_button_click(self, lineEdit):
        absolute_path = QFileDialog.getExistingDirectory()
        if absolute_path:
            showTest = absolute_path
            lineEdit.setText(showTest)

    #获得目标目录
    def tab1_of_button_click(self):
        self.of_button_click(self.ui.lineEditTab1Object)

    def tab2_of_button_click(self):
        self.of_button_click(self.ui.lineEditTab2Object)

    def tab4_of_button_click(self):
        self.of_button_click(self.ui.lineEditTab4Object)

    def of_button_click(self, lineEdit):
        absolute_path = QFileDialog.getExistingDirectory()
        if absolute_path:
            showTest = absolute_path
            lineEdit.setText(showTest)

    #切换简繁转换
    def transChineseTypeChs(self):
        self.transChineseType = 1

    def transChineseTypeCht(self):
        self.transChineseType = 0

    #获得当前目录下文件
    def getInitTbl(self):
        return self.getInitFile(type = 'tbl', fiedMessage = "请选择字库文件")

    def getInitFirstTxt(self):
        return self.getInitFile(fiedMessage = "请选择文本文件")

    def getInitSecondTxt(self):
        return self.getInitFile(num = 2, fiedMessage = "请选择文本文件")

    def getInitThirdTxt(self):
        return self.getInitFile(num = 2, fiedMessage = "请选择文本文件")

    def getInitFile(self, num = 1, type = 'txt', fiedMessage = "请选择文件"):
        fiedMessage = fiedMessage.decode('utf-8')
        findNum = 0
        files = os.listdir(self.FilePath)
        for f in files:
            if f.split('.')[-1] == type:
                fileStr = self.FilePath + '\\' + f
                findNum += 1
                if findNum == num:
                    return fileStr
        return fiedMessage

    #文本打包
    def go_button_click(self):
        try:
            tblFile = self.ui.lineEditTab1Tbl.text()
            tbl = newtran.loadTbl(tblFile)
        except Exception as e:
            errorMessage = '读取码表文件失败[%s]'%(e)
            self.transError(errorMessage)
            return

        try:
            transFilePath = self.ui.lineEditTab1Source.text()
            objectFilePath = self.ui.lineEditTab1Object.text()
            newtran.convertFile(transFilePath, objectFilePath, tblFile, tbl)
        except Exception as e:
            errorMessage = '打包错误[%s]'%(e)
            errorMessage = errorMessage.decode('utf-8')
            self.transError(errorMessage)
            return

        succeedMessage = "打包成功".decode('utf-8')
        self.transSucceed(succeedMessage)

    #简繁转换
    def transChinese(self):
        sourceDir = self.ui.lineEditTab2Source.text()
        targetDir = self.ui.lineEditTab2Object.text()
        #transChineseType = 0为简体转繁体，否则为繁体转简体
        try:
            fileList = []
            newtran.getFileList(sourceDir, fileList)
            for sourcePath in fileList :
                targetPath = targetDir + '\\' + sourcePath.split(sourceDir)[-1]
                sourceFile = file(sourcePath , 'r')
                targetPathDir = os.path.dirname(targetPath)
                if not os.path.exists(targetPathDir):
                    os.makedirs(targetPathDir)
                targetFile = file(targetPath , 'w')
                for line in sourceFile.readlines() :
                    if self.transChineseType:
                        lineStr = langconv.Converter('zh-hans').convert(line.decode('utf-8'))
                    else:
                        lineStr = langconv.Converter('zh-hant').convert(line.decode('utf-8'))
                    targetFile.write(lineStr.encode('utf-8'))
        except Exception as e:
            errorMessage = '转换错误[%s]'%(e)
            errorMessage = errorMessage.decode('utf-8')
            self.transError(errorMessage)
            return

        succeedMessage = "转换成功".decode('utf-8')
        self.transSucceed(succeedMessage)

    def isListIn(self, str, lists):
        for line in lists:
            if line in str:
                return True
        return False

    def mergeText(self):
        sourceDir1 = self.ui.lineEditTab3Text1.text()
        sourceDir2 = self.ui.lineEditTab3Text2.text()
        objectDir = self.ui.lineEditTab3Object.text()
        try:
            indexList = self.ui.lineEditTab3Index.text().split('|')
            readFile1 = file(sourceDir1, 'r')
            readFile2 = file(sourceDir2, 'r')
            fileObject = file(objectDir, 'w')
            file2Lines = readFile2.readlines()
            file2Len = len(file2Lines)
            file2Index = 0
            for File1Line in readFile1.readlines():
                if not file2Lines:
                    break
                if self.isListIn(File1Line, indexList):
                    while True:
                        if (file2Index == file2Len) or self.isListIn(file2Lines[file2Index], indexList):
                            break
                        fileObject.write(file2Lines[file2Index])
                        file2Index += 1
                    fileObject.write(File1Line)
                    file2Index += 1
                    continue
                fileObject.write(File1Line)
        except Exception as e:
            errorMessage = '合并错误[%s]'%(e)
            errorMessage = errorMessage.decode('utf-8')
            self.transError(errorMessage)
            return

        succeedMessage = "合并成功".decode('utf-8')
        self.transSucceed(succeedMessage)

    #字频统计
    def calculateWord(self):
        try:
            tblFile = self.ui.lineEditTab4Tbl.text()
            tbl = readTBL(tblFile)
        except Exception as e:
            errorMessage = '读取码表文件失败[%s]'%(e)
            self.transError(errorMessage)
            return
        
        try:
            transFilePath = self.ui.lineEditTab4Source.text()
            objectFilePath = self.ui.lineEditTab4Object.text()
            fileList = []
            wordFreq.getFileLists(transFilePath, fileList)
            wF = wordFreq.wordFrequency(fileList)
            wordNotUse = wordFreq.compareJIS(wF, tbl)
            codeNotUse = wordFreq.compareJIS(tbl, wF)
            wordFreq.outputFile(wF, u'字频', objectFilePath + '\\')
            wordFreq.outputFile(wordNotUse, u'文本剩字', objectFilePath + '\\')
            wordFreq.outputFile(codeNotUse, u'码表剩字', objectFilePath + '\\')
        except Exception as e:
            errorMessage = '统计错误[%s]'%(e)
            errorMessage = errorMessage.decode('utf-8')
            self.transError(errorMessage)
            return

        succeedMessage = "统计完毕".decode('utf-8')
        self.transSucceed(succeedMessage)

    def transSucceed(self, succeedMessage):
        QMessageBox.information(self, "Blanc message", succeedMessage, QMessageBox.Ok, QMessageBox.Ok)

    def transError(self, errorMessage):
        QMessageBox.warning (self, "Blanc message", errorMessage, QMessageBox.Ok, QMessageBox.Ok)

app = QApplication(sys.argv)
form = Form()
form.show()
# app.connect(b,SIGNAL("clicked()"),app,SLOT("quit()")) #点击b关闭
app.exec_()

