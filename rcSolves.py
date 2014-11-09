# -*- coding: utf-8 -*-
"""
Created on Fri Nov 07 23:42:52 2014

@author: Pyltsin
"""
from table import tables_csv
import numpy as np
import time
import gc
from scipy import interpolate
import math
import rcMaterial
import rcMesh


class Solves(object):
    '''все расчеты производятся относительно центра массы'''
    def __init__(self):
        pass
    def loadForm(self,lst):
        '''Загрузка форм
        lst - список
        lst=[['Rectangle',[[-1,-1],[1,1]],[100,100],1,1,[0,0,0]],
                 ['Circle',[1,0,-1],[1,1],1,2,[0,0,0]],
                 ['Circle',[1,0,1],[1,1],1,2,[0,0,0]]]
        Создает self.formLst - список созданных материалов!'''
                
        formLst=[]
        for i in lst:
            if i[0]=='Rectangle' or i[0]==0:
                formLst.append(rcMesh.Rectangles(i[1],i[2],i[3],i[4],i[5]))
            elif i[0]=='Circle' or i[0]==1:
                formLst.append(rcMesh.Circles(i[1],i[2],i[3],i[4],i[5]))
            elif i[0]=='SolidCircle' or i[0]==2:
                formLst.append(rcMesh.SolidCircles(i[1],i[2],i[3],i[4],i[5]))
            elif i[0]=='Triangle' or i[0]==3:
                formLst.append(rcMesh.Triangles(i[1],i[2],i[3],i[4],i[5]))
            
        self.formLst=formLst
        self.formGen()

    def centerMass(self):
        '''возвращает координаты центра массы'''
        a=0
        sx=0
        sy=0
        for i in self.formLst:
            a+=i.a()
            sx+=i.sx()
            sy+=i.sy()
            
        x=sx/a
        y=sy/a
        return x,y
        
    def formGen(self):
        '''Создает матрицу элементов'''
        lst=self.formLst
        matr=np.array([[0],[0],[0],[0],[0],[0],[0]])
        for i in lst:
            matr=np.concatenate((matr,i.mesh()) ,axis=1)
            
        self.elemMatr=matr
        x,y=self.centerMass()
        self.elemMatr[0]-=x
        self.elemMatr[1]-=y

    def e0rxry2e(self,e0=0,rx=0,ry=0):
        '''создаем матрицу e'''
        elemMatr=self.elemMatr #копируем матрицу, чтобы не испортить старую
        one=np.ones(elemMatr.shape[1]) #создаем матрицу 1 длиной с количества точек e
        
        e=one*(elemMatr[4]+e0)+elemMatr[0]*(elemMatr[5]+rx)+elemMatr[1]*(elemMatr[6]+ry) #e=e+rx*x+ry*y
        return e
    
    def e2d(self, e):
        ''''возвращаем d от e - матрицы списка перемещений'''
        ev=self.e2ev(e)[1] #вернули матрицу e*v
        d33=self.elemMatr[2]*ev
        d13=d33*self.elemMatr[0]
        d23=d33*self.elemMatr[1]
        d11=d13*self.elemMatr[0]
        d22=d23*self.elemMatr[1]
        d12=d13*self.elemMatr[1]
        return [[d11,d12,d13],
                [d12,d22,d23],
                [d13,d23,d33]]

    def e2sigma(self, e):
        '''возвращает матрицу sigma от e'''     
        return np.transpose(self.ufunE2sigma()(e, self.elemMatr[3])[0])


    def funE2sigma(self, e, numMat):
        '''просто фнкция для определения e2sigma от номера материала - для перевода ее в uFun'''
#        print 'fun', self.lstFunE2ev[int(numMat)][0](e),self.lstFunE2ev[int(numMat)][1](e)
        return self.lstFunE2ev[int(numMat)][0](e)

    def ufunE2sigma(self):
        '''возвращает функцию funE2ev для массивов'''
        return np.frompyfunc(self.funE2sigma,2,2)




    def e2sigma2(self, e):
        '''возвращает матрицу sigma от e'''     
#        print self.ufunE2sigma2()(e, self.elemMatr[3])
        return self.ufunE2sigma2()(e, self.elemMatr[3])


    def funE2sigma2(self, e, numMat):
        '''просто фнкция для определения e2sigma от номера материала - для перевода ее в uFun'''
#        print 'e',e
#        print 'fun2', self.lstFunE2ev2[0](e)
#        print 'fun', self.lstFunE2ev2[int(numMat)](e)
        return self.lstFunE2ev2[int(numMat)](e)[0]

    def ufunE2sigma2(self):
        '''возвращает функцию funE2ev для массивов'''
        return np.frompyfunc(self.funE2sigma2,2,1)





    def e2ev(self, e):
        '''возвращает матрицу ev от e'''     
        return np.transpose(self.ufunE2ev()(e, self.elemMatr[3])[0])
    
    
    def funE2ev(self, e, numMat):
        '''просто фнкция для определения e2sigma от номера материала - для перевода ее в uFun'''
#        print 'fun', self.lstFunE2ev[int(numMat)][0](e),self.lstFunE2ev[int(numMat)][1](e)
        return self.lstFunE2ev[int(numMat)][1](e)

    def ufunE2ev(self):
        '''возвращает функцию funE2ev для массивов'''
        return np.frompyfunc(self.funE2ev,2,2)

    def e0rxry2nmxmy(self,e0rxry):
        '''возвращает значение усилий по дополнительным деформациям'''
        e0,rx,ry=e0rxry
        e=self.e0rxry2e(e0,rx,ry) #получили e1
#        print self.e2sigma2(e),'sigma' 
        sigma=self.e2sigma2(e)
        n=sigma*self.elemMatr[2]
        mx=sigma*self.elemMatr[2]*self.elemMatr[0]
        my=sigma*self.elemMatr[2]*self.elemMatr[1]
        nSum=n.sum()
        mxSum=mx.sum()
        mySum=my.sum()
        return nSum, mxSum, mySum
        
    def loadMat(self, lstMat, typLst, lst, typDia, typPS, typTime, typR, typRT):
        '''загружаем материалы и создаем список функций 
        lstMat - список созднных материалов
        typLst - если True - диаграмма создается по списку lst, 
        lst - cписок точек для typLst=True, 
        typDia - тип диаграммы для бетонна, 
        typPS - тип предельного состояния, 
        typTime - long или short для бетона, 
        typR - для бетона, если 1 - просто режется все -, если 2 - после последнего значения - до 0, другое - продлеваем до max, 
        typRT - для бетона, если 1 - просто режется все +, если 2 - после последнего значения - до 0, другое - продлеваем до max'''
        self.lstMat=lstMat
        lstFunDia=[]
        for i in lstMat:
            if i.title()=='Concrete':
                if typLst==False:
                    lstFunDia.append(i.functDia(typDia, typPS, typTime, typR, typRT))
                else:
                    lstFunDia.append(i.functDiaLst(lst))
            elif i.title()=='Reinforced':
                if typLst==False:
                    lstFunDia.append(i.functDia(typPS))
                else:
                    lstFunDia.append(i.functDiaLst(lst))
        self.lstFunE2ev=lstFunDia

        lstFunDia2=[]
        
        for i in lstMat:
            if i.title()=='Concrete':
                if typLst==False:
                    lstFunDia2.append(i.functDia2)
                else:
                    lstFunDia.append(i.functDiaLst(lst))
            elif i.title()=='Reinforced':
                if typLst==False:
                    lstFunDia.append(i.functDia2())
                else:
                    lstFunDia.append(i.functDiaLst(lst))
        self.lstFunE2ev2=lstFunDia2

        

    def nmxmy2e0rxry(n, mx, my, lstForm, lstMat, nn, criter):
        numberElements=lstForm.shape[1]
        cx,cy=centerMass(lstForm)
        formMatr=formGen(lstForm, cx, cy)
    #   возвращает список функций апроксимаций от mat
        matFunE2V=matGenE2V(lstMat)
    #возвращает E
        e=matGenE(lstForm, lstMat)
        e0,rx,ry=0,0,0
        
        v=np.ones(numberElement)
        
        while True:
            da=formMatr[2]*v*e
            dsx=da*formMatr[0]
            dsy=da*formMatr[1]
        
            djx=dsx*formMatr[0]
            djy=dsy*formMatr[1]
            djxy=dsx*formMatr[1]
        
            d11=djx.sum()
            d22=djy.sum()
            d12=djxy.sum()
            d12=dsx.sum()
            d23=dsy.sum()
            d33=da.sum()
            
            e0,rx,ry,error=funtSolve(n,mx,my,d11,d22,d12,d13,d23,d33)
            if error==1:
                raise Error
        '''траливали - недописано'''
        
    
    
        
    def critPoint(self, e, rx,ry):
        lstCritPoint=[]
        for i in self.lstForm:
            lstCritPoint+=i.critPoint(e,rx,ry)
        self.lstCritPoint=lstCritPoint
        return lstCritPoint

    
if __name__ == "__main__":
    lstForm=[['Rectangle',[[1.,1.],[3.,3.]],[100.,100.],0,1,[0,0,0]]]
    
    sol=Solves()
    sol.loadForm(lstForm)
#    print sol.formLst[0].a()  
#    print sol.elemMatr
#    print sol.elemMatr.shape[1]
#    print sol.centerMass()
    conc=rcMaterial.Concrete()
    conc.norme=52
    conc.b=25
    conc.initProperties()
#    
#    reinf=rcMaterial.Reinforced()
#    reinf.rn=400
#    reinf.typ='A'
#    reinf.initProperties()
    lstMat=[conc]

    sol.loadMat(lstMat, typLst=False, lst=None, typDia=2, typPS=1, typTime='short', typR=3, typRT=3)
    
    for i in range(100):
    
        e0rxry=[-0.0025,0,0]
    #    
        sol.e0rxry2nmxmy(e0rxry)
#        
#    
#def interpol(x):
#    lstx=[1,2,3,4,5,6]
#    lsty=[1,2,3,4,5,6]
#    for i in range(len(lstx)-1):
#        if lstx[i]>=x and lstx[i+1]<=x:
#            y=(lsty[i]-lsty[i+1])/(lstx[i]-lstx[i+1])+lsty[i+1]
#            return y
#for i in range(100*100*100):
#    interpol(3.5)
print 'ok'