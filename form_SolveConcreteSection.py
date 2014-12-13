# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 18:55:48 2014

@author: Pyltsin
"""

from  PyQt4 import QtCore, QtGui, uic

import win32com.client
import os
import sys
import rcMaterial

class MyWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        
        self.listSection=['Прямоугольник', 'Двутавр', 'Круг']
        self.listSectionRein=[['Угловое', 'По периметру','Равное сверху/снизу' ,'Сверху и снизу', 'Свободное' ],['Сверху/снизу', 'Свободное'],['По кругу']]
        self.listSectionProp=[['h, см', 'b, см'],['h1, см', 'h2, см',  'h3, см', 'b1, см', 'b2, см', 'b3, см'],['d, см']]
        self.listSectionReinPropCheck=[
                                        [['a, см', 'd, cм'],
                                         ['n1, см', 'n2, см','a, см', 'd, cм'],
                                         ['n1, см','a, см', 'd, cм'],
                                         ['n1, см', 'n2, см','a1, см','a2, см', 'd1, cм', 'd2, cм']
                                        ],
                                        [['n1, см', 'n2, см','a1, см','a2, см', 'd1, cм', 'd2, cм']
                                        ],
                                        [['n1, см','a, см', 'd, cм']]
                                    ]

        self.listSectionReinPropCheck=[
                                        [['a, см'],
                                         ['a, см'],
                                         ['a, см'],
                                         ['a1, см','a2, см']
                                        ],
                                        [['a1, см','a2, см']
                                        ],
                                        [['a, см']]
                                    ]
                                    
                                    
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi("gui/solve_concrete_section.ui", self)
        
#        связывеам нормы с материалами - ппока только отечественные нормы
        self.boxCode.currentIndexChanged.connect(self.changeCode)
        self.changeCode()

        self.boxTypeSection.currentIndexChanged.connect(self.changeTypeSection)
        self.changeTypeSection()

        self.boxTypeSolve.currentIndexChanged.connect(self.changeTypeSolve)
        self.changeTypeSolve()
        
#       связываем прочность и трещиностойкость
        self.checkBoxPS1.clicked.connect(self.changeCheckBoxSolve)
        self.checkBoxPS2.clicked.connect(self.changeCheckBoxSolve)
        self.checkBoxD.clicked.connect(self.changeCheckBoxSolve)
        self.changeCheckBoxSolve()
#загружаем формы
        
        
    def changeCheckBoxSolve(self):
        '''работает при изменении что и как считаем'''
#        первый случай - нет галок вообще
        if self.checkBoxPS1.isChecked()==False and self.checkBoxPS2.isChecked()==False:
        
            self.checkBoxPS1.setChecked(True)
            self.checkBoxD.setChecked(False)
            self.changeCheckBoxSolve()
#   если расчет прочности галка стоит:
        if self.checkBoxPS1.isChecked()==True:
            self.checkBoxD.setEnabled(True)
            self.tabLoad.setEnabled(True)
        else:
            self.checkBoxD.setEnabled(False)
            self.checkBoxD.setChecked(False)
            self.tabLoad.setEnabled(False)


        if self.checkBoxPS2.isChecked()==True:
            self.tabNLoad.setEnabled(True)
        else:
            self.tabNLoad.setEnabled(False)

        self.changeSolvePS1(self.checkBoxPS1.isChecked())
        self.changeSolvePS2(self.checkBoxPS2.isChecked())
        self.changeSolveD(self.checkBoxD.isChecked())
        
    def changeSolvePS1(self, bol):
        '''переключаем при расчете по 1 ps'''
        pass
    def changeSolvePS2(self, bol):
        '''переключаем при расчете по 1 ps'''
        pass
    def changeSolveD(self,bol):
        '''переключаем при расчете по D'''
        pass
        
    def changeTypeSolve(self):
        '''работает при изменении типа расчета'''
        pass

    def changeTypeSection(self):
        '''работает при изменении типа сечения'''
        pass
    def changeCode(self):
        '''работает при изменении и загрузки норм.
        1. загружаем типы материалов'''
        if self.boxCode.currentIndex()==0:
            self.code=52
        elif self.boxCode.currentIndex()==1:
            self.code=63
        tempRein=rcMaterial.Reinforced()
        tempConc=rcMaterial.Concrete()
        
        if self.code==52:            
            lstRein=tempRein.listSP52()
            lstConc=tempConc.listSP52()
        elif self.code==63:
            lstRein=tempRein.listSP63()
            lstConc=tempConc.listSP63()

        self.loadComboBox(self.boxCodeConc, lstConc)
        self.loadComboBox(self.boxCodeRein, lstRein)
        
    def loadComboBox(self, widget, lst):
        '''load ComboBox'''
        widget.clear()
        widget.addItems(lst)
        
if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())
