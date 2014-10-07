# -*- coding: utf-8 -*-
"""
Created on Sat Oct 04 22:22:00 2014

@author: Pyltsin
"""

from  PyQt4 import QtCore, QtGui, uic

from steel import list_steel
import win32com.client
import os
from basa_sort import BasaSort
from key_press_event import copy_past
from py2word import printToWord
import sys

class MyWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi("gui/solve_steel_section.ui", self)
        self.basa=BasaSort()
        #загружаем код и связываем его изменение
        self.loadCode()
        self.boxCode.currentIndexChanged.connect(self.changeCode)

        #загружаем элементы и связываем его изменение

        self.loadElement()
        self.boxElement.currentIndexChanged.connect(self.changeElement)

        #загружаем тип расчета и связываем его изменение

        self.loadTypeSolve()
        self.boxTypeSolve.currentIndexChanged.connect(self.changeTypeSolve)
        
        #загружаем тип сечения и связываем его изменение

        self.loadTypeSection()
        self.boxTypeSection.currentIndexChanged.connect(self.changeTypeSection)

        #загружаем тип расчета и связываем его изменение

        self.loadFormSection()
        self.boxFormSection.currentIndexChanged.connect(self.changeFormSection)


        #загружаем сортаменты и связываем его изменение

        self.loadSortament()
        self.boxSortament.currentIndexChanged.connect(self.changeSortament)

        #загружаем элементы и связываем его изменение

        self.loadNumberSection()
        self.boxNumberSection.currentIndexChanged.connect(self.changeNumberSection)

        #загружаем сталь и связываем его изменение

        self.loadSteel()
        self.boxSteel.currentIndexChanged.connect(self.changeSteel)
        
        #загружаем таблицу и связываем его изменение

        self.loadTableInput()
        self.tableInput.currentItemChanged.connect(self.changeTableInput)
        
        #загружаем таблицу усилий и связываем его изменение
        self.loadTableLoad()
        self.tableLoad.currentItemChanged.connect(self.changeTableInput)

        #загружаем рисунок
        self.loadPicture()
        
        #на всякий случай сбрасываем выходные данные
        self.changeInputData()
        
        #связываем счетчик с дейтсвиями
        self.boxCountLoad.valueChanged.connect(self.changeCountTableLoad)
        self.boxCountLoad.setValue(1)
        self.changeCountTableLoad()

        self.buttonSolve.clicked.connect(self.solve)
    
    def solve(self):
        lst=[]
        rowCount=self.tableLoad.rowCount()
        for i in range(rowCount):
            it=self.tableLoad.item(i, 0).text()
#            print it
            lst.append(int(it))
        print sum(lst)

    def keyPressEvent(self, e):
        """обеспечивает возможность копирования, вставить"""
        copy_past(e, [window.tableInput, window.tableLoad], [], window)

        
    def loadComboBox(self, widget, lst):
        '''load ComboBox'''
        widget.clear()
        widget.addItems(lst)
    def changeInputData(self):
        '''Делать, когда изменились данные'''
        self.tabOutputData.setEnabled(False)
        self.tabGeneralOutputData.setEnabled(False)
    
    def loadCode(self):
        '''загружаем и ставим список норм'''
        lst=self.basa.list_code()
        self.loadComboBox(self.boxCode, lst)

    def changeCode(self):
        '''Делаем когда изменились нормы,
        1. Меняем список стали
        2. Делаем стандартные действия'''
        self.loadSteel()
        self.changeInputData()


    def loadElement(self):
        '''загружаем и ставим список элементов'''
        tempLst=self.basa.output_list_elements()
        lst=[]
        for i in tempLst:
            lst.append(i[0])
#        print lst
        self.loadComboBox(self.boxElement, lst)

    def changeElement(self):
        '''делаем когда изменился тип элемента:
        1. меняем список форму сечения
        2. меняем таблицу входных данных
        3. меняем таблицу усилий
        4. делаем стандартные дейтсивя'''
        
        self.loadFormSection()
        self.loadTableInput()
        self.loadTableLoad()
        self.changeInputData()

    def loadTypeSolve(self):
        '''загружаем и ставим список расчетов - подбор и проверка'''
        lst=[u'Проверка', u'Подбор']
        self.loadComboBox(self.boxTypeSolve, lst)

    def changeTypeSolve(self):
        '''делаем когда изменился тип расчета:
        1. если подбор - заблокировать выбор номера сечения
        2. делаем стандартные дейтсивя'''
        flag=self.boxTypeSolve.currentIndex()
        if flag==0:
            self.boxNumberSection.setEnabled(True)
            self.loadNumberSection()
        elif flag==1:
            self.boxNumberSection.setEnabled(False)
            self.boxNumberSection.clear()
        self.changeInputData()

    def loadTypeSection(self):
        '''загружаем и ставим тип сечения'''
        lst=[u'Прокат']
        self.loadComboBox(self.boxTypeSection, lst)


    def changeTypeSection(self):
        'Пока ничего не делаем'
        pass

    def loadFormSection(self):
        '''загружаем и ставим форму сечения'''

        element=self.boxElement.currentText()
        lst=self.basa.output_list_section(element)
        self.loadComboBox(self.boxFormSection, lst)

    def changeFormSection(self):
        '''делаем когда изменился тип расчета:
        1. загрузить список сортаментов
        2. меняем рисунок
        3. делаем стандартные дейтсивя'''
        self.loadSortament()        
        self.loadPicture()        
        self.changeInputData()
        


    def loadSortament(self):
        '''загружаем и ставим список сортаментов'''
        formSection=self.boxFormSection.currentText()
        lstSortament=self.basa.output_list_sortament(formSection)
        self.loadComboBox(self.boxSortament, lstSortament)


    def changeSortament(self):
        '''делаем когда изменился тип расчета:
        1. загрузить список сортаментов
        2. делаем стандартные дейтсивя'''
        self.loadNumberSection()
        self.changeInputData()

    def loadNumberSection(self):
        '''загружаем и ставим список профилей, если элемент активен'''
        if self.boxNumberSection.isEnabled():
            formSection=self.boxFormSection.currentText()
            sortament=self.boxSortament.currentText()
            lstNumberSection=self.basa.output_list_sect_num(sortament, formSection)
            self.loadComboBox(self.boxNumberSection, lstNumberSection)

    def changeNumberSection(self):
        '''делаем когда изменился номер профиоя:
        1. делаем стандартные дейтсивя'''
        self.changeInputData()
    
        
        
    def loadSteel(self):
        '''загружаем и ставим список стали'''
        code=self.boxCode.currentText()
        lstSteel=list_steel(code=code,typ_steel='prokat').get_list()
#        print lstSteel
        self.loadComboBox(self.boxSteel, lstSteel)

    def changeSteel(self):
        '''делаем когда изменилась сталь:
        1. делаем стандартные дейтсивя'''
        self.changeInputData()

    def loadTableInput(self):
        '''загружаем данные в таблицу'''
        self.tableInput.clear()
        code=self.boxCode.currentText()
        element=self.boxElement.currentText()
        lst=self.basa.lstInputDataPP(code, element)
#        print lst
        ln=len(lst)
        self.tableInput.setRowCount(ln)
        i=-1
        name=[]
        for num in lst:
            i+=1
            if type(num[1][0])==type(0.10) or type(num[1][0])==type(1):
                self.tableInput.setItem(i, 0, QtGui.QTableWidgetItem(""))
            else:
#                print num[1]
                userWidget=QtGui.QComboBox()
                self.loadComboBox(userWidget, num[1])
                self.tableInput.setCellWidget(i,0,userWidget)
                
            name.append(num[0])
        self.tableInput.setVerticalHeaderLabels(name)
            

    
    def changeTableInput(self):
        '''делаем когда изменилась таблица:
        1. делаем стандартные дейтсивя'''
        self.changeInputData()

    def loadTableLoad(self):
        '''загружаем таблицу усилий '''

        self.tableLoad.clear()
        code=self.boxCode.currentText()
        element=self.boxElement.currentText()
        lst=self.basa.lstLoadDataPP(code, element)
        self.tableLoad.setColumnCount(len(lst))
        self.tableLoad.setHorizontalHeaderLabels(lst)

    def changeTableLoad(self):
        '''делаем когда изменилась таблица:
        1. делаем стандартные дейтсивя'''
        self.changeInputData()


    def loadPicture(self):
        '''загружаем рисунок'''
        lab=self.boxFormSection.currentText()
        if lab!="":
#            print lab
            pict=self.basa.pict(lab)
            self.labelPicture.setPixmap(QtGui.QPixmap(pict))    

    def changeCountTableLoad(self):
        '''изменяем кол-во строк при изенении счетчика'''
        i=self.boxCountLoad.value()
        self.tableLoad.setRowCount(i)
        
if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())
