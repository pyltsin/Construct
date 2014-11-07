# -*- coding: utf-8 -*-
"""
Created on Fri Sep 19 23:19:35 2014

@author: Pyltsin
"""
#from timeit import Timer
from table import tables_csv
import numpy as np
import time
import gc
from scipy import interpolate
import math

class Rectangles(object):
    def __init__(self,lstXY, lstN, mat=1, sign=1, e0rxry=[0,0,0]):
        self.nx=float(lstN[0])
        self.ny=float(lstN[1])
        self.mat=mat
        self.lstXY=lstXY
        self.b=abs(lstXY[1][0]-lstXY[0][0])
        self.h=abs(lstXY[1][1]-lstXY[0][1])
        self.x=lstXY[0][0]
        self.y=lstXY[0][1]
        self.sign=sign
        self.e0rxry=e0rxry
    def a(self):
        return self.b*self.h
    def sx(self):
        return self.a()*(self.x+self.b/2.)
    def sy(self):
        return self.a()*(self.y+self.h/2.)
    def critPoint(self, e,rx,ry):
        b=self.b
        h=self.h
        x=self.x
        y=self.y
        mat=self.mat
        p1=[x,y, mat]
        p2=[x+b,y+h, mat]
        p3=[x+b,y, mat]
        p4=[x,y+h, mat]
        return [p1,p2,p3,p4]
    def mesh(self):
        gc.collect()
        h,b,x,y,nx,ny, mat=self.h,self.b,self.x,self.y,self.nx,self.ny, self.mat
        sign=self.sign
        db=b/nx
        dh=h/ny
        a=db*dh    
        xone=np.ones(ny)
        xmatr= np.arange(nx)
        xmatr=np.meshgrid(xmatr,xone)
        xmatr=xmatr[0].flatten()
    
    
        xmatr*=db
        xmatr+=(x-db/2)
    
        yone=np.ones(nx)
        ymatr= np.arange(ny)
        ymatr=np.meshgrid(ymatr,yone)
        ymatr=ymatr[0].transpose()
        ymatr=ymatr.flatten()
        
    
        ymatr*=dh
        ymatr+=(y-dh/2)
    
        amatr=np.ones(nx*ny)
        amatr*=(sign*a)
    
        matmatr=np.ones(nx*ny)
        matmatr*=mat

        e0=np.ones(nx*ny)
        e0*=self.e0rxry[0]
        rx=np.ones(nx*ny)
        rx*=self.e0rxry[1]
        ry=np.ones(nx*ny)
        ry*=self.e0rxry[2]

        lst=np.vstack((xmatr,ymatr,amatr, matmatr,e0,rx,ry))
        
        return lst
    
class Circles(object):
    def __init__(self,lst,lstN, mat=1, sign=1, e0rxry=[0,0,0]):
        self.d=float(lst[0])

        self.x=float(lst[1])
        self.y=float(lst[2])
        self.mat=mat
        self.sign=sign
        self.e0rxry=e0rxry
    def a(self):
        return 3.1415*(self.d/2.)**2
    def sx(self):
        return 0
    def sy(self):
        return 0

    def mesh(self):
        a=self.a()*self.sign
        matr=np.array([[self.x],[self.y],[a], [self.mat],[self.e0rxry[0]],[self.e0rxry[1]],[self.e0rxry[2]]])
        return matr

    def critPoint(self, e,rx,ry):
        x=self.x
        y=self.y
        mat=self.mat
        p1=[x,y, mat]
        return [p1]


class SolidCircles(object):
    def __init__(self,lst,lstN, mat=1, sign=1,e0rxry=[0,0,0]):
        '''x y  - координаты центра тяжести'''
        self.d=float(lst[0])
        self.nx=lstN[0]
        self.x=float(lst[1])
        self.y=float(lst[2])
        self.mat=mat
        self.sign=sign
        self.e0rxry=e0rxry
    def a(self):
        return 3.1415*(self.d/2.)**2
    def sx(self):
        return self.a()*self.x
    def sy(self):
        return self.a()*self.y

    def mesh(self):
        d=self.d
        x=self.x
        y=self.y
        nx=self.nx
        mat=self.mat
        
        gc.collect()
        lst=[]
        b=d/nx
        h=b
        r=d/2.
        a=b*h
        dx=b/2.-r
        r2=r*r
    
        xone=np.ones(nx)
        xmatr= np.arange(nx)
        xmatr=np.meshgrid(xmatr,xone)
        xmatr=xmatr[0]*h+dx
        ymatr=xmatr.transpose()
        
        xmatr=xmatr.flatten()
        ymatr=ymatr.flatten()
        
        rmatr=np.square(xmatr)+np.square(ymatr)
        rbool=(rmatr<=r2)
    
        amatr=rbool
        amatr*=a
    
        matmatr=np.ones(nx*nx)
        matmatr*=mat
        
        xmatr+=(-r+x)
        ymatr+=(-r+y)    

        e0=np.ones(nx*ny)
        e0*=self.e0rxry[0]
        rx=np.ones(nx*ny)
        rx*=self.e0rxry[1]
        ry=np.ones(nx*ny)
        ry*=self.e0rxry[2]

    
        lst=np.vstack((xmatr,ymatr,amatr, matmatr,e0,rx,ry))
        
        return lst

    def critPoint(self, e,rx,ry):
        d=self.d
        x0=rx/(rx**2+ry**2)**0.5*d/2.
        y0=ry/(rx**2+ry**2)**0.5*d/2.
            
        x=self.x
        y=self.y
        mat=self.mat
        p1=[x+x0,y+y0, mat]
        p2=[x-x0,y-y0, mat]

        return [p1,p2]


class Triangles(object):
    def __init__(self,lstXY, lstN, mat=1, sign=1,e0rxry=[0,0,0]):
        self.nx=float(lstN[0])
        self.ny=float(lstN[1])
        self.mat=mat
        self.lstXY=lstXY
        self.sign=sign
        self.e0rxry=e0rxry
    def a(self):
        x1=self.lstXY[0][0]
        y1=self.lstXY[0][1]
    
        x2=self.lstXY[1][0]
        y2=self.lstXY[1][1]
    
        x3=self.lstXY[2][0]
        y3=self.lstXY[2][1]

        a=1./2.*abs((x1-x3)*(y2-y3)-(x2-x3)*(y1-y3))
        
        return a
    def sx(self):
        return self.a()*(self.xcyc()[0])**2

    def sy(self):
        return self.a()*(self.xcyc()[1])**2

    def critPoint(self, e,rx,ry):
        x1=self.lstXY[0][0]
        y1=self.lstXY[0][1]
    
        x2=self.lstXY[1][0]
        y2=self.lstXY[1][1]
    
        x3=self.lstXY[2][0]
        y3=self.lstXY[2][1]
        
        mat=self.mat
        p1=[x1,y1, mat]
        p2=[x2,y2, mat]
        p3=[x3,y3, mat]
        return [p1,p2,p3]
        
    def xcyc(self):
        x1=self.lstXY[0][0]
        y1=self.lstXY[0][1]
    
        x2=self.lstXY[1][0]
        y2=self.lstXY[1][1]
    
        x3=self.lstXY[2][0]
        y3=self.lstXY[2][1]

    
        xc=(x1+x2+x3)/3.
        yc=(y1+y2+y3)/3.
        
        return xc, yc
        
    def mesh(self):
        lstxy,nx,ny, mat, sign=self.lstXY,self.nx,self.ny, self.mat, self.sign
        xc=self.xcyc()[0]
        yc=self.xcyc()[1]
        
        kmatr=[]
        bmatr=[]
        for i in range(3):
            if (lstxy[i-1][0]-lstxy[i][0])!=0:
                kmatr.append((lstxy[i-1][1]-lstxy[i][1])/(lstxy[i-1][0]-lstxy[i][0]))
                bmatr.append(lstxy[i-1][1]-lstxy[i-1][0]*kmatr[i])
            else:
                kmatr.append(None)
                bmatr.append(lstxy[i-1][0])
    
        kkmatr=[]
        for i in range(3):
            if kmatr[i]!=None:
                if yc>=kmatr[i]*xc+bmatr[i]:
                    kkmatr.append(1)
                else:
                    kkmatr.append(0)
            else:
                if xc>bmatr[i]:
                    kkmatr.append(1)
                else:
                    kkmatr.append(0)
                    
        b=max(abs(lstxy[2][0]-lstxy[1][0]),abs(lstxy[2][0]-lstxy[0][0]),abs(lstxy[1][0]-lstxy[0][0]))
        h=max(abs(lstxy[2][1]-lstxy[1][1]),abs(lstxy[2][1]-lstxy[0][1]),abs(lstxy[1][1]-lstxy[0][1]))
    
        db=b/nx
        dh=h/ny
    
        dx=db/2.
        dy=dh/2.
        a=db*dh
        
#        xmatr=[i for i in range(int(nx))]
#        xmatr=np.concatenate((xmatr*int(ny-1), xmatr))
##        print xmatr
        xone=np.ones(ny)
        xmatr= np.arange(nx)
        
        xmatr=np.meshgrid(xmatr,xone)
        xmatr=xmatr[0].flatten()
    
    
        xmatr*=db
        xmatr+=(dx)
    
        yone=np.ones(nx)
        ymatr= np.arange(ny)
        ymatr=np.meshgrid(ymatr,yone)
        ymatr=ymatr[0].transpose()
        ymatr=ymatr.flatten()
        
    
        ymatr*=dh
        ymatr+=(dy)
    
        bol=[[],[],[]]
        
        for i in range(3):
            if kmatr[i]!=None:
                if kkmatr[i]==1:
                    bol[i]=(ymatr>=kmatr[i]*xmatr+bmatr[i])
                else:
                    bol[i]=(ymatr<kmatr[i]*xmatr+bmatr[i])
            else:
                if kkmatr[i]==1:            
                    bol[i]=(xmatr>=bmatr[i])
                else:
                    bol[i]=(xmatr<bmatr[i])
                
        boolmatr=bol[0] * bol[1]
        
        boolmatr=boolmatr * bol[2]
        
        amatr=boolmatr+0.00
        
        amatr*=(sign*a)
        matmatr=np.ones(nx*nx)
        matmatr*=mat

        e0=np.ones(nx*ny)
        e0*=self.e0rxry[0]
        rx=np.ones(nx*ny)
        rx*=self.e0rxry[1]
        ry=np.ones(nx*ny)
        ry*=self.e0rxry[2]

    
#        lst=np.vstack((xmatr,ymatr,amatr, matmatr))

        return [xmatr,ymatr,amatr, matmatr,e0,rx,ry]

    
if __name__ == "__main__": 

    rc=Rectangles([[-1,-1],[1,1]],[3000,3000],1,1)
    rcmesh=rc.mesh()
    print rcmesh[2].sum()
    print (rcmesh[2]*rcmesh[0]*rcmesh[0]).sum()
    rcmesh=None
    gc.collect()

    start=time.time()
    for i in range(10000):
        a=Triangles([[0.,0.],[1.,0.],[0.5,1.]],[100,100],1,1)
        amesh=a.mesh()
#        print amesh[2].sum()
#        print (amesh[2]*amesh[1]*amesh[1]).sum()
#        print (amesh[2]*amesh[0]*amesh[0]).sum()
    
#        amesh=None
#        gc.collect()
    print  time.time()-start    

