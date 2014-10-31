# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:29:42 2014

@author: Pyltsin
"""

import unittest

from profiles2 import *
from table import *
pi=3.14159265358979


from  PyQt4 import QtCore
from steel import *

from codes import * 
#список для новых тестов: phi_b при l_d->0 и l_b=0  
#fermaPP, beamPP, columnPP - снип/сп (около 7 тестов!)      

import basa_sort          

class Test_fermaPP(unittest.TestCase):
    def testSNIP(self):
        print 'ferma SNIP'
#        solvePP(self, code, element, typeSolve,typeSection,formSection,sortament,numberSection,steel,lstAddData, lstInputData, lstForce):
#    def checkPP(self, code, element, typeSection,formSection,sortament,numberSection,stl,lstAddData, lstInputData, lstForce):
#        '''Проверка сечений - для начала загружаем все даные и отправляем их в codes, 
#        Исходные данные - отправляем в QString
#        code -  имя норм (СНиП II-23-81*)
#        element - название типа элемента (Ферма), 
#        typeSection- название типа сечения (пока только ПРОКАТ)
#        formSection - название сечения (Уголки в тавр (длинные стор. - вверх))
#        sortament - текстом (QString) названия ГОСТа соратмента (ГОСТ 8509-93 Уголки равнополочные)
#        numberSection - номер сечения (L20x20x3)
#        steel - текстом (QString) сталь (C235)
#        lstAddData - для сечения
#        lstInputData - для расчета
#        lstForce - усилия'''

        code=QtCore.QString(u"СНиП II-23-81*")
        element=QtCore.QString(u"Ферма")
        typeSolve=QtCore.QString(u"Проверка")
        typeSection=QtCore.QString(u"Прокат")
        formSection=QtCore.QString(u"Уголки в тавр (длинные стор. - вверх)")
        sortament=QtCore.QString(u"ГОСТ 8510-86 Уголки неравнополочные")
        numberSection=QtCore.QString(u"L100x63x10")
        steel=QtCore.QString(u"C245")
        lstAddData=[1.]
        lstInputData=[0.8,0.9,200.,1.,2.,400.,1,1.]
        lstForce=[[-5.],[0],[-4.],[5.],[4.]]
        basa=basa_sort.BasaSort()
        out=basa.solvePP(code, element, typeSolve,typeSection,formSection,sortament,numberSection,steel,lstAddData, lstInputData, lstForce)
#        print out[0]
#        print out[1]
#        print out[2]
#        print out[3]
        #сначала частично тестируем 3 список.
        a=15.47*2
        jx=153.9*2
        jy=47.18*2+2*(0.5+1.58)**2*15.47
        ix=(jx/a)**0.5
        iy=(jy/a)**0.5
        lambda_x=200*1./ix
        lambda_y=200*2./iy
        ry=240*10/9.81*10
        phix=0.79
        phiy=0.286
        
        check=out[3][0][0]
        res=a*ry*phiy*0.9/1000.
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][1][0]
        res=a*ry*0.8/1000.
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][2][0]
        res=0.4
        self.assertLess(abs(res-check)/res,0.01)      


        check=out[3][3][0]
        res=phix
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][4][0]
        res=phiy
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][5][0]
        res=a*ry*0.8/1000.
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][6][0]
        res=a*360*100/9.81/1.3*0.8/1000.
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][7][0]
        res=3.14**2*2.1*10**6*jx/(200*1.)**2/1000
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][8][0]
        res=3.14**2*2.1*10**6*jy/(200*2.)**2/1000
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][-1][0]
        res=lambda_y
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][-2][0]
        res=lambda_x
        self.assertLess(abs(res-check)/res,0.01)      

        # тестируем 1 список.
        check=out[1][1][0]
        res=-5.        
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][1]
        res=lambda_y/150.       
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][2]
        res=u'-'
        self.assertEqual(check,res)

        check=out[1][1][3]
        res=5./19.46
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][4]
        res=u'-'
        self.assertEqual(check,res)

        check=out[1][1][5]
        res=lambda_y/150.       
        self.assertLess(abs(res-check)/res,0.01)      


        check=out[1][4][0]
        res=5.        
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][4][1]
        res=lambda_y/400.     
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][4][2]
        res=5/60.55
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][4][3]
        res=u'-'
        self.assertEqual(check,res)

        check=out[1][4][4]
        res=lambda_y/400.     
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][4][5]
        res=u'-'
        self.assertEqual(check,res)

        # тестируем 2 список.
        check=out[2][0][1]
        res=lambda_y/150.         
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][1][1]
        res=5/60.55       
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][2][1]
        res=4
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][3][1]
        res=5./19.46
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][4][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][5][1]
        res=lambda_y/400.  
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][6][1]
        res=lambda_y/150.
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][7][1]
        res=0.4
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][8][1]
        res=0.22
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[2][9][1]
        res=150
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][10][1]
        res=180
        self.assertLess(abs(res-check)/res,0.01)      
        # нулевой список - не тестируется, так как не используется.

#варианты  - только 2 список
        lstInputData=[0.8,0.9,200.,1.,2.,400.,2,200.]

        lstForce=[[-50.],[-40.]]
        out=basa.solvePP(code, element, typeSolve,typeSection,formSection,sortament,numberSection,steel,lstAddData, lstInputData, lstForce)

#        print out[0]
#        print out[1]
#        print out[2]
#        print out[3]
        # тестируем 2 список.
        check=out[2][0][1]
        res=50/19.46    
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][1][1]
        res=0
        self.assertLess(abs(res-check),0.01)      

        check=out[2][2][1]
        res=0
        self.assertLess(abs(res-check),0.01)      

        check=out[2][3][1]
        res=50/19.46  
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][4][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][5][1]
        res=0
        self.assertLess(abs(res-check),0.01)      

        check=out[2][6][1]
        res=lambda_y/150.
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][7][1]
        res=0.4
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][8][1]
        res=0.22
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[2][9][1]
        res=120
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][10][1]
        res=150
        self.assertLess(abs(res-check)/res,0.01)      

#варианты    - только 2 список
        lstInputData=[0.8,0.9,200.,1.,2.,400.,3,200.]
        lstForce=[[-15.],[0],[16.],[17]]
        out=basa.solvePP(code, element, typeSolve,typeSection,formSection,sortament,numberSection,steel,lstAddData, lstInputData, lstForce)

#        print out[0]
#        print out[1]
#        print out[2]
#        print out[3]

        check=out[2][0][1]
        res=15/19.46    
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][1][1]
        res=17/60.55
        self.assertLess(abs(res-check),0.01)      

        check=out[2][2][1]
        res=4
        self.assertLess(abs(res-check),0.01)      

        check=out[2][3][1]
        res=15/19.46  
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][4][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][5][1]
        res=lambda_y/400
        self.assertLess(abs(res-check),0.01)      

        check=out[2][6][1]
        res=lambda_y/200.
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][7][1]
        res=0.4
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][8][1]
        res=0.22
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[2][9][1]
        res=180-60*(15/19.46 )
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][10][1]
        res=210-60*(15/19.46 )
        self.assertLess(abs(res-check)/res,0.01)      


#варианты    - только 2 список
        lstInputData=[0.8,0.9,200.,1.,2.,400.,3,200.]
        lstForce=[[26.],[27]]
        out=basa.solvePP(code, element, typeSolve,typeSection,formSection,sortament,numberSection,steel,lstAddData, lstInputData, lstForce)

#        print out[0]
#        print out[1]
#        print out[2]
#        print out[3]

        check=out[2][0][1]
        res=27/60.55  
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][1][1]
        res=27/60.55 
        self.assertLess(abs(res-check),0.01)      

        check=out[2][2][1]
        res=2
        self.assertLess(abs(res-check),0.01)      

        check=out[2][3][1]
        res=0
        self.assertLess(abs(res-check),0.01)      

        check=out[2][4][1]
        res=0
        self.assertLess(abs(res-check),0.01)      

        check=out[2][5][1]
        res=lambda_y/400
        self.assertLess(abs(res-check),0.01)      

        check=out[2][6][1]
        res=0
        self.assertLess(abs(res-check),0.01)      

        check=out[2][7][1]
        res=0.4
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][8][1]
        res=0.22
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[2][9][1]
        res=150
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][10][1]
        res=180
        self.assertLess(abs(res-check)/res,0.01)      

    def testSP(self):
        print 'ferma SP'
#        solvePP(self, code, element, typeSolve,typeSection,formSection,sortament,numberSection,steel,lstAddData, lstInputData, lstForce):
#    def checkPP(self, code, element, typeSection,formSection,sortament,numberSection,stl,lstAddData, lstInputData, lstForce):
#        '''Проверка сечений - для начала загружаем все даные и отправляем их в codes, 
#        Исходные данные - отправляем в QString
#        code -  имя норм (СНиП II-23-81*)
#        element - название типа элемента (Ферма), 
#        typeSection- название типа сечения (пока только ПРОКАТ)
#        formSection - название сечения (Уголки в тавр (длинные стор. - вверх))
#        sortament - текстом (QString) названия ГОСТа соратмента (ГОСТ 8509-93 Уголки равнополочные)
#        numberSection - номер сечения (L20x20x3)
#        steel - текстом (QString) сталь (C235)
#        lstAddData - для сечения
#        lstInputData - для расчета
#        lstForce - усилия'''

        code=QtCore.QString(u"СП16.13330.2011")
        element=QtCore.QString(u"Ферма")
        typeSolve=QtCore.QString(u"Проверка")
        typeSection=QtCore.QString(u"Прокат")
        formSection=QtCore.QString(u"Уголки в тавр (длинные стор. - вверх)")
        sortament=QtCore.QString(u"ГОСТ 8510-86 Уголки неравнополочные")
        numberSection=QtCore.QString(u"L100x63x10")
        steel=QtCore.QString(u"C245")
        lstAddData=[1.]
        lstInputData=[0.8,0.9,200.,1.,2.,400.,1,1.]
        lstForce=[[-5.],[0],[-4.],[5.],[4.]]
        basa=basa_sort.BasaSort()
        out=basa.solvePP(code, element, typeSolve,typeSection,formSection,sortament,numberSection,steel,lstAddData, lstInputData, lstForce)
#        print out[0]
#        print out[1]
#        print out[2]
#        print out[3]
        #сначала частично тестируем 3 список.
        a=15.47*2
        jx=153.9*2
        jy=47.18*2+2*(0.5+1.58)**2*15.47
        ix=(jx/a)**0.5
        iy=(jy/a)**0.5
        lambda_x=200*1./ix
        lambda_y=200*2./iy
        ry=240*10/9.81*10
        phix=0.72
        phiy=0.286
        
        check=out[3][0][0]
        res=a*ry*phiy*0.9/1000.
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][1][0]
        res=a*ry*0.8/1000.
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][2][0]
        res=0.4
        self.assertLess(abs(res-check)/res,0.01)      


        check=out[3][3][0]
        res=phix
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][4][0]
        res=phiy
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][5][0]
        res=u'c'
        self.assertEqual(check, res)      

        check=out[3][6][0]
        res=u'c'
        self.assertEqual(check, res)      

        check=out[3][7][0]
        res=a*ry*0.8/1000.
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][8][0]
        res=a*360*100/9.81/1.3*0.8/1000.
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][9][0]
        res=3.14**2*2.1*10**6*jx/(200*1.)**2/1000
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][10][0]
        res=3.14**2*2.1*10**6*jy/(200*2.)**2/1000
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][-1][0]
        res=lambda_y
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][-2][0]
        res=lambda_x
        self.assertLess(abs(res-check)/res,0.01)      

        # тестируем 1 список.
        check=out[1][1][0]
        res=-5.        
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][1]
        res=lambda_y/150.       
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][2]
        res=u'-'
        self.assertEqual(check,res)

        check=out[1][1][3]
        res=5./19.46
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][4]
        res=u'-'
        self.assertEqual(check,res)

        check=out[1][1][5]
        res=lambda_y/150.       
        self.assertLess(abs(res-check)/res,0.01)      


        check=out[1][4][0]
        res=5.        
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][4][1]
        res=lambda_y/400.     
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][4][2]
        res=5/60.55
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][4][3]
        res=u'-'
        self.assertEqual(check,res)

        check=out[1][4][4]
        res=lambda_y/400.     
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][4][5]
        res=u'-'
        self.assertEqual(check,res)

        # тестируем 2 список.
        check=out[2][0][1]
        res=lambda_y/150.         
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][1][1]
        res=5/60.55       
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][2][1]
        res=4
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][3][1]
        res=5./19.46
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][4][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][5][1]
        res=lambda_y/400.  
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][6][1]
        res=lambda_y/150.
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][7][1]
        res=0.4
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][8][1]
        res=0.22
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[2][9][1]
        res=150
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][10][1]
        res=180
        self.assertLess(abs(res-check)/res,0.01)      
        # нулевой список - не тестируется, так как не используется.

#варианты  - только 2 список
        lstInputData=[0.8,0.9,200.,1.,2.,400.,2,200.]

        lstForce=[[-50.],[-40.]]
        out=basa.solvePP(code, element, typeSolve,typeSection,formSection,sortament,numberSection,steel,lstAddData, lstInputData, lstForce)

#        print out[0]
#        print out[1]
#        print out[2]
#        print out[3]
        # тестируем 2 список.
        check=out[2][0][1]
        res=50/19.46    
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][1][1]
        res=0
        self.assertLess(abs(res-check),0.01)      

        check=out[2][2][1]
        res=0
        self.assertLess(abs(res-check),0.01)      

        check=out[2][3][1]
        res=50/19.46  
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][4][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][5][1]
        res=0
        self.assertLess(abs(res-check),0.01)      

        check=out[2][6][1]
        res=lambda_y/150.
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][7][1]
        res=0.4
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][8][1]
        res=0.22
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[2][9][1]
        res=120
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][10][1]
        res=150
        self.assertLess(abs(res-check)/res,0.01)      

#варианты    - только 2 список
        lstInputData=[0.8,0.9,200.,1.,2.,400.,3,200.]
        lstForce=[[-15.],[0],[16.],[17]]
        out=basa.solvePP(code, element, typeSolve,typeSection,formSection,sortament,numberSection,steel,lstAddData, lstInputData, lstForce)

#        print out[0]
#        print out[1]
#        print out[2]
#        print out[3]

        check=out[2][0][1]
        res=15/19.46    
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][1][1]
        res=17/60.55
        self.assertLess(abs(res-check),0.01)      

        check=out[2][2][1]
        res=4
        self.assertLess(abs(res-check),0.01)      

        check=out[2][3][1]
        res=15/19.46  
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][4][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][5][1]
        res=lambda_y/400
        self.assertLess(abs(res-check),0.01)      

        check=out[2][6][1]
        res=lambda_y/200.
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][7][1]
        res=0.4
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][8][1]
        res=0.22
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[2][9][1]
        res=180-60*(15/19.46 )
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][10][1]
        res=210-60*(15/19.46 )
        self.assertLess(abs(res-check)/res,0.01)      


#варианты    - только 2 список
        lstInputData=[0.8,0.9,200.,1.,2.,400.,3,200.]
        lstForce=[[26.],[27]]
        out=basa.solvePP(code, element, typeSolve,typeSection,formSection,sortament,numberSection,steel,lstAddData, lstInputData, lstForce)

#        print out[0]
#        print out[1]
#        print out[2]
#        print out[3]

        check=out[2][0][1]
        res=27/60.55  
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][1][1]
        res=27/60.55 
        self.assertLess(abs(res-check),0.01)      

        check=out[2][2][1]
        res=2
        self.assertLess(abs(res-check),0.01)      

        check=out[2][3][1]
        res=0
        self.assertLess(abs(res-check),0.01)      

        check=out[2][4][1]
        res=0
        self.assertLess(abs(res-check),0.01)      

        check=out[2][5][1]
        res=lambda_y/400
        self.assertLess(abs(res-check),0.01)      

        check=out[2][6][1]
        res=0
        self.assertLess(abs(res-check),0.01)      

        check=out[2][7][1]
        res=0.4
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][8][1]
        res=0.22
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[2][9][1]
        res=150
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][10][1]
        res=180
        self.assertLess(abs(res-check)/res,0.01)      

class Test_beamPP(unittest.TestCase):
    def testSNIP(self):
        print 'beam SNIP'
#        solvePP(self, code, element, typeSolve,typeSection,formSection,sortament,numberSection,steel,lstAddData, lstInputData, lstForce):
#    def checkPP(self, code, element, typeSection,formSection,sortament,numberSection,stl,lstAddData, lstInputData, lstForce):
#        '''Проверка сечений - для начала загружаем все даные и отправляем их в codes, 
#        Исходные данные - отправляем в QString
#        code -  имя норм (СНиП II-23-81*)
#        element - название типа элемента (Ферма), 
#        typeSection- название типа сечения (пока только ПРОКАТ)
#        formSection - название сечения (Уголки в тавр (длинные стор. - вверх))
#        sortament - текстом (QString) названия ГОСТа соратмента (ГОСТ 8509-93 Уголки равнополочные)
#        numberSection - номер сечения (L20x20x3)
#        steel - текстом (QString) сталь (C235)
#        lstAddData - для сечения
#        lstInputData - для расчета
#        lstForce - усилия'''

        code=QtCore.QString(u"СНиП II-23-81*")
        element=QtCore.QString(u"Балка")
        typeSolve=QtCore.QString(u"Проверка")
        typeSection=QtCore.QString(u"Прокат")
        formSection=QtCore.QString(u"Двутавр")
        sortament=QtCore.QString(u"ГОСТ 8239-89 Двутавры с уклоном полок")
        numberSection=QtCore.QString(u"24")
        steel=QtCore.QString(u"C255")
        lstAddData=[]
        lstInputData=[1, 0.5, 1000, 0.6, 1, 1, 3, 1]
        lstForce=[[10,1,2,1],[-5,1,-1,1]]
        basa=basa_sort.BasaSort()
        out=basa.solvePP(code, element, typeSolve,typeSection,formSection,sortament,numberSection,steel,lstAddData, lstInputData, lstForce)
#        print out[0]
#        print out[1]
#        print out[2]
#        print out[2]
        #сначала частично тестируем 3 список.

        a=34.77
        jx=3457
        jy=199
        wx=288.1
        wy=34.5
        sx=162.7
        sy=28.88
        phi_b=0.383
        phi_1=0.38
        psi=5.06
        aa=49.34
        ry=2548
        rs=0.58*ry
        
        check=out[3][0][0]
        res=wx*ry*1/1000/100
        mx=res
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][1][0]
        res=wy*ry*1/1000/100
        my=res
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][2][0]
        res=wx*phi_b*ry*0.5/1000/100
        mxb=res
        self.assertLess(abs(res-check)/res,0.01)      


        check=out[3][10][0]
        res=rs*0.56*jx/(sx)/1000
        qx=res
#        print check, res
        self.assertLess(abs(res-check)/res,0.01)      
        
        check=out[3][11][0]
        res=rs*0.95*jy*2/(sy)/1000
        qy=res
#        print check, res
        self.assertLess(abs(res-check)/res,0.01)      

        # тестируем 1 список.
        check=out[1][1][0]
        res=10
        self.assertLess(abs(res-check)/res,0.01)      
        
        check=out[1][1][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][2]
        res=2
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][3]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][4]
        res=10/mxb+1/my
#        print check, res
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][5]
        res=10/mx+1/my
#        print check, res
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][6]
        res=((2/qx)**2+(1/qy)**2)**0.5
#        print check, res
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][7]
        res=((10/mx*ry+1/my*ry)**2+3*(rs*2/qx)**2+3*(rs*1/qy)**2)**0.5/1.15/ry
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][8]
        res=10/mxb+1/my
        self.assertLess(abs(res-check)/res,0.01)      

#       2 список усилий
        check=out[1][2][0]
        res=-5
#        print check, res
        
        self.assertLess(abs(res-check)/res,0.01)      
        
        check=out[1][2][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][2][2]
        res=-1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][2][3]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][2][4]
        res=5/mxb+1/my
#        print check, res
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][2][5]
        res=5/mx+1/my
#        print check, res
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][2][6]
        res=((1/qx)**2+(1/qy)**2)**0.5
#        print check, res
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][2][7]
        res=((5/mx*ry+1/my*ry)**2+3*(rs*1/qx)**2+3*(rs*1/qy)**2)**0.5/1.15/ry
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][2][8]
        res=5/mxb+1/my
        self.assertLess(abs(res-check)/res,0.01)      

        # тестируем 2 список.
        check=out[2][0][1]
        res=8.25
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][1][1]
        res=2.50
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][2][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][3][1]
        res=0.12
        self.assertLess(abs(res-check)/res,0.05)      

        check=out[2][4][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01) 
        
        check=out[2][5][1]
        res=2.17
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][6][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][7][1]
        res=8.25
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][8][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][9][1]
        res=0.38
        self.assertLess(abs(res-check)/res,0.012)      

        check=out[2][10][1]
        res=0.33
        self.assertLess(abs(res-check)/res,0.012)      

    def testSP(self):
        print 'beam SP'
#        solvePP(self, code, element, typeSolve,typeSection,formSection,sortament,numberSection,steel,lstAddData, lstInputData, lstForce):
#    def checkPP(self, code, element, typeSection,formSection,sortament,numberSection,stl,lstAddData, lstInputData, lstForce):
#        '''Проверка сечений - для начала загружаем все даные и отправляем их в codes, 
#        Исходные данные - отправляем в QString
#        code -  имя норм (СНиП II-23-81*)
#        element - название типа элемента (Ферма), 
#        typeSection- название типа сечения (пока только ПРОКАТ)
#        formSection - название сечения (Уголки в тавр (длинные стор. - вверх))
#        sortament - текстом (QString) названия ГОСТа соратмента (ГОСТ 8509-93 Уголки равнополочные)
#        numberSection - номер сечения (L20x20x3)
#        steel - текстом (QString) сталь (C235)
#        lstAddData - для сечения
#        lstInputData - для расчета
#        lstForce - усилия'''

        code=QtCore.QString(u"СП16.13330.2011")
        element=QtCore.QString(u"Балка")
        typeSolve=QtCore.QString(u"Проверка")
        typeSection=QtCore.QString(u"Прокат")
        formSection=QtCore.QString(u"Двутавр")
        sortament=QtCore.QString(u"ГОСТ 8239-89 Двутавры с уклоном полок")
        numberSection=QtCore.QString(u"24")
        steel=QtCore.QString(u"C255")
        lstAddData=[]
        lstInputData=[1, 0.5, 1000, 0.6, 1, 1, 3, 1]
        lstForce=[[10,1,2,1],[-5,1,-1,1]]
        basa=basa_sort.BasaSort()
        out=basa.solvePP(code, element, typeSolve,typeSection,formSection,sortament,numberSection,steel,lstAddData, lstInputData, lstForce)
#        print out[0]
#        print out[1]
#        print out[2]
#        print out[2]
        #сначала частично тестируем 3 список.

        a=34.77
        jx=3457
        jy=199
        wx=288.1
        wy=34.5
        sx=162.7
        sy=28.88
        phi_b=0.367
        ry=2446
        rs=0.58*ry
        
        check=out[3][0][0]
        res=wx*ry*1/1000/100
        mx=res
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][1][0]
        res=wy*ry*1/1000/100
        my=res
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][2][0]
        res=wx*phi_b*ry*0.5/1000/100
        mxb=res
        self.assertLess(abs(res-check)/res,0.01)      


        check=out[3][10][0]
        res=rs*0.56*jx/(sx)/1000
        qx=res
#        print check, res
        self.assertLess(abs(res-check)/res,0.01)      
        
        check=out[3][11][0]
        res=rs*0.95*jy*2/(sy)/1000
        qy=res
#        print check, res
        self.assertLess(abs(res-check)/res,0.01)      

        # тестируем 1 список.
        check=out[1][1][0]
        res=10
        self.assertLess(abs(res-check)/res,0.01)      
        
        check=out[1][1][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][2]
        res=2
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][3]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][4]
        res=10/mxb+1/my
#        print check, res
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][5]
        res=10/mx+1/my
#        print check, res
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][6]
        res=((2/qx)**2+(1/qy)**2)**0.5
#        print check, res
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][7]
        res=((10/mx*ry+1/my*ry)**2+3*(rs*2/qx)**2+3*(rs*1/qy)**2)**0.5/1.15/ry
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][8]
        res=10/mxb+1/my
        self.assertLess(abs(res-check)/res,0.01)      

#       2 список усилий
        check=out[1][2][0]
        res=-5
#        print check, res
        
        self.assertLess(abs(res-check)/res,0.01)      
        
        check=out[1][2][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][2][2]
        res=-1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][2][3]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][2][4]
        res=5/mxb+1/my
#        print check, res
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][2][5]
        res=5/mx+1/my
#        print check, res
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][2][6]
        res=((1/qx)**2+(1/qy)**2)**0.5
#        print check, res
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][2][7]
        res=((5/mx*ry+1/my*ry)**2+3*(rs*1/qx)**2+3*(rs*1/qy)**2)**0.5/1.15/ry
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][2][8]
        res=5/mxb+1/my
        self.assertLess(abs(res-check)/res,0.01)      

        # тестируем 2 список.
        check=out[2][0][1]
        res=8.94
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][1][1]
        res=2.60
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][2][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][3][1]
        res=0.13
        self.assertLess(abs(res-check)/res,0.05)      

        check=out[2][4][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01) 
        
        check=out[2][5][1]
        res=2.26
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][6][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][7][1]
        res=8.94
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][8][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][9][1]
        res=0.37
        self.assertLess(abs(res-check)/res,0.012)      

        check=out[2][10][1]
        res=0.33
        self.assertLess(abs(res-check)/res,0.012)      

class Test_columnPP(unittest.TestCase):
    def testSNIP(self):
        print 'Column SNIP'
#        solvePP(self, code, element, typeSolve,typeSection,formSection,sortament,numberSection,steel,lstAddData, lstInputData, lstForce):
#    def checkPP(self, code, element, typeSection,formSection,sortament,numberSection,stl,lstAddData, lstInputData, lstForce):
#        '''Проверка сечений - для начала загружаем все даные и отправляем их в codes, 
#        Исходные данные - отправляем в QString
#        code -  имя норм (СНиП II-23-81*)
#        element - название типа элемента (Ферма), 
#        typeSection- название типа сечения (пока только ПРОКАТ)
#        formSection - название сечения (Уголки в тавр (длинные стор. - вверх))
#        sortament - текстом (QString) названия ГОСТа соратмента (ГОСТ 8509-93 Уголки равнополочные)
#        numberSection - номер сечения (L20x20x3)
#        steel - текстом (QString) сталь (C235)
#        lstAddData - для сечения
#        lstInputData - для расчета
#        lstForce - усилия'''

        code=QtCore.QString(u"СНиП II-23-81*")
        element=QtCore.QString(u"Колонна")
        typeSolve=QtCore.QString(u"Проверка")
        typeSection=QtCore.QString(u"Прокат")
        formSection=QtCore.QString(u"Двутавр")
        sortament=QtCore.QString(u"ГОСТ 8239-89 Двутавры с уклоном полок")
        numberSection=QtCore.QString(u"24")
        steel=QtCore.QString(u"C255")
        lstAddData=[]
        lstInputData=[0.9, 0.5, 100, 2, 3, 4, 400, 1,1]
        lstForce=[[-10,1,2,3,4],[-10,1,-2,3,-4],[-10,-1,2,-3,4],[-20,1,2,3,4],[5,1,2,3,4],[0,1,2,3,4]]
        basa=basa_sort.BasaSort()
        out=basa.solvePP(code, element, typeSolve,typeSection,formSection,sortament,numberSection,steel,lstAddData, lstInputData, lstForce)
#        print out[0]
#        print out[1]
#        print out[2]
#        print out[3]
#        Проверка 4 списка

        a=34.77
        jx=3457
        jy=199
        ix=(jx/a)**0.5
        iy=(jy/a)**0.5
        lambda_x=200*1./ix
        lambda_y=300*1./iy
        ry=250*10/9.81*10
        phix=0.961
        phiy=0.374

        check=out[3][0][0]
        res=a*ry*phiy*0.9/1000.
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][1][0]
        res=a*ry*0.9/1000.
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][2][0]
        res=0.53
        self.assertLess(abs(res-check)/res,0.01)      


        check=out[3][3][0]
        res=phix
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][4][0]
        res=phiy
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][5][0]
        res=a*ry*0.9/1000.
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][6][0]
        res=a*370*100/9.81/1.3*0.9/1000.
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][7][0]
        res=3.14**2*2.1*10**6*jx/(200*1.)**2/1000
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][8][0]
        res=3.14**2*2.1*10**6*jy/(300*1.)**2/1000
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][9][0]
        res=ry*288.1/1000/100*0.9
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][10][0]
        res=ry*34.5/1000/100*0.9
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][11][0]
        res=2.37
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][12][0]
        res=0.58*ry*jx*0.56/163.07/1000*.9
#        print check, res
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][13][0]
        res=0.58*ry*jy*0.95*2/28.88/1000*.9
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][14][0]
        res=0.53
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][15][0]
        res=2.3
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][16][0]
        res=1.22
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][17][0]
        res=.33
        self.assertLess(abs(res-check)/res,0.011)      


        check=out[3][18][0]
        res=.5
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][19][0]
        res=.17
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[3][20][0]
        res=1.3
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][21][0]
        res=a*7850./10000
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][22][0]
        res=ry
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][23][0]
        res=a
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][24][0]
        res=ix
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][25][0]
        res=iy
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][26][0]
        res=lambda_x
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[3][27][0]
        res=lambda_y
        self.assertLess(abs(res-check)/res,0.01)      

#        Проверка 2 списка
        check=out[1][1][0]
        res=-10
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][2]
        res=2
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][3]
        res=3
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][4]
        res=4
        self.assertLess(abs(res-check)/res,0.01)      


        check=out[1][1][5]
        res=3.07
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][6]
        res=((3/15.83)**2+(4/17.37)**2)**0.5
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][8]
        res=10/79.9+1/6.62+2/.79
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][7]
        res=2.45
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][9]
        res=u'-'
        self.assertEqual(check, res)   

        check=out[1][1][10]
        res=u'-'
        self.assertEqual(check, res)   

        check=out[1][1][11]
        res=u'-'
        self.assertEqual(check, res)   

        check=out[1][1][12]
        res=u'-'
        self.assertEqual(check, res)   

        check=out[1][1][13]
        res=u'-'
        self.assertEqual(check, res)   

        check=out[1][1][14]
        res=0.13
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][15]
        res=0.96
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][16]
        res=0.34
        self.assertLess(abs(res-check)/res,0.015)      

        check=out[1][1][17]
        res=0.37
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[1][1][18]
        res=0.249
        self.assertLess(abs(res-check)/res,0.021)      

        check=out[1][1][19]
        res=0.51
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][1][20]
        res=2.03
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][1][21]
        res=1.68
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][1][22]
        res=0.7
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][1][23]
        res=10/79.9+1/2.37+2/0.79
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][2][5]
        res=3.07
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][3][5]
        res=3.07
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][4][23]
        res=2.67
#        print check, res
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][4][24]
        res=0.094
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][4][25]
        res=10.07
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][4][26]
        res=1
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][4][27]
        res=4.38
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][4][28]
        res=0.75
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][4][29]
        res=0.89
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][4][30]
        res=0.94
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][4][31]
        res=0.6
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][4][32]
        res=2.68
        self.assertLess(abs(res-check)/res,0.04)      

        check=out[1][4][33]
        res=0.091
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][4][34]
        res=0.094
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][4][35]
        res=0.89
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][4][36]
        res=u'-'
        self.assertEqual(check, res)     

        check=out[1][4][37]
        res=125.6/120
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][4][38]
        res=400
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][4][39]
        res=120
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][5][8]
        res=5/79.9+1/6.62+2/0.79
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][5][9]
        res=5/79.9+1/2.37+2/0.79
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][5][10]
        res=0.64
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][5][11]
        res=0.64
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][5][12]
        res=3.79
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][5][13]
        res=22
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][5][-4]
        res=125.67/400
        self.assertLess(abs(res-check)/res,0.02)      

        check=out[1][5][-2]
        res=400
        self.assertLess(abs(res-check)/res,0.02)      
#проверяем последний 3 список [2]     
        check=out[2][0][1]
        res=3.07
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][1][1]
        res=0.3
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][2][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][3][1]
        res=2.56
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][4][1]
        res=4
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][5][1]
        res=2.93
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][6][1]
        res=4
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][7][1]
        res=3.01
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][8][1]
        res=5
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][9][1]
        res=0.26
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][10][1]
        res=4
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][11][1]
        res=0.67
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][12][1]
        res=4
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][13][1]
        res=0.37
        self.assertLess(abs(res-check)/res,0.013)      

        check=out[2][14][1]
        res=4
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][15][1]
        res=3.07
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][16][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][17][1]
        res=0.75
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][18][1]
        res=4
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][19][1]
        res=2.76
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][20][1]
        res=4
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][21][1]
        res=0.31
        self.assertLess(abs(res-check)/res,0.014)      

        check=out[2][22][1]
        res=5
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][23][1]
        res=1.05
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][24][1]
        res=1
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][25][1]
        res=0.53
        self.assertLess(abs(res-check)/res,0.01)      

        check=out[2][26][1]
        res=0.33
        self.assertLess(abs(res-check)/res,0.011)      


        lstInputData=[0.9, 0.5, 100, 2, 3, 4,  400, 2,1]
        basa=basa_sort.BasaSort()
        out=basa.solvePP(code, element, typeSolve,typeSection,formSection,sortament,numberSection,steel,lstAddData, lstInputData, lstForce)

        check=out[1][1][-1]
        res=150
        self.assertLess(abs(res-check)/res,0.011)      


        lstInputData=[0.9, 0.5, 100, 2, 3, 4,   400, 3,300]
        basa=basa_sort.BasaSort()
        out=basa.solvePP(code, element, typeSolve,typeSection,formSection,sortament,numberSection,steel,lstAddData, lstInputData, lstForce)

        check=out[1][1][-1]
        res=300
        self.assertLess(abs(res-check)/res,0.011)      
        
if __name__ == "__main__":
    unittest.main()