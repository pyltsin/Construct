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
from py2word import printToWord

class MyWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi("gui/solve_number_steel.ui", self)
        self.basa=BasaSort()

#Загрузка и установка рассчитываемых типов
        self.list_type_element=[u'Ферма']
#        self.list_type_element=[u'Ферма',u'Балка']

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
        
#связываем с расчетом
        self.solve_button.clicked.connect(self.solve)

#в ворд
        self.word_button.clicked.connect(self.toWord)     
#закрыть сохранение и и ворд
        self.changed_input_data()
        self.input_table.currentItemChanged.connect(self.changed_input_data)
        
    def changed_input_data(self):
        """закрывает схранение и ворд"""
        self.word_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.text_error.clear()

        self.text_error.insert(u'Расчет не выполнен')

    def keyPressEvent(self, e):
        """обеспечивает возможность копирования, вставить"""
        copy_past(e, [window.input_table], [window.output_table], window)

    def toWord(self):
        try:
            lst=[u'Расчет сечений', self.type_element, self.type_section
            , self.type_code, self.input_table, self.output_table]
    #        , self.type_code, self.input_table]
    
            printToWord(lst)
        except:
            self.changed_input_data()
            self.text_error.clear()
            self.text_error.insert(u'Ошибка импорта в Word')
            
    def load_files(self):
        """Обеспечивает загрузку новых файлов из сохранения - недоделано"""
        folder=self.text_folder.text()
        fil_name=self.listWidget.currentItem().text()
        fil=folder+str(u"\\")+fil_name
        print fil           
        
    def show_dia_folder(self):
        """отправляет список файлов, которые можно открыть в окно"""
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
        self.changed_input_data()
        current_code=self.type_code.currentText()
        current_count=self.number.value()
        current_type_element=self.type_element.currentText()
        current_section=self.type_section.currentText()
        add_data2=[u'Название', u'Сортамент', u'№ Сечения', u'Сталь']
        
        if self.flag_new==True or current_code!=self.flag_current_code or current_type_element!=self.flag_current_type_element or current_section!=self.flag_current_section:

            self.input_table.clear()
            self.input_table.setRowCount(0)
            self.input_table.setColumnCount(current_count+1)
            self.input_table.setColumnCount(current_count)


            self.flag_new=False
            self.flag_current_code=current_code
            self.flag_current_type_element=  current_type_element 
            self.flag_current_section=current_section
            add_data=self.basa.add_data_sostav(current_section)
            
            self.data_lst=self.basa.data_solve(current_type_element)


#            print self.data_lst
            data=[]
            for i in self.data_lst:
                data.append(i[0])
            
#            print data            
#            data=self.basa.data_solve(current_type_element)
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

#обнуление данных
        for i in range(current_count):
            for j in range(self.input_table.rowCount()):
#                print self.input_table.cellWidget(j,i)
                if self.input_table.cellWidget(j,i)==None:
#                    print i, j
                    self.input_table.setItem(j, i, QtGui.QTableWidgetItem(""))

                
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

    def solve(self):
#сбор исходных данных
        class error_data():pass
        current_code=self.type_code.currentText()
        current_count=self.number.value()
        current_type_element=self.type_element.currentText()
        current_section=self.type_section.currentText()
        add_data=self.basa.add_data_sostav(current_section)            
        sdv=len(add_data)+4

        lst_gen=[]
        
        self.data_lst=self.basa.data_solve(current_type_element)
        
        try:
            for i in range(current_count):
                lst=[]
    
                for j in range(self.input_table.rowCount()):
                    if self.input_table.cellWidget(j,i)==None and self.input_table.item(j, i).text()=="" :
                        self.input_table.item(j,i).setText(u"0")
                    if  self.input_table.cellWidget(j,i)==None and ("," in self.input_table.item(j, i).text()):
                        text=self.input_table.item(j, i).text()
                        text=text.replace(',','.')
                        self.input_table.item(j, i).setText(text)
                        
                    if self.input_table.cellWidget(j,i)==None:
                        if j==0:
                            lst.append(self.input_table.item(j,i).text())
                        else:
                            num=self.input_table.item(j,i).text()
                            num=float(num)
#                            print j
#                            print self.data_lst[j-sdv][1][0], self.data_lst[j-sdv][1][0], sdv, num
                            if j>=sdv and self.data_lst[j-sdv][1][0]<num and self.data_lst[j-sdv][1][1]>num:
                                lst.append(num)
                            elif j<sdv:
                                lst.append(num)                                                        
                            else:
                                raise error_data()
                    else:
                        wid=self.input_table.cellWidget(j,i)
                        lst.append(wid.currentText())
    
    
                current_gost=lst[1]
                current_num_sect=lst[2]
                current_steel=lst[3]
                inp=lst[4:]
    #            print current_code, current_type_element, current_section, current_gost, current_num_sect, current_steel, inp
                out=self.basa.output_simple(current_code, current_type_element, current_section, current_gost, current_num_sect, current_steel, inp)
                lst_gen.append(out)
    #ставим данные
                self.output_table.setColumnCount(current_count)
                self.output_table.setRowCount(len(lst_gen[0]))
                
                vert_head=[]
                for i in lst_gen[0]:
                    vert_head.append(i[1])
                self.output_table.setVerticalHeaderLabels(vert_head)
                
            for i in range(current_count):
                for j in range(self.output_table.rowCount()):
                    self.output_table.setItem(j, i, QtGui.QTableWidgetItem("1"))
                    if type(lst_gen[i][j][0])!=type(''):
                        txt="%.2f"%(lst_gen[i][j][0])
                    else:
                        txt=lst_gen[i][j][0]
                    self.output_table.item(j,i).setText(txt)
                    
                  
                    self.output_table.item(j,i).setFlags(QtCore.Qt.ItemFlags(1+2+4+8+6+12+64))
    
    

        except ZeroDivisionError :
            self.changed_input_data()
            self.text_error.clear()
            self.text_error.insert(u'Ошибка')
        except error_data, ValueError:
            self.changed_input_data()
            self.text_error.clear()
            self.text_error.insert(u'Ошибка исходных данных')
            
        else:
            self.word_button.setEnabled(True)
            self.save_button.setEnabled(True)
            self.text_error.clear()
            self.text_error.insert(u'Расчет выполнен')

                
                
if __name__=="__main__":
    import sys
    app=QtGui.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())


