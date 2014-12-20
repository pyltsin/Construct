# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 18:55:48 2014

@author: Pyltsin
"""

from  PyQt4 import QtCore, QtGui, uic
from math import sin, cos, sqrt, tan
import win32com.client
import os
import sys
import rcMaterial
import matplotlib
import matplotlib.path as mpath
import matplotlib.patches as mpatches

class MyWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        
        self.listSection=[u'Прямоугольник', u'Двутавр', u'Круг']
        self.listSectionRein=[[u'Угловое', u'По периметру',u'Равное сверху/снизу' ,u'Сверху и снизу', u'Свободное' ],[u'Сверху/снизу', u'Свободное'],[u'По кругу', u'Свободное']]
        self.listSectionProp=[[u'h, см', u'b, см'],[u'b1, см', u'b2, см',  u'b3, см', u'h1, см', u'h2, см', u'h3, см'],[u'd, см']]
        self.listSectionReinPropCheck=[
                                        [[u'a, см', u'd, мм'],
                                         [u'n1', u'n2',u'a, см', u'd, мм'],
                                         [u'n1',u'a, см', u'd, мм'],
                                         [u'n1', u'n2',u'a1, см',u'a2, см', u'd1, мм', u'd2, мм']
                                        ],
                                        [[u'n1', u'n2',u'a1, см',u'a2, см', u'd1, мм', u'd2, мм']
                                        ],
                                        [[u'n1',u'a, см', u'd, мм']]
                                    ]

        self.listSectionReinPropFind=[
                                        [[u'a, см'],
                                         [u'a, см'],
                                         [u'a, см'],
                                         [u'a1, см','a2, см']
                                        ],
                                        [[u'a1, см','a2, см']
                                        ],
                                        [[u'a, см']]
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
        
        self.boxFormConc.currentIndexChanged.connect(self.changeForm)
        self.loadComboBox(self.boxFormConc, self.listSection)    
    
        self.boxFormRein.currentIndexChanged.connect(self.changeRein)
        self.changeRein()
#рисуем формы если могем
        self.buttonDraw.clicked.connect(self.drawForm)
#связываем кнопку по умолчанию 1 пс
        self.buttonPS1.clicked.connect(self.PS1Reset)
        
# связываем счетчик с дейтсвиями
        self.boxCountLoadPS1.valueChanged.connect(self.changeCountTableLoadPS1)
        self.boxCountLoadPS1.setValue(1)

        self.boxCountLoadPS2.valueChanged.connect(self.changeCountTableLoadPS2)
        self.boxCountLoadPS2.setValue(1)
        
        self.changeCountTableLoadPS1()
        self.changeCountTableLoadPS2()

    def changeCountTableLoadPS1(self):
        self.changeCountTableLoad(self.boxCountLoadPS1.value(), self.tableLoadPS1)

    def changeCountTableLoadPS2(self):
        self.changeCountTableLoad(self.boxCountLoadPS2.value(), self.tableLoadPS2)


    def changeCountTableLoad(self, i, widget):
        '''изменяем кол-во строк при изенении счетчика'''
        widget.setRowCount(i)
        for j in range(widget.rowCount()):
            for k in range(widget.columnCount()):
                if widget.item(j,k)==None:
                   widget.setItem(j, k, QtGui.QTableWidgetItem('0'))

    def PS1Reset(self):
        '''сбрасываем на умолчание'''
        self.boxPS1Char.setCurrentIndex(0)
        self.boxPS1Dia.setCurrentIndex(0)
        self.boxPS1Rt.setCurrentIndex(0)
        self.doubleBoxTol.setValue(0.001)
        self.boxNum.setValue(100)
     

    def drawForm(self):
        '''получаем список и рисуем картинку'''
        lst=self.getLstForm()

        if lst!='Error':
            fig = self.mplForm.figure
            ax=fig.add_subplot(111)   
            ax.clear()
            for i in lst:
                if i[0]=='Rectangle':
                    rect = mpatches.Rectangle((i[1][0][0], i[1][0][1]),i[1][1][0]-i[1][0][0],i[1][1][1]-i[1][0][1])      
            
                    ax.add_patch(rect)
    
                elif i[0]=='Circle':
                    circle = mpatches.Circle((i[1][0],i[1][1]), radius=i[1][2]/2., color=[0.,1,0])  
            
                    ax.add_patch(circle)
                elif i[0]=='SolidCircle':
                    circle = mpatches.Circle((i[1][0],i[1][1]), radius=i[1][2]/2., color=[1,0.0,0.0])  
            
                    ax.add_patch(circle)
                    
            ax.relim()
            ax.autoscale_view(tight=True, scalex=True, scaley=True)
            self.mplForm.draw()
        else:
            self.error('Data')
            
        
    def error(self, sign):
        print 'Error:', sign
        
    def getLstForm(self):
        '''берем таблицы, проверяем, меняем и возвращаем готовый список готовый и для rcSolve
                lst=[['Rectangle',[[-1,-1],[1,1]],[100,100],1,1,[0,0,0]],
                 ['Circle',[1,0,-1],[1,1],1,2,[0,0,0]],
                 ['Circle',[1,0,1],[1,1],1,2,[0,0,0]]]
                 lstXY - [1,2,3] 1- x, 2-y, 3-d 
                lstN - список количества мешов [100]
                mat - добавка mat
                sign - коэффициент для площади
                e0rxry - добавка для e0rxr
                '''
        lst=[]
        indFormConc=self.boxFormConc.currentIndex()
        indFormRein=self.boxFormRein.currentIndex()

        tC=self.tableFormConc
        tR=self.tableFormRein
        

        lstConc=self.getItemTable(tC, '+')
        lstRein=self.getItemTable(tR, '+')
        if lstRein=="Error" or lstConc=="Error":
            return 'Error'
        print lstRein, 'lstRein'
        nx=int(self.boxNx.value())
        ny=int(self.boxNy.value())        
        if indFormConc==0:
            y1=lstConc[0][0]
            x1=lstConc[1][0]
            
            lst1=['Rectangle',[[0,0],[x1,y1]],[nx,ny],0,1,[0,0,0]]
            lst.append(lst1)
        elif  indFormConc==1:
            x11=0
            y11=0
            x12=lstConc[0][0]
            y12=lstConc[3][0]
            
            x21=x12/2.-lstConc[1][0]/2.
            x22=x21+lstConc[1][0]
            y21=y12
            y22=y21+lstConc[4][0]
            
            x31=x12/2.-lstConc[2][0]/2.
            x32=x31+lstConc[2][0]
            y31=y22
            y32=y31+lstConc[5][0]
            
            lst1=['Rectangle',[[x11,y11],[x12,y12]],[nx,ny],0,1,[0,0,0]]
            lst2=['Rectangle',[[x21,y21],[x22,y22]],[nx,ny],0,1,[0,0,0]]
            lst3=['Rectangle',[[x31,y31],[x32,y32]],[nx,ny],0,1,[0,0,0]]
            lst.append(lst1)
            lst.append(lst2)
            lst.append(lst3)

        elif  indFormConc==2:
            dd=lstConc[0][0]/1.
            lst1=['SolidCircle',[dd/2.,dd/2.,dd],[nx,ny],0,1,[0,0,0]]
            lst.append(lst1)
            
        lstD=[]
        
        if indFormConc==0 and indFormRein==0:
            a=lstRein[0][0]*1.
            d=lstRein[1][0]/10.
            lstD=[[a,a,d],[x1-a,a,d],[x1-a,y1-a,d],[a,y1-a,d]]
        elif  indFormConc==0 and indFormRein==1:
            n1=lstRein[0][0]
            n2=lstRein[1][0]
            a=lstRein[2][0]*1.
            d=lstRein[3][0]/10.
            lstD=[[a,a,d],[x1-a,a,d],[x1-a,y1-a,d],[a,y1-a,d]]
            for i in range(n1):
                lstTemp=[(x1-2*a)*1./(n1+1)*(1+i)+a,a,d]
                lstTemp1=[(x1-2*a)*1./(n1+1)*(1+i)+a,y1-a,d]
                lstD.append(lstTemp)
                lstD.append(lstTemp1)

            for i in range(n2):
                lstTemp=[a,(y1-2*a)*1./(n2+1)*(1+i)+a,d]
                lstTemp1=[x1-a,(y1-2*a)*1./(n2+1)*(1+i)+a,d]
                lstD.append(lstTemp)
                lstD.append(lstTemp1)

                
        elif  indFormConc==0 and indFormRein==2:
            n1=lstRein[0][0]
            a=lstRein[1][0]*1.
            d=lstRein[2][0]/10.
            if n1!=1:
                for i in range(n1):
                    lstTemp=[(x1-2*a)*1./(n1-1)*(i)+a,a,d]
                    lstTemp1=[(x1-2*a)*1./(n1-1)*(i)+a,y1-a,d]
                    lstD.append(lstTemp)
                    lstD.append(lstTemp1)
            else:
                lstTemp=[x1/2.,a,d]
                lstTemp1=[x1/2.,y1-a,d]
                lstD.append(lstTemp)
                lstD.append(lstTemp1)
                
            
        elif   (indFormConc==0 and indFormRein==3) or (indFormConc==1 and indFormRein==0):
            n1=lstRein[0][0]
            n2=lstRein[1][0]
            a1=lstRein[2][0]*1.
            a2=lstRein[3][0]*1.
            d1=lstRein[4][0]/10.
            d2=lstRein[5][0]/10.
            
            if indFormConc==0:
                x01=0
                x02=0
                xb1=x1
                xb2=x1
                h=y1
            else:
                x01=0
                x02=x31
                xb1=x12
                xb2=x32
                h=y32
            
            if n1!=1:
                for i in range(n1):
                    lstTemp=[(xb1-x01-2*a1)*1./(n1-1)*(i)+a1+x01,a1,d1]
                    lstD.append(lstTemp)
            else:
                lstTemp=[(xb1-x01)/2.+x01,a1,d1]
                lstD.append(lstTemp)
                
            if n2!=1:
                for i in range(n2):
                    lstTemp=[(xb2-x02-2*a2)*1./(n2-1)*(i)+a2+x02,h-a2,d2]
                    lstD.append(lstTemp)
            else:
                lstTemp=[(xb2-x02)/2.+x02,h-a2,d2]
                lstD.append(lstTemp)
                
        elif   (indFormConc==2 and indFormRein==0):
            n=lstRein[0][0]
            a=lstRein[1][0]*1.
            d=lstRein[2][0]/10.
            for i in range(n):
                x=(dd/2.-a)*sin(3.1814*2/n*i)+dd/2.
                y=(dd/2.-a)*cos(3.1814*2/n*i)+dd/2.
                lstTemp=[x,y,d]
                lstD.append(lstTemp)
        else:
            for i in lstRein:
                lstD.append([i[0],i[1],i[2]/10.])
                
        for i in lstD:
            lst.append(['Circle',i,[1,1],1,1,[0,0,0]])
        
        return lst
        
    def changeForm(self):
        '''загружаем данные для ввода 
        и заодно способ ввода арматуры'''
        index=self.boxFormConc.currentIndex()
        self.loadComboBox(self.boxFormRein, self.listSectionRein[index])
        
        self.loadTable(self.tableFormConc, self.listSectionProp[index], [''])

    def getItemTable(self, widget, sign):
        row=widget.rowCount()
        column=widget.columnCount()
        try:
            lst=[]
            for i in range(row):
                lstRow=[]
                for j in range(column):
                    text=widget.item(i,j).text()
                    if "," in text:
                        text=text.replace(',','.')
                    text=int(text)
                    if sign=='+':
                        if text>=0:
                            widget.item(i,j).setText(str(text))
                        else:
                            return 'Error'
                    else:
                        widget.item(i,j).setText(str(text))
                        
                        
                    lstRow.append(text)
                lst.append(lstRow)
            return lst
        except:
            return 'Error'

        
    def changeRein(self):
        '''загружаем форму для ввода'''
        indFormConc=self.boxFormConc.currentIndex()
        indFormRein=self.boxFormRein.currentIndex()
        lstFreeRein=[u'x, см',u'y, см',u'd, мм']
        lstD=[]
        for i in range(30):
            lstD.append(str(i+1))
            
        if self.boxTypeSolve.currentIndex()==0:
            if indFormRein==len(self.listSectionRein[indFormConc])-1:
                self.loadTable(self.tableFormRein, lstD, lstFreeRein)
            else:
                self.loadTable(self.tableFormRein, self.listSectionReinPropCheck[indFormConc][indFormRein], [''])
                
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
#            self.tabLoad.setEnabled(True)
        else:
            self.checkBoxD.setEnabled(False)
            self.checkBoxD.setChecked(False)
#            self.tabLoad.setEnabled(False)


#        if self.checkBoxPS2.isChecked()==True:
#            self.tabNLoad.setEnabled(True)
#        else:
#            self.tabNLoad.setEnabled(False)

        self.changeSolvePS1(self.checkBoxPS1.isChecked())
        self.changeSolvePS2(self.checkBoxPS2.isChecked())
        self.changeSolveD(self.checkBoxD.isChecked())
        
    def changeSolvePS1(self, bol):
        self.tabLoad.setEnabled(bol)  
        self.boxPS1.setEnabled(bol)
        '''переключаем при расчете по 1 ps'''
    def changeSolvePS2(self, bol):
        '''переключаем при расчете по 1 ps'''
        self.tabNLoad.setEnabled(bol)
        self.boxPS2.setEnabled(bol)
        
    def changeSolveD(self,bol):
        '''переключаем при расчете по D'''
        self.boxPSD.setEnabled(bol)
        
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

    def loadTable(self, widget, lstVertical, lstGorisont):
        widget.clear()
        indexV=len(lstVertical)
        indexG=len(lstGorisont)
        widget.setRowCount(indexV)
        widget.setColumnCount(indexG)
        widget.setHorizontalHeaderLabels(lstGorisont)
        widget.setVerticalHeaderLabels(lstVertical)
        for i in range(indexV):
            for j in range(indexG):
                widget.setItem(i, j, QtGui.QTableWidgetItem('0'))
        
if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())
