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

        #загружаем сортаменты и связываем его изменение

        self.loadSortament()
        self.boxSortament.currentIndexChanged.connect(self.changeSortament)

        #загружаем элементы и связываем его изменение

        self.loadNumberSection()
        self.boxNumberSection.currentIndexChanged.connect(self.changeNumberSection)

        #загружаем сталь и связываем его изменение

        self.loadSteel()
        self.boxSteel.currentIndexChanged.connect(self.changeSteel)

    def loadComboBox(self, widget, lst):
        '''load ComboBox'''
        widget.clear()
        widget.addItems(lst)
    def changeInputData(self):
        '''Делать, когда изменились данные'''
        pass
    
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
        1. меняем список типов сечения
        2. меняем таблицу входных данных
        3. делаем стандартные дейтсивя'''
        pass

    def loadTypeSolve(self):
        pass

    def changeTypeSolve(self):
        pass

    def loadTypeSection(self):
        pass

    def changeTypeSection(self):
        pass

    def loadSortament(self):
        pass

    def changeSortament(self):
        pass

    def loadNumberSection(self):
        pass

    def changeNumberSection(self):
        pass
    
        
        
    def loadSteel(self):
        '''загружаем и ставим список стали'''
        code=self.boxCode.currentText()
        lstSteel=list_steel(code=code,typ_steel='prokat').get_list()
#        print lstSteel
        self.loadComboBox(self.boxSteel, lstSteel)

    def changeSteel(self):
        pass

if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())
