# -*- coding: utf-8 -*-
"""
Created on Sat Aug 09 22:24:03 2014

@author: Pyltsin
"""
from  PyQt4 import QtCore, QtGui, uic

def copy_past(e, list_inputtable, list_outputtable, window):
    clip = QtGui.QApplication.clipboard()
    for x in list_inputtable:
        if (window.focusWidget()==x):
            table=x
            flag='input'
    for y in list_outputtable:
        if (window.focusWidget()==y):
            table=y
            flag='output'


    if (e.modifiers() & QtCore.Qt.ControlModifier):
        selected = table.selectedRanges()

        if e.key() == QtCore.Qt.Key_V and (flag=='input'):#past
            first_row = selected[0].topRow()
            first_col = selected[0].leftColumn()

            #copied text is split by '\n' and '\t' to paste to the cells
            for r, row in enumerate(clip.text().split('\n')):
                for c, text in enumerate(row.split('\t')):
                    table.setItem(first_row+r, first_col+c, QtGui.QTableWidgetItem(text))

        elif e.key() == QtCore.Qt.Key_C: #copy
            s = ""
            for r in xrange(selected[0].topRow(),selected[0].bottomRow()+1):
                for c in xrange(selected[0].leftColumn(),selected[0].rightColumn()+1):
                    try:
                        s += str(table.item(r,c).text()) + "\t"
                    except AttributeError:
                        s += "\t"
                s = s[:-1] + "\n" #eliminate last '\t'
            clip.setText(s)

