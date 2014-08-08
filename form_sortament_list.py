# -*- coding: utf-8 -*-
"""
Created on Fri Aug 08 22:00:52 2014

@author: Pyltsin
"""

from  PyQt4 import QtCore, QtGui, uic

import win32com.client
import os
from basa_sort import *

sort_list=[
[[u'Двутавры',0], [u'Швеллеры',1]]
    ,[[u"ГОСТ 8239-89 Двутавры с уклоном полок",u'SortamentData\GOST823989.csv'] 
    ,[u"ГОСТ 8239-89 Двутавры с уклоном полок",u'SortamentData\GOST823989.csv'] 
    ,[u"ГОСТ 8239-89 Двутавры с уклоном полок",u'SortamentData\GOST823989.csv'] 
    ,[u"ГОСТ 8239-89 Двутавры с уклоном полок",u'SortamentData\GOST823989.csv'] 
    ,[u"ГОСТ 8239-89 Двутавры с уклоном полок",u'SortamentData\GOST823989.csv'] 
    ,[u"ГОСТ 8239-89 Двутавры с уклоном полок",u'SortamentData\GOST823989.csv'] 
    ,[u"ГОСТ 8239-89 Двутавры с уклоном полок",u'SortamentData\GOST823989.csv'] 
    ,[u"ГОСТ 8239-89 Двутавры с уклоном полок",u'SortamentData\GOST823989.csv'] 
    ,[u"ГОСТ 8239-89 Двутавры с уклоном полок",u'SortamentData\GOST823989.csv']         
    ,[u"ГОСТ 8239-89 Двутавры с уклоном полок",u'SortamentData\GOST823989.csv'] 
    ,[u"ГОСТ 8239-89 Двутавры с уклоном полок",u'SortamentData\GOST823989.csv'] 
    ,[u"ГОСТ 8239-89 Двутавры с уклоном полок",u'SortamentData\GOST823989.csv']]        

    ,[[u"ГОСТ 8239-89 Двутавры с уклоном полок",u'SortamentData\GOST823989.csv'] 
    ,[u"ГОСТ 8239-89 Двутавры с уклоном полок",u'SortamentData\GOST823989.csv'] ]  
]
    
class MyWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi("gui\sortament_list.ui", self)
        load_sort_list(self)
def load_sort_list(window):


    model =  QtGui.QStandardItemModel() 
    parent = model.invisibleRootItem()
    i=0
    for x in sort_list[0]:
        item = QtGui.QStandardItem(x[0])
        item.setEditable(False)
        parent.appendRow(item)
        for y in sort_list[i+1]:
            item2=QtGui.QStandardItem(y[0])
            item2.setEditable(False)

            item.appendRow(item2)
        i=i+1
    model.setHorizontalHeaderItem(0, QtGui.QStandardItem(u'Список сортаментов'))
    sel_model=QtGui.QItemSelectionModel(model)
    window.list_sort.setModel(model)

    window.list_sort.setSelectionModel(sel_model)
    
    model_signal=window.list_sort.selectionModel()
#    QtCore.QObject.connect(model_signal, QtCore.Signal("currentChanged(QModelindex, QModelindex)"),edit_table)
    model_signal.currentChanged.connect(edit_table)
    return 0

def edit_table():
    a=window.list_sort.selectionModel().currentIndex()
    print u'элемент', a
    print u'data', a.data()
    print u'название', a.data().toString()
    print u'папа'
    print u'элемент', a.parent()
    print u'data', a.parent().data()
    print u'название', a.parent().data().toString()
    ind=a.data().toString()
    par_ind=a.parent().data().toString()
    i=0
    for x in sort_list[0]:
        if par_ind==x[0]:
            for y in sort_list[i+1]:
                if ind==y[0]:
                    print y[1]
                    break
            break
        i=i+1
    


if __name__=="__main__":
    import sys
    app=QtGui.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())
