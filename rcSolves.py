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
    def __init__(self):
        pass
    def loadForm(self,lstForm):
        lstFormTemp=lstForm
        
        formMatr=[]
        for i in lstFormTemp:
            if i[0]=='Rectangle' or i[0]==0:
                formMatr=append(rcMesh.Rectangles(i[1],i[2],i[3],i[4],i[5]))
            elif i[0]=='Circle' or i[0]==1:
                formMatr.append(rcMesh.Circles(i[1],i[2],i[3],i[4],i[5]))
            elif i[0]=='SolidCircle' or i[0]==2:
                formMatr.append(rcMesh.SolidCircles(i[1],i[2],i[3],i[4],i[5]))
            elif i[0]=='Triangle' or i[0]==3:
                formMatr.append(rcMesh.Triangles(i[1],i[2],i[3],i[4],i[5]))
            
        self.formMatr=formMatr
        self.formGen()
        
    def loadMat(self, lstMat, typLst, lst, typDia, typPS, typTime, typR, typRT, typFun):
        self.lstMat=lstMat
        lstFunDia=[]
        for i in lstMat:
            if i.title()=='Concrete':
                if typLst==False:
                    lstFunDia.append(i.functDia(typDia, typPS, typTime, typR, typRT, 'v'))
                else:
                    lstFunDia.append(i.functDiaLst(lst, 'v'))
            elif i.title()=='Reinforced':
                if typLst==False:
                    lstFunDia.append(i.functDia(typPS, 'v'))
                else:
                    lstFunDia.append(i.functDiaLst(lst, 'v'))
        self.lstFunDia=lstFunDia
    def loadmatFunE2Sigma(self):
        pass
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
        
    def e0rxry2nmxmy(self):
    #   создаем матрицу e по всем точкам:
        elemMatr=self.elemMatr
        one=np.ones(elemMatr.shape[1])
        e=one*elemMatr[4]+elemMatr[0]*elemMatr[5]+elemMatr[1]*elemMatr[6]
        
        sigma=matFunE2Sigma(e, formMatr[3])
        n=sigma*formMatr[2]
        mx=sigma*formMatr[2]*formMatr[0]
        my=sigma*formMatr[2]*formMatr[1]
        nSum=n.sum()
        mxSum=mx.sum()
        mySum=my.sum()
        return nSum, mxSum, mySum
    
    def formGen(self):
        '''lst - список созданных элементов!'''
        lts=self.formMatr
        matr=np.array([[0],[0],[0],[1],[0],[0],[0]])
        for i in lst:
            matr=np.concatenate((matr,lst.mesh()) ,axis=1)
        self.elemMatr=matr
    
    def centerMass(lst):
        '''lst - список элементов'''
        a=0
        sx=0
        sy=0
        for i in lst:
            a+=i.a()
            sx+=i.sx()
            sy+=i.sy()
            
        x=sx/a
        y=sy/a
        return x,y
    def critPoint(self, e, rx,ry):
        lstCritPoint=[]
        for i in self.lstForm:
            lstCritPoint+=i.critPoint(e,rx,ry)
        self.lstCritPoint=lstCritPoint
        return lstCritPoint
    
if __name__=='main':
    lstForm=[['Rectangle',[[-1,-1],[1,1]],[100,100],1,1,[0,0,0]],
             ['Circle',[1,0,-1],[1,1],1,2,[0,0,0]],
             ['Circle',[1,0,1],[1,1],1,2,[0,0,0]]]

    conc=rcMaterial.Concrete()
    conc.b=25
    conc.initProperties()
    
    reinf=rcMaterial.Reinforced()
    reinf.rn=400
    reinf.typ='A'
    reinf.initProperties()
    
    lstMat=[conc, reinf]
    
#    e0rxry=[1,1,1]
    
    sol=Solves()
    sol.loadLst(lstForm)
    sol.loadMat(lstMat, typLst=False, lst=None, typDia=2, typPS=1, typTime='short', 2, 2)
    print sol.e0rxry2nmxmy(e0rxry)
        
    
