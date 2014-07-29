# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 18:15:04 2014

@author: Pyltsin
"""

from  PyQt4 import QtCore, QtGui, uic
import profiles2 as profiles

class BasaSort(object):
    def __init__(self):
        self.list_sort=[u'Двутавр', u'Швеллер',u'Уголок', u'Прямоугольная труба',
                        u'Труба', u'Уголки в тавр (длинные стор. - вверх)'
                        , u'Уголки в тавр (длинные стор. - в бок)'
                        ,u'Уголки в крест']
        self.dict_sort={u'Двутавр':0, u'Швеллер':1,u'Уголок':2, u'Прямоугольная труба':3,
                        u'Труба':4, u'Уголки в тавр (длинные стор. - вверх)':5
                        , u'Уголки в тавр (длинные стор. - в бок)':6
                        ,u'Уголки в крест':7}
        self.list_input={0:profiles.dvut(1,1,1,1,1,1,0).input_data()
        ,1: profiles.shvel(h=1, b=1, s=1, t=1, r1=1, r2=1, a1=0, r3=1).input_data()
        ,2:profiles.ugol(h=1, b=1, t=0.1, r1=0, r2=0, r3=0).input_data()
        ,3:profiles.truba_pryam(h=1, b=1, t=0.1, r1=0, r2=0).input_data()
        ,4:profiles.ring(r=1, r1=0).input_data()
        ,5:[u"h, см",u"b, см",u"t, см",u"r1, см",u"r2, см",u"r3, см", u"dx, см"]
        ,6:[u"h, см",u"b, см",u"t, см",u"r1, см",u"r2, см",u"r3, см", u"dx, см"]
        ,7:[u"h, см",u"b, см",u"t, см",u"r1, см",u"r2, см",u"r3, см", u"dx, см", u"dy, см"]}

        self.pictures_list={0:'SortamentPicture/dvut.png'
        , 1:'SortamentPicture/shvel.png'
        , 2:'SortamentPicture/ugol.png' 
        , 3:'SortamentPicture/korob.png'
        , 4:'SortamentPicture/ring.png'}


    def key_sortament(self):
        return self.list_sort

    def input_data(self, i):

        for label in self.dict_sort:
            if str(i)==str(label):
                x=self.dict_sort[label]

        y=self.list_input[x]
        return y
    def output_data(self, i, inp):
        for label in self.dict_sort:
            if str(i)==str(label):
                x=self.dict_sort[label]
        if x==0:
            pr=profiles.dvut(inp[0],inp[1],inp[2],inp[3],inp[4],inp[5],inp[6])
        elif x==1:
            pr=profiles.shvel(inp[0],inp[1],inp[2],inp[3],inp[4],inp[5],inp[6],inp[7])
        elif x==2:
            pr=profiles.ugol(inp[0],inp[1],inp[2],inp[3],inp[4],inp[5])
        elif x==3:
            pr=profiles.truba_pryam(inp[0],inp[1],inp[2],inp[3],inp[4])
        elif x==4:
            pr=profiles.ring(inp[0],inp[1])
        return pr
    def pict(self, i):
        for label in self.dict_sort:
            if str(i)==str(label):
                x=self.dict_sort[label]
        return self.pictures_list[x]


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
    window.messege.clear()
    try:
        lab=window.listWidget.currentItem().text()
        countcolumn=window.inputtable.columnCount()
        input_list=[]
        for i in range(0, countcolumn):
#            print type(window.inputtable.item(0, i))
            if window.inputtable.item(0, i).text()=="":
                window.inputtable.item(0, i).setText("0")
#            print window.inputtable.item(0, i).text()
            input_list.append(float(window.inputtable.item(0, i).text()))
        basa=BasaSort()
        pr=basa.output_data(lab, input_list)
        window.outputtable.setColumnCount(len(pr.output_list()))
        window.outputtable.setHorizontalHeaderLabels(pr.output_list())
        j=0
        for i in pr.output_list():
            txt="%.2f"%(pr.output_dict()[i])
            window.outputtable.setItem(0,j,QtGui.QTableWidgetItem(txt))
#            print window.outputtable.item(0,j).setFlags(QtCore.Qt.ItemFlags(1+2+4+8+6+12+64))
            j=j+1
    except (ValueError, AttributeError, ZeroDivisionError):
        window.messege.clear()
        window.messege.insert(u"Ошибка исходных данных")

    else:
        window.messege.insert(u"Расчет выполнен успешно")



def table_clear():
    window.inputtable.clear()
    window.inputtable.setRowCount (1)
    window.outputtable.clear()
    window.outputtable.setRowCount (1)
    window.messege.clear()
    window.outputtable.setColumnCount(0)
def table_clear_output():
    window.messege.clear()
    window.messege.insert(u"Расчет НЕ выполнен")

def table_head():
    table_clear()
    lab=window.listWidget.currentItem().text()
    basa=BasaSort()
    input_data=basa.input_data(lab)
    window.inputtable.setColumnCount(len(input_data))
    window.inputtable.setHorizontalHeaderLabels(input_data)
    pict=basa.pict(lab)
    window.picture.setPixmap(QtGui.QPixmap(pict))
    for i in range(0, window.inputtable.columnCount()):
        window.inputtable.setItem(0, i, QtGui.QTableWidgetItem(""))

if __name__=="__main__":
    import sys
    app=QtGui.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())


