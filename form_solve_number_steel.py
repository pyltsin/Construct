# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 18:15:04 2014

@author: Pyltsin
"""

from  PyQt4 import QtCore, QtGui, uic

import win32com.client
import os
from basa_sort import BasaSort
from key_press_event import copy_past
class MyWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi("gui/solve_number_steel.ui", self)
        self.basa=BasaSort()
#Загрузка и установка рассчитываемых типов
        self.list_type_section=[u'Ферма',u'Балка']
        self.list_code=[u'СНиП II-23-81*', u'СП16.13330.2012']
        self.load_combobox(self.type_element, self.list_type_section)
        self.type_element.currentIndexChanged["const QString&"].connect(self.load_sortament)
#Загрузка таблиц
        self.type_element.currentIndexChanged.connect(self.load_input_table)
#Загрузка сортаментов
        self.load_sortament(self.list_type_section[0])

#Получение и передача списка сортамента в табицу:
        self.type_section.currentIndexChanged.connect(self.load_input_table)
        self.type_section.currentIndexChanged.connect(self.load_picture)
        self.load_picture()

#Загрузка списка норм
        self.load_combobox(self.type_code, self.list_code)
        self.type_code.currentIndexChanged.connect(self.load_input_table)
        
#Установка количества:        
        self.number.setValue(1)
        self.number.valueChanged['int'].connect(self.change_column_table)
        self.change_column_table(1)        

#Очистка таблицы вывода
        self.output_table.clear()
        self.output_table.setColumnCount(0)
        self.output_table.setRowCount(0)

    def load_combobox(self, widget, lst):
        widget.clear()
        widget.addItems(lst)
        
    def load_sortament(self, type_section):
        lst=[]        
        for x in self.basa.output_list_elements():
            if type_section==x[0]:
                numbers_element=self.basa.output_list4elements()[x[1]]
                break
#        print numbers_element
        for y in self.basa.key_sortament():
#            print y
            if self.basa.output_dict_sort()[y] in numbers_element:
                lst.append(y)
        print lst
        self.load_combobox(self.type_section, lst)
        
    def load_input_table(self):
        print 'hello!'
    
    def change_column_table(self, i):
        self.input_table.setColumnCount(i)
    
    def load_picture(self):
        lab=self.type_section.currentText()
        if lab!="":
#            print lab
            pict=self.basa.pict(lab)
            self.picture.setPixmap(QtGui.QPixmap(pict))      


if __name__=="__main__":
    import sys
    app=QtGui.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())


