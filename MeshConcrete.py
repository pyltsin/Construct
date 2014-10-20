# -*- coding: utf-8 -*-
"""
Created on Fri Sep 19 23:19:35 2014

@author: Pyltsin
"""
#from timeit import Timer
import numpy as np
import time
import gc
def functionMeshCells(h,b,x,y):
    a=h*b
    jx0=a*h*h/12.
    jx=jx0+a*y*y
    jy0=a*b*b/12.
    jy=jy0+a*x*x
    return [x,y, a, jx, jy]

def functionRectanglesNP(h,b,x,y,nx,ny):
#    gc.collect()

    db=b/nx
    dh=h/ny
    a=db*dh
    jx0=a*db*db/12.
    jy0=a*dh*dh/12.
    dx=db/2.-b/2.
    dy=dh/2.-h/2.

    xone=np.ones(ny)
    xmatr= np.arange(nx)
    xmatr=np.meshgrid(xmatr,xone)
    xmatr=xmatr[0].flatten()


    xmatr*=db
    xmatr+=(x+dx)

    yone=np.ones(nx)
    ymatr= np.arange(ny)
    ymatr=np.meshgrid(ymatr,yone)
    ymatr=ymatr[0].transpose()
    ymatr=ymatr.flatten()
    

    ymatr*=dh
    ymatr+=(y+dy)

    amatr=np.ones(nx*ny)
    amatr*=a
    
    jx=ymatr*ymatr*amatr+jx0
    jy=xmatr*xmatr*amatr+jy0
    
    lst=np.vstack((xmatr,ymatr,amatr, jx, jy))
    
    return lst
    
def functionRectangles(h,b,x,y, nx, ny):
    lst=[]
    db=b/nx
    dh=h/ny
    a=db*dh
    jx0=a*db*db/12.
    jy0=a*dh*dh/12.
    dx=db/2.-b/2.
    dy=dh/2.-h/2.
    for xi in xrange(nx):
        for yi in xrange(ny):
            x0=db*xi+dx
            y0=dh*yi+dy

            xCell=x+x0
            yCell=y+y0
            jx=jx0+a*yCell*yCell
            jy=jy0+a*xCell*xCell
            cell=[xCell,yCell,a,jx,jy]
            lst.append(cell)
    return lst

def functionCircles(d,x,y):
    a=3.1415*(d/2.)**2
    jx=a*y**2
    jy=a*x**2
    return [x,y,a,jx,jy]


def functionMeshSolidCirclesNP(d,x,y,nx):
#    gc.collect()
    lst=[]
    b=d/nx
    h=b
    r=d/2.
    a=b*h
    jx0=a*h*h/12.
    jy0=a*b*b/12.

    dx=b/2.-r
    dy=h/2.-r
    r2=r*r

    xone=np.ones(nx)
    xmatr= np.arange(nx)
    xmatr=np.meshgrid(xmatr,xone)
    xmatr=xmatr[0]*h+dx
    ymatr=xmatr.transpose()
    
    xmatr=xmatr.flatten()
    ymatr=ymatr.flatten()
    
    rmatr=xmatr*xmatr+ymatr*ymatr
    rbool=(rmatr<=r2)

    amatr=np.ones(nx*nx)
    amatr*=a
    amatr*=rbool
    
    jx=ymatr*ymatr*amatr+jx0
    jx*=rbool
    jy=xmatr*xmatr*amatr+jy0
    jy*=rbool

#    gc.collect()

    lst=np.vstack((xmatr,ymatr,amatr, jx, jy))
    
    return lst
        
        
def functionMeshSolidCircles(d,x,y,nx):
    lst=[]
    b=d/nx
    h=b
    r=d/2.
    a=b*h
    jx0=a*h*h/12.
    jy0=a*b*b/12.

    dx=b/2.-r
    dy=h/2.-r
    r2=r*r
    for xi in xrange(nx):
        for yi in xrange(nx):
            x0=b*xi+dx
            y0=h*yi+dy
            if x0*x0+y0*y0<=r2:
                xCell=x+x0
                yCell=y+y0
                jx=jx0+a*yCell*yCell
                jy=jy0+a*xCell*xCell
                cell=[xCell,yCell,a,jx,jy]
                lst.append(cell)
    return lst

if __name__ == "__main__":

    h=1000.
    b=1000.
    nx=2000
    ny=2000

    time_start=time.time()    

    meshLst=functionRectangles(h,b,0,0,ny,nx)

    a=0
    jx=0
    jy=0
#    print 'tut2'
    for i in meshLst:
        a+=i[2]
        jx+=i[3]
        jy+=i[4]

    time_stop1=time.time()    

#    print u'По функции'

    print a, jx, jy, time_stop1-time_start
    
#    print u'Точный расчет'

    print h*b, h**3*b/12.,b**3*h/12. 

    time_start=time.time()    
    
    meshLstNP=functionRectanglesNP(h,b,0,0,ny,nx)
    
    aNP=meshLstNP[2].sum()
    jxNP=meshLstNP[3].sum()
    jyNP=meshLstNP[4].sum()

    time_stop1=time.time()    

#    print u'NumPy'
    print aNP, jxNP, jyNP,  time_stop1-time_start



    d=2000.
    nx=1500
    time_start=time.time()    

    meshLst=functionMeshSolidCircles(d,0,0,nx)
    a=0
    jx=0
    jy=0
    print 'tut2'
    for i in meshLst:
        a+=i[2]
        jx+=i[3]
        jy+=i[4]
    time_stop1=time.time()    

    print a, jx, jy,   time_stop1-time_start
    print 3.14*(d/2.)**2, 3.1415*d** 4 / 64 

    time_start=time.time()    

    meshLstNP=functionMeshSolidCirclesNP(d,0,0,nx)
    aNP=meshLstNP[2].sum()
    jxNP=meshLstNP[3].sum()
    jyNP=meshLstNP[4].sum()
    time_stop1=time.time()    

    print aNP, jxNP, jyNP,  time_stop1-time_start
