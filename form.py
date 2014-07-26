# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 18:15:04 2014

@author: Pyltsin
"""

from  PyQt4 import QtCore, QtGui, uic
import profiles2 as profiles

class BasaSort():
    def __init__(self):    
        self.list_sort={u'Двутавр':0, u'Швеллер':1,u'Уголок':2, u'Прямоугольная труба':3, u'Труба':4
        , u'Уголки в тавр (длинные стор. - вверх)':5, u'Уголки в тавр (длинные стор. - в бок)':6
        ,u'Уголки в крест':7}
        self.list_input={0:profiles.dvut(1,1,1,1,1,1,0).input_data()
        ,1: profiles.shvel(h=1, b=1, s=1, t=1, r1=1, r2=1, a1=0, r3=1).input_data()
        ,2:[u"h, см",u"b, см",u"t, см",u"r1, см",u"r2, см"]
        ,3:[u"h, см",u"b, см",u"t, см",u"r1, см",u"r2, см",u"r3, см"]
        ,4:[u"d1, см",u"d2, см"]
        ,5:[u"h, см",u"b, см",u"t, см",u"r1, см",u"r2, см",u"r3, см", u"dx, см"]       
        ,6:[u"h, см",u"b, см",u"t, см",u"r1, см",u"r2, см",u"r3, см", u"dx, см"]
        ,7:[u"h, см",u"b, см",u"t, см",u"r1, см",u"r2, см",u"r3, см", u"dx, см", u"dy, см"]}
        

    def key_sortament(self):
        return self.list_sort.keys()
        
    def input_data(self, i):  

        for label in self.list_sort:
            if str(i)==str(label):
                x=self.list_sort[label]

        y=self.list_input[x]        
        return y
    def output_data(self, i, inp):
        for label in self.list_sort:
            if str(i)==str(label):
                x=self.list_sort[label]
        if x==0:
            pr=profiles.dvut(inp[0],inp[1],inp[2],inp[3],inp[4],inp[5],inp[6])
        elif x==1:
            pr=profiles.shvel(inp[0],inp[1],inp[2],inp[3],inp[4],inp[5],inp[6],inp[7])        
        else:
            False
        return pr
    


class MyWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi("sort_solve.ui", self)
        basa=BasaSort()
        for text in basa.key_sortament():
            self.listWidget.addItem(text)
        self.listWidget.currentItemChanged.connect(table_head)
        self.inputtable.currentItemChanged.connect(table_clear_output)
        self.solvebutton.clicked.connect(solve)

def solve():
    try: 
        lab=window.listWidget.currentItem().text()
        countcolumn=window.inputtable.columnCount()
        input_list=[]
        for i in range(0, countcolumn):
            print window.inputtable.item(0, i).text()
            input_list.append(float(window.inputtable.item(0, i).text()))
        basa=BasaSort()
        pr=basa.output_data(lab, input_list)
        window.outputtable.setColumnCount(len(pr.output_list()))
        window.outputtable.setHorizontalHeaderLabels(pr.output_list())    
    except:
        window.messege.insert(u"Ошибка исходных данных")

        
    
def table_clear():
        window.inputtable.clear()
        window.inputtable.setRowCount (1)
        window.outputtable.clear()
        window.outputtable.setRowCount (1)
        window.messege.clear()
        window.outputtable.setColumnCount(0)
def table_clear_output():
        window.outputtable.clear()
        window.outputtable.setRowCount (1)
        window.messege.clear()
        window.outputtable.setColumnCount(0)       
def table_head():
        table_clear()
        lab=window.listWidget.currentItem().text()
        print lab
        basa=BasaSort()
        input_data=basa.input_data(lab)
        window.inputtable.setColumnCount(len(input_data))
        window.inputtable.setHorizontalHeaderLabels(input_data)
    
if __name__=="__main__":
    import sys
    app=QtGui.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())


    