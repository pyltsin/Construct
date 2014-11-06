# -*- coding: utf-8 -*-
"""
Created on Fri Sep 19 23:19:35 2014

@author: Pyltsin
"""
#from timeit import Timer
import numpy as np
import time
import gc
from scipy import interpolate
#пусть материалы есть в виде функций и есть матрица материалов, 
"""v=ones(numberElements)
e=e
x
y
a

da=a*v*e

dsx=da*x
dsy=da*y

djx=dsx*x
djy=dsy*y

djxy=dsx*y

d11=djx.sum()
d22=djy.sum()
d12=djxy.sum()
d13=dsx.sum()
d23=dsy.sum()
d33=da.sum()



"""
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
    
def e0rxry2nmxmy(e0,rx,ry, formMatr, matFunE2Sigma):
#   создаем матрицу e по всем точкам:
    one=np.ones(formMatr.shape[1])
    e=one*e0+formMatr[0]*rx+formMatr[1]*ry
    sigma=matFunE2Sigma(e, formMatr[3])
    n=sigma*formMatr[2]
    mx=sigma*formMatr[2]*formMatr[0]
    my=sigma*formMatr[2]*formMatr[1]
    nSum=n.sum()
    mxSum=mx.sum()
    mySum=my.sum()
    return nSum, mxSum, mySum
    
def formGen(lst, cx, cy):
    matr=np.array([[0],[0],[0],[1]])
    for i in lst:
        if i[0]=='rectangle':
            matr=np.concatenate((matr,functionRectanglesNP(i[1],i[2],i[3]-cx,i[4]-cy,i[5],i[6],i[7]) ),axis=1)
        elif i[0]=='solidcircle':
            matr=np.concatenate((matr,functionMeshSolidCirclesNP(i[1],i[3]-cx,i[5],i[4]-cy,i[5],i[7]) ),axis=1)
        elif i[0]=='circle':
            matr=np.concatenate((matr,functionCirclesNP(i[1],i[3]-cx,i[5],i[4]-cy,i[5],i[7]) ),axis=1)
    return matr
    
def centerMass(lst):
    '''Состав lstForm:
        ['rectangle/solidcircle/circle',h,b,dx,dy, nx, ny, nummat, typmat]'''
    a=0
    sx=0
    sy=0
    for i in lst:
        if i[0]=='rectangle':
            a+=i[1]*i[2]
            sx+=a*(i[3]-i[2]/2)
            sy+=a*(i[4]-i[1]/2)
        elif [0]=='solidcircle':
            a+=(i[1]/2.)**2*3.14
            sx+=a*(i[3]-i[1]/2)
            sy+=a*(i[4]-i[1]/2)
    x=sx/a
    y=sy/a
    return x,y

    
def reinforcedPropertiesSP52(a):
    pass

def reinforcedPropertiesSP63(a):
    pass

def concretePropertiesSP(a):
    pass

def functDiaConcrete(lst, typDia, typPS, typFun):
    if typDia==1:
        x=lst[0]
        y=lst[1]
    elif typDia==2:
        rsn,rs,rsw, es, es0, es2=lst
        if typPS==1:
            r=rs
        else:
            r=rsn
        x=[-es2,-es0,0,es0,es2]
        y=[-r,-r,0,r,r]

    x=np.array(x)

    y=np.array(y)        

    
    if typFun=='sigma':
        fun=interpolate.interp1d(x,y, kind='linear')
    elif typFun=='v':
        v=y/x/eb
        fun=interpolate.interp1d(x,v, kind='linear')
    return fun
        

def functDiaConcrete(lst, typDia, typPS, typTime, typR, typRT, typFun):
    '''Отдача функции расчета sigma по e или v по e'''
    if typDia==1:
        x=lst[0]
        y=lst[1]
    if typDia==2 or typDia==3:
        rbn,rb,rbtn,rbt,eb, eb0, eb2, eb1red, ebt0, ebt2, ebt1red, ebl0, ebl2, ebl1red, eblt0, eblt2, eblt1red, phi_crc=lst
        if typPS==1:
            r=rb
            rt=rbt
        elif typPS==2:
            r=rbn
            rt=rbtn
        if typTime=='short':

            e0=eb0
            et0=ebt0

            e2=eb2
            et2=ebt2

            e1red=eb1red
            et1red=ebt1red
        elif typTime=='long':

            r=r*0.9
            rt=rt*0.9
            

            e0=ebl0
            et0=eblt0

            e2=ebl2
            et2=eblt2

            e1red=ebl1red
            et1red=eblt1red

        
        if typDia==2:
            x=[-e2,-e1red,0,et1red,et2]
            y=[-r,-r,0,r,r]
        elif typDia==3:
            x=[-e2,-e0,-0.6*r/eb,0,0.6*rt/eb,et0,et2]
            y=[-r,-r,-0.6*r,0,0.6*r,r,r]

    if typR==True:
        n=0
        for i in x:
           if i<0:
               y[n]=0
           n+=1
    else:
        x.insert(0,x[0]*1.001)
        y.insert(0,0)
           
    if typRT==True:
        n=0
        for i in x:
           if i>0:
               y[n]=0
           n+=1
    else:
        x.append(x[0]*1.001)
        y.append(0)
    
    x.append(x[-1]*1000000.)
    y.append(y[-1])

    x.insert(0,x[0]*1000000.)
    y.insert(0,y[0])

    
    x=np.array(x)
    y=np.array(y)        

    
    if typFun=='sigma':
        fun=interpolate.interp1d(x,y, kind='linear')
    elif typFun=='v':
        v=y/x/eb
        fun=interpolate.interp1d(x,v, kind='linear')
    return fun
        
    
            
        
def reinforcedPropertiesApproxSP(a, ys):
    '''аппроксимирующие функции определния характеристик бетона с A240'''
    rsn=a*100/9.81
    rs=rsn/ys
    es=2.1*10**6
    if a>=600:
        es0=rs/es+0.002
        es2=0.015
    else:
        es0=rs/es
        es2=0.025
        
    rsw=rs*0.8
    if rsw>=300*100/9.81:
        rsw=300*100/9.81
    
    return rsn,rs,rsw, es, es0, es2

    

def concretePropertiesApproxSP(b, phi):
    '''аппроксимирующие функции определния характеристик бетона с В10'''
    if b>=70:
        ybb=1/(360-b)*300
    else:
        ybb=1
    yb1=1.3*ybb
    ybt1=1.5*ybb

    rbn=max(b*(0.765-0.001*b),0.71*b)
    rb=rbn/yb1
    
#    rbtn=0.232*b**(2./3)*0.776
    rbtn=0.232*(rbn)**(2./3)*0.956*1.01
    rbt=rbtn/ybt1
    
    eb=55000*b/(19.+b/0.9)/1000*1.03
    
    eb0=0.002
    ebt0=0.0001
    
    if b<=60:
        eb2=0.0035
    else:
        eb2=(0.0033-0.0028)/(70-100)*(b-100)+0.0028
    
    eb1red=0.0015
    
    ebt2=0.00015
    ebt1red=0.00008
    
    if phi>75:
        ebl0=3
        ebl2=4.2
        ebl1red=2.4
        
        eblt0=0.21
        eblt2=0.27
        eblt1red=0.19
    elif phi<=75 and phi>=40:
        ebl0=3.4
        ebl2=4.8
        ebl1red=2.8
        
        eblt0=0.24
        eblt2=0.31
        eblt1red=0.22
    else:
        ebl0=4
        ebl2=5.6
        ebl1red=3.4
        
        eblt0=0.28
        eblt2=0.36
        eblt1red=0.26

    ebl0/=1000.
    ebl2/=1000.
    ebl1red/=1000.
    
    eblt0/=1000.
    eblt2/=1000.
    eblt1red/=1000.
    
    linMatrB=np.array([10,15,20,25,30,35,40,45,50,55,60])
    linMatr75=np.array([2.8,2.4,2.,1.8,1.6,1.5,1.4,1.3,1.2,1.1,1.])    
    linMatr4075=np.array([3.9,3.4,2.8,2.5,2.3,2.1,1.9,1.8,1.6,1.5,1.4])    
    linMatr40=np.array([5.6,4.8,4.0,3.6,3.2,3.,2.8,2.6,2.4,2.2,2.])   
    funPhi75=interpolate.interp1d(linMatrB,linMatr75, kind='linear')
    funPhi4075=interpolate.interp1d(linMatrB,linMatr4075, kind='linear')
    funPhi40=interpolate.interp1d(linMatrB,linMatr40, kind='linear')
    
    if b>60:
        if phi>75:
            phi_crc=1.
        elif phi<=75 and phi>=40:
            phi_crc=1.4
        else:
            phi_crc=2.0
    else:
        if phi>75:
            phi_crc=funPhi75(b)
        elif phi<=75 and phi>=40:
            phi_crc=funPhi4075(b)
        else:
            phi_crc=funPhi40(b)
            
    rbn*=(100./9.81)
    rb*=(100./9.81)
    rbtn*=(100./9.81)
    rbt*=(100./9.81)
    eb*=10000.
    
    return rbn,rb,rbtn,rbt,eb, eb0, eb2, eb1red, ebt0, ebt2, ebt1red, ebl0, ebl2, ebl1red, eblt0, eblt2, eblt1red, phi_crc
        
   

def functionRectanglesNP(h,b,x,y,nx,ny, mat):
#    gc.collect()

    db=b/nx
    dh=h/ny
    a=db*dh
#    jx0=a*db*db/12.
#    jy0=a*dh*dh/12.
#    dx=db/2.
#    dy=dh/2.

    xone=np.ones(ny)
    xmatr= np.arange(nx)
    xmatr=np.meshgrid(xmatr,xone)
    xmatr=xmatr[0].flatten()


    xmatr*=db
    xmatr+=(-x-db/2)

    yone=np.ones(nx)
    ymatr= np.arange(ny)
    ymatr=np.meshgrid(ymatr,yone)
    ymatr=ymatr[0].transpose()
    ymatr=ymatr.flatten()
    

    ymatr*=dh
    ymatr+=(-y-dh/2)

    amatr=np.ones(nx*ny)
    amatr*=a
    
    matmatr=np.ones(nx*ny)
    matmatr*=mat

#    jx=ymatr*ymatr*amatr
#    jy=xmatr*xmatr*amatr

    
#    jx=ymatr*ymatr*amatr+jx0
#    jy=xmatr*xmatr*amatr+jy0
    
    lst=np.vstack((xmatr,ymatr,amatr, matmatr))
    
    return lst
    

def functionCirclesNP(d,x,y, mat):
    a=3.1415*(d/2.)**2
    matr=np.array([[x],[y],[a], [mat]])
    return matr


def functionMeshSolidCirclesNP(d,x,y,nx, mat):
#    gc.collect()
    lst=[]
    b=d/nx
    h=b
    r=d/2.
    a=b*h
#    jx0=a*h*h/12.
#    jy0=a*b*b/12.

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
    
    xmatr+=(r-x)
    ymatr+=(r-y)    
#    jx=ymatr*ymatr*amatr
#    jy=xmatr*xmatr*amatr

    
#    jx=ymatr*ymatr*amatr+jx0
#    jx*=rbool
#    jy=xmatr*xmatr*amatr+jy0
#    jy*=rbool

#    gc.collect()

    lst=np.vstack((xmatr,ymatr,amatr, matmatr))
    
    return lst
        
def functionTriangleNP(lstxy,nx,ny, mat):
    
    xc=((lstxy[2][0]+lstxy[1][0])/2.+lstxy[0][0])/2.
    yc=((lstxy[2][1]+lstxy[1][1])/2.+lstxy[0][1])/2.
    
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
    
    nn= np.arange(nx*ny)
    
    
    amatr=boolmatr+0.00
    
    amatr*=a
    matmatr=np.ones(nx*nx)
    matmatr*=mat

#    lst=np.vstack((xmatr,ymatr,amatr, matmatr))
##    
#    return lst
    return [xmatr,ymatr,amatr, matmatr]

if __name__ == "__main__": 

#    print range(2)
    a=functionTriangleNP([[0.,0.],[1.,0.],[0.5,1.]],1000.,1000.,1.)
    print a[2].sum()
    print (a[2]*a[1]*a[1]).sum()
    print (a[2]*a[0]*a[0]).sum()

    a=None
    gc.collect()

    a2=functionTriangleNP([[0.,0.],[1.,0.],[1,1.]],1000.,1000.,1.)
    print a2[2].sum()
    a2=None

    gc.collect()

    a3=functionTriangleNP([[0.,0.],[1.,0.],[0,1.]],1000.,1000.,1.)
    print a3[2].sum()
    a3=None

    gc.collect()

    a4=functionTriangleNP([[0.,0.],[0.,1.],[1,1.]],1000.,1000.,1.)
    print a4[2].sum()
    a4=None

    gc.collect()


                            
    print concretePropertiesApproxSP(25,1)

