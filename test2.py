# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 00:02:51 2014

@author: Pyltsin
"""

# -*- coding: cp1251 -*-
import win32com.client
objWord = win32com.client.Dispatch(r'Word.Application',"Администратор",UnicodeToString="cp1251")
objWord.Visible = True
objDoc = objWord.Documents.Add()
objDoc.Activate
objDoc.ActiveWindow.Selection.InsertAfter("Привет.")
objDoc.ActiveWindow.Selection.InsertParagraphAfter
objDoc.ActiveWindow.Selection.InsertAfter("Чувачёк.")
objDoc.ActiveWindow.Selection.InsertParagraphAfter
objDoc.ActiveWindow.Selection.Font.Bold = True
objDoc.ActiveWindow.Selection.EndOf
#objDoc.SaveAs("C:/Test.doc")
del objDocs
objWord.Quit()