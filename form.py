# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 18:15:04 2014

@author: Pyltsin
"""

from  PyQt4 import QtCore, QtGui, uic
import profiles2 as profiles
import win32com.client
import os

class BasaSort(object):
    def __init__(self):
        self.list_sort=[u'Прямоугольник',u'Двутавр', u'Швеллер',u'Уголок', u'Прямоугольная труба',
                        u'Труба', u'Уголки в тавр (длинные стор. - вверх)'
                        , u'Уголки в тавр (длинные стор. - в бок)'
                        ,u'Уголки в крест']
        self.dict_sort={u'Двутавр':0, u'Швеллер':1,u'Уголок':2, u'Прямоугольная труба':3,
                        u'Труба':4, u'Уголки в тавр (длинные стор. - вверх)':5
                        , u'Уголки в тавр (длинные стор. - в бок)':6
                        ,u'Уголки в крест':7, u'Прямоугольник':8}
        self.list_input={0:profiles.dvut(1,1,1,1,1,1,0).input_data()
        ,1: profiles.shvel(h=1, b=1, s=1, t=1, r1=1, r2=1, a1=0, r3=1).input_data()
        ,2:profiles.ugol(h=1, b=1, t=0.1, r1=0, r2=0, r3=0).input_data()
        ,3:profiles.truba_pryam(h=1, b=1, t=0.1, r1=0, r2=0).input_data()
        ,4:profiles.ring(r=1, r1=0).input_data()
        ,5:profiles.sost_ugol_tavr_st_up(h=1,b=1,t=1,r1=0,r2=0,r3=0, dx=1).input_data()
        ,6:profiles.sost_ugol_tavr_st_right(h=1,b=1,t=1,r1=0,r2=0,r3=0, dx=1).input_data()
        ,7:profiles.sost_ugol_tavr_st_krest(h=1,b=1,t=1,r1=0,r2=0,r3=0, dx=1, dy=1).input_data()
        ,8:profiles.rectangle(1,1).input_data()
        }

        self.pictures_list={0:'SortamentPicture\dvut.png'
        , 1:'SortamentPicture\shvel.png'
        , 2:'SortamentPicture\ugol.png'
        , 3:'SortamentPicture\korob.png'
        , 4:'SortamentPicture\ring.png'
        , 5:'SortamentPicture\sost_ugol_tavr_st_up.png'
        , 6:'SortamentPicture\sost_ugol_tavr_st_right.png'
        , 7:'SortamentPicture\sost_ugol_tavr_st_krest.png'
        , 8:'SortamentPicture\rectangle.png'}

    def output_data(self, i, inp):
        for label in self.dict_sort:
            if i==QtCore.QString(label):
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
        elif x==5:
            pr=profiles.sost_ugol_tavr_st_up(inp[0],inp[1],inp[2],inp[3],inp[4],inp[5],inp[6])
        elif x==6:
            pr=profiles.sost_ugol_tavr_st_right(inp[0],inp[1],inp[2],inp[3],inp[4],inp[5],inp[6])
        elif x==7:
            pr=profiles.sost_ugol_tavr_st_krest(inp[0],inp[1],inp[2],inp[3],inp[4],inp[5],inp[6],inp[7])
        elif x==8:
            pr=profiles.rectangle(inp[0],inp[1])
        return pr
    def pict(self, i):
        for label in self.dict_sort:
            if i==QtCore.QString(label):
                x=self.dict_sort[label]
        return self.pictures_list[x]
    def input_data(self, i):

        for label in self.dict_sort:
#            print type(i)
#            print label
            if i==QtCore.QString(label):
                x=self.dict_sort[label]

        y=self.list_input[x]
        return y


    def key_sortament(self):
        return self.list_sort


class MyWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        uic.loadUi("sort_solve.ui", self)
        basa=BasaSort()
        for text in basa.key_sortament():
            self.listWidget.addItem(text)
        self.listWidget.currentItemChanged.connect(table_head)
        self.inputtable.currentItemChanged.connect(table_clear_output,)
        self.solvebutton.clicked.connect(solve)
        self.wordbutton.clicked.connect(toword)
        self.wordbutton.setEnabled(False)

        self.clip = QtGui.QApplication.clipboard()

    def keyPressEvent(self, e):
        if (window.focusWidget()==window.inputtable):
            self.table=window.inputtable
        elif (window.focusWidget()==window.outputtable):
            self.table=window.outputtable


        if (e.modifiers() & QtCore.Qt.ControlModifier):
            selected = self.table.selectedRanges()

            if e.key() == QtCore.Qt.Key_V and (window.focusWidget()==window.inputtable):#past
                first_row = selected[0].topRow()
                first_col = selected[0].leftColumn()

                #copied text is split by '\n' and '\t' to paste to the cells
                for r, row in enumerate(self.clip.text().split('\n')):
                    for c, text in enumerate(row.split('\t')):
                        self.table.setItem(first_row+r, first_col+c, QtGui.QTableWidgetItem(text))

            elif e.key() == QtCore.Qt.Key_C: #copy
                s = ""
                for r in xrange(selected[0].topRow(),selected[0].bottomRow()+1):
                    for c in xrange(selected[0].leftColumn(),selected[0].rightColumn()+1):
                        try:
                            s += str(self.table.item(r,c).text()) + "\t"
                        except AttributeError:
                            s += "\t"
                    s = s[:-1] + "\n" #eliminate last '\t'
                self.clip.setText(s)

def toword():
    try:
        basa=BasaSort()
        lab=window.listWidget.currentItem().text()
        wordapp = win32com.client.Dispatch("Word.Application")
        wordapp.Visible = 1
        worddoc = wordapp.Documents.Add()
        worddoc.PageSetup.Orientation = 1
        worddoc.PageSetup.BookFoldPrinting = 1
        worddoc.ActiveWindow.Selection.Font.Size = 12
        worddoc.ActiveWindow.Selection.Font.Name="Times New Roman"
        worddoc.ActiveWindow.Selection.BoldRun()
    
        worddoc.ActiveWindow.Selection.TypeText(u"Расчет сечения")
        worddoc.ActiveWindow.Selection.TypeParagraph()
        worddoc.ActiveWindow.Selection.BoldRun()
        worddoc.ActiveWindow.Selection.TypeText(u"Сечение: "+lab)
        worddoc.ActiveWindow.Selection.TypeParagraph()
        for i in sys.path:
    #        print i
    #        print os.listdir(i)
            if 'SortamentPicture' in os.listdir(i):
                home=i
                break
        dir_pict=str(home+'\\'+basa.pict(lab))
    #    print (dir_pict)
    #    dir_pict2='D:\python_my\Construct\SortamentPicture\shvel.png'
        worddoc.ActiveWindow.Selection.InlineShapes.AddPicture(dir_pict)
        worddoc.ActiveWindow.Selection.TypeParagraph()
        worddoc.ActiveWindow.Selection.TypeText(u"Исходные характеристики:")
        worddoc.ActiveWindow.Selection.TypeParagraph()
    
     
        location = worddoc.ActiveWindow.Selection.Range
        table = location.Tables.Add (location, 2, len(basa.input_data(lab)))
        table.ApplyStyleHeadingRows = 1
        table.AutoFormat(16)
        x=1
        for i in basa.input_data(lab):    
            table.Cell(1,x).Range.InsertAfter(i)
            table.Cell(2,x).Range.InsertAfter(window.inputtable.item(0, x-1).text())
            x=x+1
    
    
        worddoc.ActiveWindow.Selection.MoveDown()
        worddoc.ActiveWindow.Selection.MoveDown()
        worddoc.ActiveWindow.Selection.TypeParagraph()  
        worddoc.ActiveWindow.Selection.TypeText(u"Расчетные характеристики:")
        worddoc.ActiveWindow.Selection.TypeParagraph() 
        worddoc.ActiveWindow.Selection.Font.Size = 10
        location2 = worddoc.ActiveWindow.Selection.Range    
        
        output_table=window.outputtable
        lenght_table=output_table.columnCount()
        count_table=(lenght_table-0.5)//7+1
    
        table = location2.Tables.Add (location2, 2*count_table, 7)
        table.ApplyStyleHeadingRows = 1
        table.AutoFormat(16)
    
        for i in range(lenght_table):
            j=(i)//7+1
            z=(i+1)-(j-1)*7
            print j, z
            table.Cell((j-1)*2+1,z).Range.InsertAfter(output_table.horizontalHeaderItem(i).text())
            table.Cell((j-1)*2+2,z).Range.InsertAfter(output_table.item(0, i).text())        
    
        del wordapp
    except:
        window.messege.clear()
        window.messege.insert(u"Ошибка экспорта")
        

def solve():
    window.messege.clear()
    try:
        lab=window.listWidget.currentItem().text()
        countcolumn=window.inputtable.columnCount()
        input_list=[]
        for i in range(0, countcolumn):

            if window.inputtable.item(0, i).text()=="":
                window.inputtable.item(0, i).setText("0")
            if "," in window.inputtable.item(0, i).text():
                text=window.inputtable.item(0, i).text()
                text=text.replace(',','.')
                window.inputtable.item(0, i).setText(text)

            input_list.append(float(window.inputtable.item(0, i).text().replace(',','.')))
        basa=BasaSort()
        pr=basa.output_data(lab, input_list)
        window.outputtable.setColumnCount(len(pr.output_list()))
        window.outputtable.setHorizontalHeaderLabels(pr.output_list())
        j=0
        for i in pr.output_list():
            if type(pr.output_dict()[i])==type(0.1):
                txt="%.2f"%(pr.output_dict()[i])
            else:
                txt=pr.output_dict()[i]
            window.outputtable.setItem(0,j,QtGui.QTableWidgetItem(txt))
            window.outputtable.item(0,j).setFlags(QtCore.Qt.ItemFlags(1+2+4+8+6+12+64))
            j=j+1
    except (ValueError, AttributeError, ZeroDivisionError):
        window.messege.clear()
        window.messege.insert(u"Ошибка исходных данных")

    else:
        window.messege.insert(u"Расчет выполнен успешно")
    window.wordbutton.setEnabled(True)



def table_clear():
    window.inputtable.clear()
    window.inputtable.setRowCount (1)
    window.outputtable.clear()
    window.outputtable.setRowCount (1)
    window.messege.clear()
    window.outputtable.setColumnCount(0)
    window.wordbutton.setEnabled(False)

def table_clear_output():
    window.messege.clear()
    window.messege.insert(u"Расчет НЕ выполнен")
    window.wordbutton.setEnabled(False)
def table_head():
    table_clear()
    lab=window.listWidget.currentItem().text()
    basa=BasaSort()
    input_data=basa.input_data(lab)
    window.inputtable.setColumnCount(len(input_data))
    window.inputtable.setHorizontalHeaderLabels(input_data)
    pict=basa.pict(lab)
    try:
        window.picture.setPixmap(QtGui.QPixmap(pict))
    except():
        window.messege.clear()
        window.messege.insert(u"Ошибка исходных данных")
        
    for i in range(0, window.inputtable.columnCount()):
        window.inputtable.setItem(0, i, QtGui.QTableWidgetItem(""))




if __name__=="__main__":
    import sys
    app=QtGui.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())


