#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

In this example, we create a simple
window in PyQt5.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Main import *

class ParameterItem(QListWidgetItem):

    def __init__(self, str, a=10, b=-0.007, c=0.7, d=0.1, a_down=-27, b_down=0.009, weight=1):
        QListWidgetItem.__init__(self, str)
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.a_down = a_down
        self.b_down = b_down
        self.weight = weight
        self.parameter = [a,b,c,d,a_down,b_down]

class PyQtMain(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.initUI()

    def on_item_changed(self, item):
        # If the changed item is not checked, don't bother checking others
        if not item.checkState():
            return
        i = 0

        # loop through the items until you get None, which
        # means you've passed the end of the list
        while self.model.item(i):
            if not self.model.item(i).checkState():
                return
            i += 1

    def initUI(self):
        self._layout = QHBoxLayout()
        self.setLayout(self._layout)
        self.view = QListWidget(self)
        self.view.setFixedSize(200,300)
        self.view.setWindowTitle('Honey-Do List')
        # Create an empty model for the list's data
        #self.view.setModel(self.model)

        self.Btn_import = QPushButton('import')
        self.Btn_import.clicked.connect(self.btnimport)
        self.Btn_import.setFixedSize(200, 40)

        self.Btn_delete = QPushButton('delete')
        self.Btn_delete.clicked.connect(self.btndelete)
        self.Btn_delete.setFixedSize(200, 40)


        self.qgl = QVBoxLayout()
        self.qgl.addWidget(self.view)
        self.qgl.addWidget(self.Btn_import)
        self.qgl.addWidget(self.Btn_delete)
        inputGroup0 = QGroupBox()
        inputGroup0.setLayout(self.qgl)
        inputGroup0.setFixedSize(220, 450)
        inputGroup0.setTitle('NDVI time seris')

        self.Btn_Draw = QPushButton('Draw')
        self.Btn_Draw.clicked.connect(self.btndraw)
        self.Btn_Draw.setFixedSize(100, 40)

        self.Btn_Clear = QPushButton('Clear~')
        self.Btn_Clear.clicked.connect(self.clearClick)
        self.Btn_Clear.setFixedSize(100, 40)

        self.qgl2 = QVBoxLayout()
        self.qgl2.addWidget(self.Btn_Draw)
        self.qgl2.addWidget(self.Btn_Clear)
        inputGroup1 = QGroupBox()
        inputGroup1.setLayout(self.qgl2)
        inputGroup1.setFixedSize(150, 450)
        inputGroup1.setTitle('operation button')

        self.plotLabel1 = QLabel()
        self.plotLabel1.setFixedSize(450,300)
        self.plotLabel2 = QLabel()
        self.plotLabel2.setFixedSize(500,300)
        self.plotLabel3 = QLabel()
        self.plotLabel3.setFixedSize(500,300)
        '''
        pixMap1 = QPixmap('drawOne.png')
        pixMap2 = QPixmap('drawTwo.png')
        self.plotLabel1.setPixmap(pixMap2)
        self.plotLabel2.setPixmap(pixMap1)
        '''
        qhl1 = QHBoxLayout()
        qhl1.addWidget(self.plotLabel1)
        qhl1.addWidget(self.plotLabel2)
        qhl1.addWidget(self.plotLabel3)
        inputGroup2 = QGroupBox()
        inputGroup2.setLayout(qhl1)
        inputGroup2.setFixedSize(1500, 350)
        inputGroup2.setTitle('image')

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        inputGroup3 = QGroupBox()
        inputGroup3.setLayout(QVBoxLayout())
        inputGroup3.layout().addWidget(inputGroup2)
        inputGroup3.layout().addWidget(self.console)
        inputGroup3.setTitle('output')


        self._layout.addWidget(inputGroup0)
        self._layout.addWidget(inputGroup1)
        self._layout.addWidget(inputGroup3)
        self.setGeometry(300, 300, 400, 600)
        self.setLayout(self._layout)
        self.setWindowTitle('Main')
        self.show()

    def btnimport(self):
        self.inputWin = InputWin(self)

    def btndelete(self):
        # 移除
        if QMessageBox.warning(self, u'OK', u'Are you sure delete?', QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
            item_deleted = self.view.takeItem(self.view.currentRow())
            # 将读取的值设置为None
            item_deleted = None
            print('delelte success!')

    def btndraw(self):

        itemNums = self.view.count()
        if itemNums < 2:
            print("item isn't enough!")
            return
        weightList = []
        inputList = []
        for i in range(itemNums):
            #item = self.view.takeItem(0)
            item = self.view.item(i)
            inputList.append(item.parameter)
            weightList.append(item.weight)
        weightList = list(map(lambda x:x/sum(weightList), weightList))
        [GUDmix, GUDothers, GUDthre, GUDthreothers] = main(inputList, fa=weightList)
        pixMap1 = QPixmap('drawOne.png')
        pixMap2 = QPixmap('drawTwo.png')
        pixMap3 = QPixmap('drawThree.png')
        self.plotLabel1.setPixmap(pixMap1)
        self.plotLabel2.setPixmap(pixMap2)
        self.plotLabel3.setPixmap(pixMap3)
        self.consoleOperation(inputList,weightList,GUDmix,GUDothers, GUDthre, GUDthreothers)

    def clearClick(self):
        self.plotLabel1.setPixmap(QPixmap())
        self.plotLabel2.setPixmap(QPixmap())
        self.plotLabel3.setPixmap(QPixmap())
        self.console.setText('')

    def consoleOperation(self,inputList,weightList,GUDmix,GUDothers, GUDthre, GUDthreothers):
        self.console.append("--------------------------------------")
        for i in range(len(GUDothers)):
            tstr = ' a: ' + str(inputList[i][0]) + ' b: ' + str(inputList[i][1]) + ' c: ' + str(inputList[i][2])+ \
                   ' d: ' + str(inputList[i][3]) + ' a_down: ' + str(inputList[i][4]) + ' b_down: ' + str(inputList[i][5])\
                +' Weight: ' + str(weightList[i])
            self.console.append(tstr)
            self.console.append("This derivation line GUD is :" + str(GUDothers[i]/10) + 'day')
        self.console.append("the mix derivation lenght GUD is :" + str(GUDmix/10) + 'day\n')

        for i in range(len(GUDothers)):
            tstr = ' a: ' + str(inputList[i][0]) + ' b: ' + str(inputList[i][1]) + ' c: ' + str(inputList[i][2])+ \
                   ' d: ' + str(inputList[i][3]) + ' a_down: ' + str(inputList[i][4]) + ' b_down: ' + str(inputList[i][5])\
                +' Weight: ' + str(weightList[i])
            self.console.append(tstr)
            self.console.append("This thre line GUD is :" + str(GUDthreothers[i]/10) + 'day')
        self.console.append("the mix thre lenght GUD is :" + str(GUDthre / 10) + 'day')

class InputWin(QWidget):
    def __init__(self, context:PyQtMain):
        super().__init__()
        self.context = context
        self.initUI()

    def toggledClicked(self):
        if self._parameterButton.isChecked():
            self.inputGroup1.setEnabled(True)
            self.inputGroup2.setEnabled(False)

            print('_parameterButton')
        else:
            self.inputGroup2.setEnabled(True)
            self.inputGroup1.setEnabled(False)
            print('_txtButton')

    def __timeShiftClick(self, value = 100):
        inputData = self.__getInputData()[0]
        inputData[0] = inputData[0] - value * inputData[1]
        inputData[4] = inputData[4] - value * inputData[5]
        #inputData =  [inputData[0], inputData[1], inputData[2], inputData[3], inputData[4], inputData[5]]
        self.__setInputData(inputData)
        self.perviewClick()
        print('time shift!')

    def __NDVImaxShiftClick(self, value = 0.1):
        inputData = self.__getInputData()[0]
        inputData =  [inputData[0], inputData[1], inputData[2] - value, inputData[3], inputData[4], inputData[5]]
        self.__setInputData(inputData)
        self.perviewClick()
        print('max shift!')

    def __NDVIminShiftClick(self, value = 0.1):
        inputData = self.__getInputData()[0]
        inputData =  [inputData[0], inputData[1], inputData[2] - value, inputData[3] + value, inputData[4], inputData[5]]
        self.__setInputData(inputData)
        self.perviewClick()
        print('min shift!')

    def __setInputData(self, inputData):
        for i in range(len(inputData)):
            inputData[i] = round(inputData[i], 4) #小数点后4位
        self.aEdit.setText(str(inputData[0]))
        self.bEdit.setText(str(inputData[1]))
        self.cEdit.setText(str(inputData[2]))
        self.dEdit.setText(str(inputData[3]))
        self.a_downEdit.setText(str(inputData[4]))
        self.b_downEdit.setText(str(inputData[5]))

    def __getInputData(self):
        if self._parameterButton.isChecked():
            a = self.aEdit.toPlainText()
            b = self.bEdit.toPlainText()
            c = self.cEdit.toPlainText()
            d = self.dEdit.toPlainText()
            a_down = self.a_downEdit.toPlainText()
            b_down = self.b_downEdit.toPlainText()
            weigth = self.weigthEdit.toPlainText()
            str = 'a: ' + a + ' b: ' + b + ' c: ' + c + ' d: ' + d + ' a_down: ' + a_down + ' b_down: ' + b_down\
                +' Weight: ' + weigth
            a = float(a)
            b = float(b)
            c = float(c)
            d = float(d)
            a_down = float(a_down)
            b_down = float(b_down)
            weigth = float(weigth)
            print('Do Parameter Method!')
            return [a, b, c, d, a_down, b_down], weigth

        else:
            reply = QMessageBox.information(self,  # 使用infomation信息框
                                            self.titleEdit.text(),
                                            "this module hasn's finished",
                                            QMessageBox.Yes)

    def confirmClick(self):
        if self._parameterButton.isChecked():
            a = self.aEdit.toPlainText()
            b = self.bEdit.toPlainText()
            c = self.cEdit.toPlainText()
            d = self.dEdit.toPlainText()
            a_down = self.a_downEdit.toPlainText()
            b_down = self.b_downEdit.toPlainText()
            weigth = self.weigthEdit.toPlainText()
            str = 'a: ' + a + ' b: ' + b + ' c: ' + c + ' d: ' + d + ' a_down: ' + a_down + ' b_down: ' + b_down\
                +' Weight: ' + weigth
            a = float(a)
            b = float(b)
            c = float(c)
            d = float(d)
            a_down = float(a_down)
            b_down = float(b_down)
            weigth = float(weigth)
            thisItem = ParameterItem(str,a=a,b=b,c=c,d=d,a_down=a_down,b_down=b_down,weight=weigth)
            self.context.view.addItem(thisItem)
            print('Do Parameter Method!')

        else:
            reply = QMessageBox.information(self,  # 使用infomation信息框
                                            self.titleEdit.text(),
                                            "this module hasn's finished",
                                            QMessageBox.Yes)

    def cancerClick(self):
        self.close()

    def inputPath(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,
                                    "Select File",
                                    "C:/",
                                    "All Files (*);;Text Files (*.txt)") #设置文件扩展名过滤,注意用双分号间隔
        self.titleEdit.setText(fileName1)

    def perviewClick(self):
        pictureName = 'preview.png'
        inputData = self.__getInputData()[0]
        drawPreview(inputData, pictureName)
        previewPicture = QPixmap(pictureName)
        self.previewPicture.setPixmap(previewPicture)
        print("hello~ This is perview Click!")

    def initUI(self):

        self.inputGroup0 = QGroupBox()
        self.inputGroup0.setLayout(QHBoxLayout())
        self._parameterButton = QRadioButton("parameter")
        self._txtButton = QRadioButton("txt")
        self._parameterButton.setChecked(True)
        self._parameterButton.toggled.connect(self.toggledClicked)
        self.inputGroup0.layout().addWidget(self._parameterButton)
        self.inputGroup0.layout().addWidget(self._txtButton)
        self.inputGroup0.setTitle('Select which mode is used')

        self.aEdit = QTextEdit()
        self.aEdit.setText('10')
        self.aEdit.setFixedSize(80, 30)
        aLable = QLabel('a:')
        aLable.setFixedSize(30, 30)

        self.bEdit = QTextEdit()
        self.bEdit.setText('-0.007')
        self.bEdit.setFixedSize(80, 30)
        bLable = QLabel('b:')
        bLable.setFixedSize(30, 30)

        self.cEdit = QTextEdit()
        self.cEdit.setText('0.7')
        self.cEdit.setFixedSize(80, 30)
        cLable = QLabel('c:')
        cLable.setFixedSize(30, 30)

        self.dEdit = QTextEdit()
        self.dEdit.setText('0.1')
        self.dEdit.setFixedSize(80, 30)
        dLable = QLabel('d:')
        dLable.setFixedSize(30, 30)

        self.a_downEdit = QTextEdit()
        self.a_downEdit.setFixedSize(80, 30)
        self.a_downEdit.setText('-24.3')
        a_downLabel = QLabel('a_down:')
        a_downLabel.setFixedSize(80, 30)

        self.b_downEdit = QTextEdit()
        self.b_downEdit.setFixedSize(80, 30)
        self.b_downEdit.setText('0.009')
        b_downLabel = QLabel('b_down:')
        b_downLabel.setFixedSize(80, 30)

        self.weigthEdit = QTextEdit()
        self.weigthEdit.setFixedSize(80, 30)
        self.weigthEdit.setText('1')
        weigthLabel = QLabel('weigth:')
        weigthLabel.setFixedSize(80, 30)

        '''
        vbox.addWidget(a_downLabel, 2, 0)
        vbox.addWidget(a_downEdit, 2, 1)
        vbox.addWidget(b_downLabel, 2, 2)
        vbox.addWidget(b_downEdit, 2, 3)
        '''
        hbox1 = QHBoxLayout()
        hbox1.setSpacing(5)
        hbox1.addWidget(aLable)
        hbox1.addWidget(self.aEdit)
        hbox1.addWidget(bLable)
        hbox1.addWidget(self.bEdit)
        hbox1.addWidget(cLable)
        hbox1.addWidget(self.cEdit)
        hbox1.addWidget(dLable)
        hbox1.addWidget(self.dEdit)

        hbox2 = QHBoxLayout()
        hbox2.setSpacing(5)
        hbox2.addWidget(a_downLabel)
        hbox2.addWidget(self.a_downEdit)
        hbox2.addWidget(b_downLabel)
        hbox2.addWidget(self.b_downEdit)
        hbox2.addWidget(weigthLabel)
        hbox2.addWidget(self.weigthEdit)

        vbox = QVBoxLayout()
        vbox.setDirection(vbox.Up)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox1)

        NDVIPath = QLabel('NDVIPath:')
        self.titleEdit = QLineEdit()
        pathInputButton = QPushButton("Input path")
        pathInputButton.clicked.connect(self.inputPath)

        hbox3 = QHBoxLayout()
        hbox3.setSpacing(5)
        hbox3.addWidget(NDVIPath)
        hbox3.addWidget(self.titleEdit)
        hbox3.addWidget(pathInputButton)

        self.inputGroup1 = QGroupBox()
        self.inputGroup1.setTitle('Input MIDI parameter')
        self.inputGroup1.setLayout(vbox)
        self.inputGroup1.setFixedSize(self.width(), 200)

        self.inputGroup2 = QGroupBox()
        self.inputGroup2.setTitle('Input MIDI TXT')
        self.inputGroup2.setLayout(hbox3)
        self.inputGroup2.setFixedSize(self.width(), 100)

        self.okButton = QPushButton("confirm")
        self.okButton.setFixedSize(80, 30)
        self.okButton.clicked.connect(self.confirmClick)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setFixedSize(80, 30)
        self.cancelButton.clicked.connect(self.cancerClick)
        self.previewlButton = QPushButton("Preview")
        self.previewlButton.setFixedSize(80, 30)
        self.previewlButton.clicked.connect(self.perviewClick)

        hbox4 = QHBoxLayout()
        hbox4.addStretch(1)
        hbox4.addWidget(self.previewlButton)
        hbox4.addWidget(self.okButton)
        hbox4.addWidget(self.cancelButton)
        self.inputGroup3 = QGroupBox()
        self.inputGroup3.setLayout(hbox4)
        '''
        inputGroup4 = QGroupBox()
        vbox2 = QVBoxLayout()
        vbox2.layout().addWidget(self.inputGroup0)
        vbox2.layout().addWidget(self.inputGroup1)
        vbox2.layout().addWidget(self.inputGroup2)
        vbox2.layout().addWidget(self.inputGroup3)
        inputGroup4.setLayout(vbox2)
        inputGroup4.setFixedSize(500, 500)
        '''
        self.previewPicture = QLabel()
        self.previewPicture.setFixedSize(450,400)
        self.Btn_GUDtime = QPushButton("GUD time shift")
        self.Btn_GUDtime.clicked.connect(lambda: self.__timeShiftClick(value=100))
        self.Btn_NDVImax = QPushButton("mix NDVI shift")
        self.Btn_NDVImax.clicked.connect(lambda: self.__NDVImaxShiftClick(value=0.1))
        self.Btn_NDVImin = QPushButton("min NDVI shift")
        self.Btn_NDVImin.clicked.connect(lambda: self.__NDVIminShiftClick(value=0.1))

        self.inputGroup4 = QGroupBox()
        hbox5 = QHBoxLayout()
        hbox5.layout().addWidget(self.previewPicture)
        hbox5.layout().addWidget(self.Btn_GUDtime)
        hbox5.layout().addWidget(self.Btn_NDVImax)
        hbox5.layout().addWidget(self.Btn_NDVImin)
        self.inputGroup4.setLayout(hbox5)

        self.setGeometry(300, 300, self.width(), 500)
        self.setLayout(QVBoxLayout())

        #self.layout().addWidget(inputGroup4)
        self.layout().addWidget(self.inputGroup0)
        self.layout().addWidget(self.inputGroup1)
        self.layout().addWidget(self.inputGroup2)
        self.layout().addWidget(self.inputGroup3)
        self.layout().addWidget(self.inputGroup4)
        self.inputGroup2.setEnabled(False)
        self.setWindowTitle('Review')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PyQtMain()
    sys.exit(app.exec_())
