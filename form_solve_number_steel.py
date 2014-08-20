# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 18:15:04 2014

@author: Pyltsin
"""

from  PyQt4 import QtCore, QtGui, uic

from steel import list_steel
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
        self.list_type_element=[u'Ферма',u'Балка']
        self.list_code=self.basa.list_code()
        self.load_combobox(self.type_element, self.list_type_element)
        self.type_element.currentIndexChanged["const QString&"].connect(self.load_sect)
    

#Очистка таблицы вывода
        self.output_table.clear()
        self.output_table.setColumnCount(0)
        self.output_table.setRowCount(0)

#установка флажков
        self.flag_current_code=QtCore.QString(self.list_code[0])
        self.flag_current_count=1
        self.flag_current_type_element=QtCore.QString(self.list_type_element[0])
        self.flag_current_section=QtCore.QString(u'Двутавр')
        self.flag_new=True

#Загрузка таблиц
        self.type_element.currentIndexChanged.connect(self.load_input_table)
#Загрузка сортаментов
        self.load_sect(self.list_type_element[0])

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
    
#выбор рабочей папки
        self.button_folder.clicked.connect(self.show_dia_folder)

#направляем на открытие:
        self.listWidget.itemDoubleClicked.connect(self.load_files)
    def load_files(self):
        folder=self.text_folder.text()
        fil_name=self.listWidget.currentItem().text()
        fil=folder+str(u"\\")+fil_name
        print fil           
    def show_dia_folder(self):
        folder_name = QtGui.QFileDialog.getExistingDirectory(self, 'Open Folfer', '/home')
        self.text_folder.clear()
        self.text_folder.insert(folder_name)
        self.load_list_files(folder_name)
       
    def load_list_files(self, folder_name):
        
        raw_list_files=os.listdir(folder_name)
        list_files=[]
        for x in raw_list_files:
            if x[-4:]=='.txt':
                list_files.append(unicode(x))
            
            
        self.listWidget.clear()
        self.listWidget.addItems(list_files)
        
    def load_combobox(self, widget, lst):
        widget.clear()
        widget.addItems(lst)
        
    def load_sect(self, type_section):
        lst=self.basa.output_list_section(type_section)
        self.load_combobox(self.type_section, lst)
        
    def load_input_table(self):
        current_code=self.type_code.currentText()
        current_count=self.number.value()
        current_type_element=self.type_element.currentText()
        current_section=self.type_section.currentText()
        add_data2=[u'Название', u'Сортамент', u'№ Сечения', u'Сталь']
        
        if self.flag_new==True or current_code!=self.flag_current_code or current_type_element!=self.flag_current_type_element or current_section!=self.flag_current_section:
            self.flag_new=False
            self.flag_current_code=current_code
            self.flag_current_type_element=  current_type_element 
            self.flag_current_section=current_section
            add_data=self.basa.add_data_sostav(current_section)
            data=[u'Расчетная длина']
#            data=self.snipn.solve_data(self.flag_current_type_element)# нет пока таког
            lst=add_data2+add_data+data
            
            self.input_table.clear()
            self.input_table.setRowCount(len(lst))
            self.input_table.setVerticalHeaderLabels(lst)
            self.combobox_sort=[]
            self.combobox_num_sect=[]
            self.combobox_steel=[]
            for i in range(current_count):
                self.load_table_combobox(i)
                

        if current_count>self.flag_current_count:
            for i in range(self.flag_current_count, current_count):
                self.load_table_combobox(i)
            self.flag_current_count=current_count
        
        if current_count<self.flag_current_count:
            
            for i in range(self.flag_current_count,current_count,-1):
                self.combobox_sort.pop(i-1)
                self.combobox_num_sect.pop(i-1)
                self.combobox_steel.pop(i-1)               
            self.flag_current_count=current_count            


                
    class load_section_number():
        def __init__(self, i, parent):
            self.i=i
            self.parent=parent
        def __call__(self):
            i=self.i
            lst_num_sect=self.parent.basa.output_list_sect_num(self.parent.combobox_sort[i].currentText(), self.parent.type_section.currentText())
            self.parent.load_combobox(self.parent.combobox_num_sect[i], lst_num_sect)
        def start(self):
            self.__call__()            
            
                
    def load_table_combobox(self, i):
#сортаменты
        self.combobox_sort.append(QtGui.QComboBox())
        lst_sort=self.basa.output_list_sortament(self.type_section.currentText())
        self.load_combobox(self.combobox_sort[i], lst_sort)
        self.input_table.setCellWidget(1,i,self.combobox_sort[i])
        
        
        
# сечения
        self.combobox_num_sect.append(QtGui.QComboBox())
        load=self.load_section_number(i, self)
        load.start()
        self.input_table.setCellWidget(2,i,self.combobox_num_sect[i])            

        self.combobox_sort[i].currentIndexChanged.connect(self.load_section_number(i, self))
# сталь


        self.combobox_steel.append(QtGui.QComboBox())

        code=self.type_code.currentText()
        steel=list_steel(code=code,typ_steel='prokat')
        lst_steel=steel.get_list()
        self.load_combobox(self.combobox_steel[i], lst_steel)

        self.input_table.setCellWidget(3,i,self.combobox_steel[i]) 
                
    def change_column_table(self, i):
        self.input_table.setColumnCount(i)
        self.load_input_table()
    
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


