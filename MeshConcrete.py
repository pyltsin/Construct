# -*- coding: utf-8 -*-
"""
Created on Fri Sep 19 23:19:35 2014

@author: Pyltsin
"""

#import numpy as np

def functionMeshCells(h,b,x,y):
    a=h*b
    jx0=a*h*h/12.
    jx=jx0+a*y*y
    jy0=a*b*b/12.
    jy=jy0+a*x*x
    return [x,y, a, jx, jy]


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

class Circles():
    def __init__(self, d, x, y):
        self.__d=d
        self.__x=x
        self.__y=y
    def mesh(self):
        a=3.1415*(self.__d/2.)**2
        jx=a*self.__y**2
        jy=a*self.__x**2
        return [self.__x,self.__y, a, jx, jy]

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
    d=2000.
    nx=2000
    meshLst=functionMeshSolidCircles(d,0,0,nx)
    a=0
    jx=0
    jy=0
    print 'tut2'
    for i in meshLst:
        a+=i[2]
        jx+=i[3]
        jy+=i[4]
    print a, jx, jy
    print 3.14*(d/2.)**2, 3.1415*d** 4 / 64 
