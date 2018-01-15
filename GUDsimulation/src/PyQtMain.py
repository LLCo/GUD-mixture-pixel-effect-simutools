#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
simulation software ：Calculate the mix pixel affect of GUD inversion

Author: Liu Li cong
Last edited: Nov 2017
"""

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QHBoxLayout, QListWidget, QPushButton, QVBoxLayout, QGroupBox,\
    QLabel, QTextEdit, QMessageBox, QRadioButton, QApplication, QLineEdit, QFileDialog,QGridLayout
from Main import *
import txt_ndviseris_read
import sys


class ParameterItem(QListWidgetItem):

    def __init__(self, tstr, a=11.105, b=-0.008, c=0.7, d=0.1, a_down=-24.3, b_down=0.009, weight=1.0, threshold=0.09):
        QListWidgetItem.__init__(self, tstr)
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.a_down = a_down
        self.b_down = b_down
        self.weight = weight
        self.parameter = [a, b, c, d, a_down, b_down]
        self.threshold = threshold


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

        self.Btn_import = QPushButton('Import')
        self.Btn_import.clicked.connect(self.btnimport)
        self.Btn_import.setFixedSize(200, 40)

        self.Btn_delete = QPushButton('Delete')
        self.Btn_delete.clicked.connect(self.btndelete)
        self.Btn_delete.setFixedSize(200, 40)


        self.qgl = QVBoxLayout()
        self.qgl.addWidget(self.view)
        self.qgl.addWidget(self.Btn_import)
        self.qgl.addWidget(self.Btn_delete)
        inputGroup0 = QGroupBox()
        inputGroup0.setLayout(self.qgl)
        inputGroup0.setFixedSize(220, 450)
        inputGroup0.setTitle('NDVI Time Series')

        self.Btn_Draw = QPushButton('Draw')
        self.Btn_Draw.clicked.connect(self.btndraw)
        self.Btn_Draw.setFixedSize(100, 40)

        self.Btn_Clear = QPushButton('Clear')
        self.Btn_Clear.clicked.connect(self.clearClick)
        self.Btn_Clear.setFixedSize(100, 40)

        self.qgl2 = QVBoxLayout()
        self.qgl2.addWidget(self.Btn_Draw)
        self.qgl2.addWidget(self.Btn_Clear)
        inputGroup1 = QGroupBox()
        inputGroup1.setLayout(self.qgl2)
        inputGroup1.setFixedSize(150, 450)
        inputGroup1.setTitle('Action Buttons')

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
        '''
        qhl1 = QHBoxLayout()
        qhl1.addWidget(self.plotLabel1)
        qhl1.addWidget(self.plotLabel2)
        qhl1.addWidget(self.plotLabel3)
        inputGroup2 = QGroupBox()
        inputGroup2.setLayout(qhl1)
        inputGroup2.setFixedSize(1500, 350)
        inputGroup2.setTitle('Image Result')

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        inputGroup3 = QGroupBox()
        inputGroup3.setLayout(QVBoxLayout())
        inputGroup3.layout().addWidget(inputGroup2)
        inputGroup3.layout().addWidget(self.console)
        inputGroup3.setTitle('Output')
        '''
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        inputGroup3 = QGroupBox()
        grid = QGridLayout()
        inputGroup3.setLayout(grid)
        grid.setSpacing(10)
        grid.addWidget(self.plotLabel1, 1, 0)
        grid.addWidget(self.plotLabel2, 0, 1)
        grid.addWidget(self.plotLabel3, 0, 0)
        grid.addWidget(self.console, 1, 1)
        inputGroup3.setTitle('Output')

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
        '''
        if QMessageBox.warning(self, u'OK', u'Are you sure delete?', QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
            item_deleted = self.view.takeItem(self.view.currentRow())
            # 将读取的值设置为None
            item_deleted = None
            print('delelte success!')
        '''
        item_deleted = self.view.takeItem(self.view.currentRow())

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
            threshold = item.threshold

        weightList = list(map(lambda x:x/sum(weightList), weightList))
        [GUDmix, GUDothers, GUDthre, GUDthreothers] = main(inputList, fa=weightList, thre=threshold)
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
            tstr0 = 'The ' + str(i+1) + 'th line'
            tstr = tstr0 + "'s parameter is->\n  a: " + str(inputList[i][0]) + ' b: ' + \
                   str(inputList[i][1]) + ' c: ' + str(inputList[i][2])+ \
                   ' d: ' + str(inputList[i][3]) + ' a_down: ' + \
                   str(inputList[i][4]) + ' b_down: ' + str(inputList[i][5])+\
                   ' Weight: ' + str(weightList[i])
            self.console.append(tstr)
            self.console.append(tstr0 + "'s threshold GUD is :" + str(GUDothers[i] / 10) + 'day')
            self.console.append(tstr0 + "'s curvature GUD is :" + str(GUDthreothers[i]/10) + 'day\n')

        self.console.append("Mix threshold GUD is :" + str(GUDmix/10) + 'day')
        self.console.append("Mix curvature GUD is :" + str(GUDthre/10) + 'day')


class InputWin(QWidget):
    def __init__(self, context:PyQtMain):
        super().__init__()
        self.context = context
        self.initUI()

    def toggledClicked(self):
        if self._parameterButton.isChecked():
            self.inputGroup1.setEnabled(True)
            self.inputGroup2.setEnabled(False)
            self.inputGroup4right.setEnabled(True)
            print('_parameterButton')
        else:
            self.inputGroup2.setEnabled(True)
            self.inputGroup1.setEnabled(False)
            self.inputGroup4right.setEnabled(False)
            print('_txtButton')

    def __timeShiftClick(self, value=60):
        inputData = self.__getInputData()[0]
        inputData[0] = inputData[0] - value * inputData[1]
        inputData[4] = inputData[4] - value * inputData[5]
        #inputData =  [inputData[0], inputData[1], inputData[2], inputData[3], inputData[4], inputData[5]]
        self.__setInputData(inputData)
        self.perviewClick()
        print('time shift!')

    def __NDVImaxShiftClick(self, value = 0.05):
        inputData = self.__getInputData()[0]
        inputData =  [inputData[0], inputData[1], inputData[2] - value, inputData[3], inputData[4], inputData[5]]
        self.__setInputData(inputData)
        self.perviewClick()
        print('max shift!')

    def __NDVIminShiftClick(self, value = 0.05):
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
                                            self.pathEdit.text(),
                                            "this module hasn's finished",
                                            QMessageBox.Yes)

    def confirmClick(self):
        weigth = self.weigthEdit.toPlainText()
        threshold = float(self.threEdit.toPlainText())
        if self._parameterButton.isChecked():
            a = self.aEdit.toPlainText()
            b = self.bEdit.toPlainText()
            c = self.cEdit.toPlainText()
            d = self.dEdit.toPlainText()
            a_down = self.a_downEdit.toPlainText()
            b_down = self.b_downEdit.toPlainText()

            tstr = 'a: ' + a + ' b: ' + b + ' c: ' + c + ' d: ' + d + ' a_down: ' + a_down + ' b_down: ' + b_down\
                +' Weight: ' + weigth
            a = float(a)
            b = float(b)
            c = float(c)
            d = float(d)
            a_down = float(a_down)
            b_down = float(b_down)
            weigth = float(weigth)

        else:
            '''
            reply = QMessageBox.information(self,  # 使用infomation信息框
                                            self.pathEdit.text(),
                                            "this module hasn's finished",
                                            QMessageBox.Yes)
            '''
            parameters = txt_ndviseris_read.readtxt(self.pathEdit.text())
            a = round(parameters[0], 3)
            b = round(parameters[1], 3)
            c = round(parameters[2], 3)
            d = round(parameters[3], 3)
            a_down = round(parameters[4], 3)
            b_down = round(parameters[5], 3)
            tstr = self.pathEdit.text()
            weigth = float(weigth)

        thisItem = ParameterItem(tstr, a=a, b=b, c=c, d=d, a_down=a_down,\
                                 b_down=b_down, weight=weigth, threshold=threshold)
        self.context.view.addItem(thisItem)

    def cancerClick(self):
        self.close()

    def inputPath(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,
                                    "Select File",
                                    "./",
                                    "All Files (*);;Text Files (*.txt)") #设置文件扩展名过滤,注意用双分号间隔
        self.pathEdit.setText(fileName1)

    def resetClick(self):
        initial_p = ParameterItem("initial parameter")
        self.aEdit.setText(str(initial_p.a))
        self.bEdit.setText(str(initial_p.b))
        self.cEdit.setText(str(initial_p.c))
        self.dEdit.setText(str(initial_p.d))
        self.a_downEdit.setText(str(initial_p.a_down))
        self.b_downEdit.setText(str(initial_p.b_down))

    def perviewClick(self):
        if self._parameterButton.isChecked():
            pictureName = 'preview.png'
            inputData = self.__getInputData()[0]
            drawPreview(inputData, pictureName)
            previewPicture = QPixmap(pictureName)
            self.previewPicture.setPixmap(previewPicture)
            print("hello~ This is perview Click!")
        else:
            txtPath = self.pathEdit.text()
            self.parameters = txt_ndviseris_read.readtxt(txtPath)
            previewPicture = QPixmap('preview.png')
            self.previewPicture.setPixmap(previewPicture)

    def initUI(self):

        self.inputGroup0 = QGroupBox()
        self.inputGroup0.setLayout(QHBoxLayout())
        self._parameterButton = QRadioButton("Parameter")
        self._txtButton = QRadioButton("NDVI Series File(.txt)")
        self._parameterButton.setChecked(True)
        self._parameterButton.toggled.connect(self.toggledClicked)
        self.inputGroup0.layout().addWidget(self._parameterButton)
        self.inputGroup0.layout().addWidget(self._txtButton)
        self.inputGroup0.setTitle('Select one import method')

        initial_p = ParameterItem("initial parameter")
        self.aEdit = QTextEdit()
        self.aEdit.setText(str(initial_p.a))
        self.aEdit.setFixedSize(80, 30)
        aLable = QLabel('a:')
        aLable.setFixedSize(30, 30)

        self.bEdit = QTextEdit()
        self.bEdit.setText(str(initial_p.b))
        self.bEdit.setFixedSize(80, 30)
        bLable = QLabel('b:')
        bLable.setFixedSize(30, 30)

        self.cEdit = QTextEdit()
        self.cEdit.setText(str(initial_p.c))
        self.cEdit.setFixedSize(80, 30)
        cLable = QLabel('c:')
        cLable.setFixedSize(30, 30)

        self.dEdit = QTextEdit()
        self.dEdit.setText(str(initial_p.d))
        self.dEdit.setFixedSize(80, 30)
        dLable = QLabel('d:')
        dLable.setFixedSize(30, 30)

        self.a_downEdit = QTextEdit()
        self.a_downEdit.setFixedSize(80, 30)
        self.a_downEdit.setText(str(initial_p.a_down))
        a_downLabel = QLabel('a_down:')
        a_downLabel.setFixedSize(80, 30)

        self.b_downEdit = QTextEdit()
        self.b_downEdit.setFixedSize(80, 30)
        self.b_downEdit.setText(str(initial_p.b_down))
        b_downLabel = QLabel('b_down:')
        b_downLabel.setFixedSize(80, 30)

        self.weigthEdit = QTextEdit()
        self.weigthEdit.setFixedSize(80, 30)
        self.weigthEdit.setText('0.5')
        weigthLabel = QLabel('weight:')
        weigthLabel.setFixedSize(80, 30)

        self.threEdit = QTextEdit()
        self.threEdit.setFixedSize(80, 30)
        self.threEdit.setText('0.09')
        threLabel = QLabel('threshold:')
        threLabel.setFixedSize(60, 30)
        '''
        vbox.addWidget(a_downLabel, 2, 0)
        vbox.addWidget(a_downEdit, 2, 1)
        vbox.addWidget(b_downLabel, 2, 2)
        vbox.addWidget(b_downEdit, 2, 3)
        '''
        '''
        hbox2.addWidget(weigthLabel)
        hbox2.addWidget(self.weigthEdit)
        hbox2.addWidget(threLabel)
        hbox2.addWidget(self.threEdit)
        '''

        vbox = QGridLayout()
        vbox.setSpacing(10)
        vbox.addWidget(aLable, 1, 1)
        vbox.addWidget(self.aEdit, 1, 2)
        vbox.addWidget(bLable, 1, 3)
        vbox.addWidget(self.bEdit, 1, 4)
        vbox.addWidget(cLable, 1, 5)
        vbox.addWidget(self.cEdit, 1, 6)
        vbox.addWidget(dLable, 2, 1)
        vbox.addWidget(self.dEdit, 2, 2)
        vbox.addWidget(a_downLabel, 2, 3)
        vbox.addWidget(self.a_downEdit, 2, 4)
        vbox.addWidget(b_downLabel, 2, 5)
        vbox.addWidget(self.b_downEdit, 2, 6)

        NDVIPath = QLabel('Path:')
        self.pathEdit = QLineEdit()
        pathInputButton = QPushButton("Open")
        pathInputButton.clicked.connect(self.inputPath)

        hbox3 = QHBoxLayout()
        hbox3.setSpacing(5)
        hbox3.addWidget(NDVIPath)
        hbox3.addWidget(self.pathEdit)
        hbox3.addWidget(pathInputButton)

        self.inputGroup1 = QGroupBox()
        self.inputGroup1.setTitle('Input NDVI simulation parameter')
        self.inputGroup1.setLayout(vbox)
        # self.inputGroup2.setFixedSize(self.width(), 200)

        self.inputGroup2 = QGroupBox()
        self.inputGroup2.setTitle('Input NDVI Series')
        self.inputGroup2.setLayout(hbox3)
        # self.inputGroup2.setFixedSize(self.width(), 100)

        self.okButton = QPushButton("Confirm")
        self.okButton.setFixedSize(80, 30)
        self.okButton.clicked.connect(self.confirmClick)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setFixedSize(80, 30)
        self.cancelButton.clicked.connect(self.cancerClick)
        self.previewlButton = QPushButton("Preview")
        self.previewlButton.setFixedSize(80, 30)
        self.previewlButton.clicked.connect(self.perviewClick)
        self.resetButton = QPushButton("Reset")
        self.resetButton.setFixedSize(80, 30)
        self.resetButton.clicked.connect(self.resetClick)

        hbox4 = QHBoxLayout()
        hbox4.addStretch(1)
        hbox4.addWidget(self.previewlButton)
        hbox4.addWidget(self.resetButton)
        hbox4.addWidget(self.okButton)
        hbox4.addWidget(self.cancelButton)
        self.inputGroup3 = QGroupBox()
        self.inputGroup3.setLayout(hbox4)
        self.inputGroup3.setTitle('Action Buttons')
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
        self.Btn_GUDtime = QPushButton("GUD time right shift")
        self.Btn_GUDtime.clicked.connect(lambda: self.__timeShiftClick(value=60))
        self.Btn_NDVImax = QPushButton("mix NDVI Down")
        self.Btn_NDVImax.clicked.connect(lambda: self.__NDVImaxShiftClick(value=0.05))
        self.Btn_NDVImin = QPushButton("min NDVI Up")
        self.Btn_NDVImin.clicked.connect(lambda: self.__NDVIminShiftClick(value=0.05))

        self.Btn_GUDtime_vers = QPushButton("GUD time left shift")
        self.Btn_GUDtime_vers.clicked.connect(lambda: self.__timeShiftClick(value=-60))
        self.Btn_NDVImax_vers = QPushButton("mix NDVI Up")
        self.Btn_NDVImax_vers.clicked.connect(lambda: self.__NDVImaxShiftClick(value=-0.05))
        self.Btn_NDVImin_vers = QPushButton("min NDVI Down")
        self.Btn_NDVImin_vers.clicked.connect(lambda: self.__NDVIminShiftClick(value=-0.05))

        self.inputGroup4 = QGroupBox()

        inputGroup4left = QGroupBox()
        inputGroup4left.setTitle("Preview Image")
        inputGroup4leftLayout = QGridLayout()
        inputGroup4leftLayout.setSpacing(10)
        inputGroup4leftLayout.addWidget(self.previewPicture, 2, 1, 1, 4)
        inputGroup4leftLayout.addWidget(weigthLabel, 1, 1)
        inputGroup4leftLayout.addWidget(self.weigthEdit, 1, 2)
        inputGroup4leftLayout.addWidget(threLabel, 1, 3)
        inputGroup4leftLayout.addWidget(self.threEdit, 1, 4)
        inputGroup4left.setLayout(inputGroup4leftLayout)

        self.inputGroup4right = QGroupBox()
        self.inputGroup4right.setTitle("Change NDVI Series Buttons")
        inputGroup4rightLayout = QVBoxLayout()
        inputGroup4rightLayout.addWidget(self.Btn_GUDtime)
        inputGroup4rightLayout.addWidget(self.Btn_GUDtime_vers)
        inputGroup4rightLayout.addWidget(self.Btn_NDVImax)
        inputGroup4rightLayout.addWidget(self.Btn_NDVImax_vers)
        inputGroup4rightLayout.addWidget(self.Btn_NDVImin_vers)
        inputGroup4rightLayout.addWidget(self.Btn_NDVImin)

        self.inputGroup4right.setLayout(inputGroup4rightLayout)

        hbox5 = QHBoxLayout()
        hbox5.layout().addWidget(inputGroup4left)
        hbox5.layout().addWidget(self.inputGroup4right)
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
        self.setWindowTitle('Import')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PyQtMain()
    sys.exit(app.exec_())
