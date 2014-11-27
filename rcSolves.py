# -*- coding: utf-8 -*-
"""
Created on Fri Nov 07 23:42:52 2014

@author: Pyltsin
"""
import numpy as np
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
        Создает self.formLst - список созданных материалов!
        Проверено, тесты не сделаны'''
                
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
        '''возвращает координаты центра массы - проверено, тесты не сделаны'''
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
        '''Создает матрицу элементов
        type0 - флаг если начальные искривления
        Проверено, тесты не сделаны'''
        lst=self.formLst
        matr=False
        first=False
        for i in lst:
            if first==False:
                matr=np.array(i.mesh())
                first=True
            else:
                matr=np.concatenate((matr,i.mesh()) ,axis=1)
            
        self.elemMatr=matr
        x,y=self.centerMass()
        self.elemMatr[0]-=x
        self.elemMatr[1]-=y
#        print 'elemMatr', self.elemMatr

        e0=(matr[-3]!=0).astype(float)
        rx=(matr[-2]!=0).astype(float)
        ry=(matr[-1]!=0).astype(float)
        
        e0sum=e0.sum()
        rxsum=rx.sum()
        rysum=ry.sum()
        
        if e0sum<10**(-10) and rxsum<10**(-10) and rysum<10**(-10):
            self.type0=False
        else:
            self.type0=True
        
        self.jx=(matr[3]*matr[0]*matr[0]).sum
        self.jy=(matr[3]*matr[1]*matr[1]).sum
        
        
    def e0rxry2e(self,e0=0,rx=0,ry=0):
        '''создаем матрицу e
        проверено - тестов нет'''
        elemMatr=self.elemMatr #копируем матрицу, чтобы не испортить старую
        one=np.ones(elemMatr.shape[1]) #создаем матрицу 1 длиной с количества точек e
        
        e=one*(elemMatr[4]+e0)+elemMatr[0]*(elemMatr[5]+rx)+elemMatr[1]*(elemMatr[6]+ry) #e=e+rx*x+ry*y
        return e
    
    def e2d(self, ee):
        ''''возвращаем d от e - матрицы списка перемещений'''
        ev=self.e2ev4(ee) #вернули матрицу e*v
        d33=self.elemMatr[2]*ev
        d13=d33*self.elemMatr[0]
        d23=d33*self.elemMatr[1]
        d11=d13*self.elemMatr[0]
        d22=d23*self.elemMatr[1]
        d12=d13*self.elemMatr[1]
        
        d33Sum=d33.sum()
        d13Sum=d13.sum()
        d23Sum=d23.sum()
        d11Sum=d11.sum()
        d22Sum=d22.sum()
        d12Sum=d12.sum()
        
        return [d11Sum,d12Sum,d13Sum,d22Sum,d23Sum,d33Sum],[d11,d12,d13,d22,d23,d33]

#    def e2sigma(self, e):
#        '''возвращает матрицу sigma от e'''     
#        return np.transpose(self.ufunE2sigma()(e, self.elemMatr[3])[0])
#
#
#    def funE2sigma(self, e, numMat):
#        '''просто фнкция для определения e2sigma от номера материала - для перевода ее в uFun'''
##        print 'fun', self.lstFunE2ev[int(numMat)][0](e),self.lstFunE2ev[int(numMat)][1](e)
#        return self.lstFunE2ev[int(numMat)][0](e)
#
#    def ufunE2sigma(self):
#        '''возвращает функцию funE2ev для массивов'''
#        return np.frompyfunc(self.funE2sigma,2,2)
#
#
#
#    '''Интерполяция 2 через функцию материала'''
#    def e2sigma2(self, e):
#        '''возвращает матрицу sigma от e'''     
##        print self.ufunE2sigma2()(e, self.elemMatr[3])
#        return self.ufunE2sigma2()(e, self.elemMatr[3])
#
#
#    def funE2sigma2(self, e, numMat):
#        '''просто фнкция для определения e2sigma от номера материала - для перевода ее в uFun'''
##        print 'e',e
##        print 'fun2', self.lstFunE2ev2[0](e)
##        print 'fun', self.lstFunE2ev2[int(numMat)](e)
#        return self.lstFunE2ev2[int(numMat)](e)[0]
#
#    def ufunE2sigma2(self):
#        '''возвращает функцию funE2ev для массивов'''
#        return np.frompyfunc(self.funE2sigma2,2,1)
#
    '''Версия 4 интерполяции - через функцию здесь'''
    def e2sigma4(self, e):
        '''e - матрица e
        проверено - тестов нет'''

        xmatr=self.xmatr.copy()
        ymatr=self.ymatr.copy()
        kymatr=self.kymatr.copy()

#        print e.shape
#        print xmatr.shape
#        print self.elemMatr
        
        boolmatr=(e>xmatr)
#        print boolmatr
#        print e
#        print xmatr
        one=np.zeros(boolmatr.shape[1])
        
        boolmatrInvert=np.vstack((boolmatr[1:],one))
        boolmatrInvert=(boolmatrInvert==False)
        boolmatr=(boolmatr==boolmatrInvert)
        
#        xmatr*=boolmatr
#        xmatr=np.sum(xmatr, axis=0)
        
        ymatr*=boolmatr
        ymatr=np.sum(ymatr, axis=0)
        
        kymatr*=boolmatr[:-1]
        kymatr=np.sum(kymatr, axis=0)
        
        xmatr*=boolmatr
        xmatr=np.sum(xmatr, axis=0)
        sigma=kymatr*(e-xmatr)+ymatr
#        print sigma

        return sigma
        
    def e2ev4(self, e):
        '''e - матрица e'''
        ebool=(e==0)
        ebool=ebool.astype(float)
        de=self.dxmatr*ebool
        
        eTotal=e+de 
        sigma=self.e2sigma4(eTotal)
        ev=sigma/eTotal
        return ev
        


    


    def e0rxry2nmxmy(self,e0rxry):
        '''возвращает значение усилий по дополнительным деформациям
        проверено - тестов нет'''
        e0,rx,ry=e0rxry
        e=self.e0rxry2e(e0,rx,ry) #получили e1
#        print self.e2sigma2(e),'sigma' 
        sigma=self.e2sigma4(e)
        n=sigma*self.elemMatr[2]
        mx=sigma*self.elemMatr[2]*self.elemMatr[0]
        my=sigma*self.elemMatr[2]*self.elemMatr[1]
        nSum=n.sum()
        mxSum=mx.sum()
        mySum=my.sum()
        return nSum, mxSum, mySum, sigma, e
        
        
    def matrSolve(self, nmxmy, dd):
        '''расчет матрицы'''
        n, m_x, m_y=nmxmy
        d_11,d_12,d_13,d_22,d_23,d_33=dd
        if d_11*(d_22*d_33-d_23**2)-d_12*(d_12*d_33-d_13*d_23)+d_13*(d_12*d_23-d_13*d_22)!=0:
            rx=(d_12*(d_33*m_y-d_23*n)+d_13*(d_22*n-d_23*m_y)+(d_23**2-d_22*d_33)*m_x)/(d_11*(d_23**2-d_22*d_33)+d_12**2*d_33-2*d_12*d_13*d_23+d_13**2*d_22)
            ry=-(d_11*(d_33*m_y-d_23*n)+d_12*d_13*n-d_13**2*m_y+(d_13*d_23-d_12*d_33)*m_x)/(d_11*(d_23**2-d_22*d_33)+d_12**2*d_33-2*d_12*d_13*d_23+d_13**2*d_22)
            e0=(d_11*(d_23*m_y-d_22*n)+d_12**2*n-d_12*d_13*m_y+(d_13*d_22-d_12*d_23)*m_x)/(d_11*(d_23**2-d_22*d_33)+d_12**2*d_33-2*d_12*d_13*d_23+d_13**2*d_22)
            error=0
        else:
            e0 = 0
            rx= 0
            ry = 0
            error = 1
        return [e0,rx,ry,error]

    def nmxmy2e0rxry(self,nmxmy, nn, crit):
        '''определение e0rxry, nn - макс кол-во итераций, criter - критерий сходимости
        type0 - учет начального искривления  False - нет искривлени - считается автоматом
        Возвращает список: e0f, rxf, ryf, tol
        При ошибке tol==string'''
        elemMatr=self.elemMatr.copy()
        
        type0=self.type0
                 
        e0,rx,ry=0,0,0
        if type0==True:
            dn, dmx, dmy=self.e0rxry2nmxmy([e0,rx,ry])[0:3]
            nmxmy=[nmxmy[0]+dn,nmxmy[1]+dmx,nmxmy[2]+dmy]
        n=0
        while True:
            ee=self.e0rxry2e(e0,rx,ry)
#            print 'ee',ee[0:10]
            dd=self.e2d(ee)
            
            if type0==True:
                d11,d12,d13,d22,d23,d33= dd[1]           
                dnTemp=d33*elemMatr[-3]+d13*elemMatr[-2]+d23*elemMatr[-1]
                dnSum=dnTemp.sum()
                
                
                dmxTemp=d13*elemMatr[-3]+d11*elemMatr[-2]+d12*elemMatr[-1]
                dmxSum=dmxTemp.sum()
    
    
                dmyTemp=d23*elemMatr[-3]+d12*elemMatr[-2]+d22*elemMatr[-1]
                dmySum=dmyTemp.sum()
    
                nmxmyTemp=[nmxmy[0]-dnSum,nmxmy[1]-dmxSum,nmxmy[2]-dmySum]
            else:
                nmxmyTemp=nmxmy
            e0f,rxf,ryf,error=self.matrSolve(nmxmyTemp,dd[0])
#            print '1f',e0, rx, ry
#            print 'f',e0f, rxf, ryf, error
#            print 'n',nmxmyTemp
#            print 'dd',dd[0]
            if error==1:
                return [False, False, False, 'Matr',n, []]
            else:
                if e0f<10**(-20):
                    tolE=abs(e0f-e0)
                else:
                    tolE=abs((e0f-e0)/e0f)

                if rxf<10**(-20):
                    tolRx=abs(rxf-rx)
                else:
                    tolRx=abs((rxf-rx)/rxf)

                if ryf<10**(-20):
                    tolRy=abs(ryf-ry)
                else:
                    tolRy=abs((ryf-ry)/ryf)

                    
                tol=max(tolE, tolRx, tolRy)

                if tol<crit:
                    return [e0f, rxf, ryf, tol, n, dd[0]]
                
                if n>nn:
                    return [False, False, False, 'Nmax',n,[]]
                
                e0, rx,ry=e0f, rxf, ryf  
                n+=1
                
        
    
    def loadMat(self, lstMat):
        '''загружаем материалы и создаем список функций
        в принципе правильно - без тестов''' 

        self.lstMat=lstMat

        ''' записываем в lst все массивы'''  
        maxx=0
        lstx=[]
        lsty=[]
        lstky=[]
        lstyEv=[]
        lstkyEv=[]
        lstdx=[]
        
        for i in lstMat:
            if len(i.x)>maxx:
                maxx=len(i.x)

            lstx.append(i.x)
            lsty.append(i.y)
            lstky.append(i.ky)
            lstyEv.append(i.yEv)
            lstkyEv.append(i.kyEv)
            lstdx.append(i.dx) 
                   
        '''приводим все к одному значению'''
        for j in range(len(lstx)):
            if len(lstx[j])<maxx:
                for i in range(maxx-len(lstx[j])):
                    lstx[j]=np.append(lstx[j], lstx[j][-1])
                    lsty[j]=np.append(lsty[j], lsty[j][-1])
                    lstky[j]=np.append(lstky[j], lstky[j][-1])
                    lstyEv[j]=np.append(lstyEv[j], lstyEv[j][-1])
                    lstkyEv[j]=np.append(lstkyEv[j], lstkyEv[j][-1])

        '''теперь создаем матрицу соответствующую № массива'''
        
        xmatr=None
        
        ymatr=None
        kymatr=None

        yEvmatr=None
        kyEvmatr=None
        
        dxmatr=None
        
        for i in self.formLst:
            ln=i.ln()
            xone=np.ones(ln)
            
            xmatrTemp= np.array(lstx[i.mat])
            xmatrTemp=np.meshgrid(xmatrTemp,xone)
            xmatrTemp=xmatrTemp[0]
            xmatrTemp=xmatrTemp.transpose()

            dxmatrTemp= np.array(lstdx[i.mat])
            dxmatrTemp=np.meshgrid(dxmatrTemp,xone)
            dxmatrTemp=dxmatrTemp[0]
            dxmatrTemp=dxmatrTemp.transpose()


            ymatrTemp= np.array(lsty[i.mat])
            ymatrTemp=np.meshgrid(ymatrTemp,xone)
            ymatrTemp=ymatrTemp[0]
            ymatrTemp=ymatrTemp.transpose()
            
            kymatrTemp= np.array(lstky[i.mat])
            kymatrTemp=np.meshgrid(kymatrTemp,xone)
            kymatrTemp=kymatrTemp[0]
            kymatrTemp=kymatrTemp.transpose()
            
            yEvmatrTemp= np.array(lstyEv[i.mat])
            yEvmatrTemp=np.meshgrid(yEvmatrTemp,xone)
            yEvmatrTemp=yEvmatrTemp[0]
            yEvmatrTemp=yEvmatrTemp.transpose()
            
            kyEvmatrTemp= np.array(lstkyEv[i.mat])
            kyEvmatrTemp=np.meshgrid(kyEvmatrTemp,xone)
            kyEvmatrTemp=kyEvmatrTemp[0]
            kyEvmatrTemp=kyEvmatrTemp.transpose()
            
            if xmatr==None:
                xmatr=xmatrTemp
                dxmatr=dxmatrTemp
 
                ymatr=ymatrTemp
                kymatr=kymatrTemp
                yEvmatr=yEvmatrTemp
                kyEvmatr=kyEvmatrTemp

            else:
                xmatr=np.hstack((xmatr,xmatrTemp))
                dxmatr=np.hstack((dxmatr,dxmatrTemp))   
#                print ymatr, ymatrTemp
                ymatr=np.hstack((ymatr,ymatrTemp))
                kymatr=np.hstack((kymatr,kymatrTemp))
                yEvmatr=np.hstack((yEvmatr,yEvmatrTemp))
                kyEvmatr=np.hstack((kyEvmatr,kyEvmatrTemp))

        self.xmatr=xmatr
        self.ymatr=ymatr
        self.kymatr=kymatr
        self.yEvmatr=yEvmatr
        self.kyEvmatr=kyEvmatr
#        print self.xmatr
        self.dxmatr=np.array(dxmatr)                
        
    def critPoint(self, e0, rx,ry):
        lstCritPoint=[]
        for i in self.lstForm:
            lstCritPoint.append(i.critPoint(e0,rx,ry))
        self.lstCritPoint=lstCritPoint

        x,y=self.centerMass()

        
        for i in self.lstCritPoint:
            i[0]-=x
            i[1]-=y
        return lstCritPoint
    
    def findKult(self, nmxmy, nn, crit ):
        '''Находим коэффициент к'''
        
#        определим начальный nmxmy
        n,mx,my=nmxmy
        lenN=(n**2+mx**2+my**2)**.5        

        e0,rx,ry=0,0,0
        ee=self.e0rxry2e(e0,rx,ry)

        dd=self.e2d(ee)

        e0rxry=self.matrSolve(nmxmy,dd[0])

        
        k1=self.kk(e0rxry[0:3])
        if k1==0:
            return 'error'
        e0rxryTemp=[e0rxry[0]/k1, e0rxry[1]/k1, e0rxry[2]/k1]
        n=0
        while True:
            n+=1
            if n>nn:
                return 'error'
            nmxmyTemp=self.e0rxry2nmxmy(e0rxryTemp)
            nTemp,mxTemp,myTemp=nmxmyTemp            
            cosa=(n*nTemp+mx*mxTemp+my*myTemp)/((n**2+mx**2+my**2)**0.5*(nTemp**2+mxTemp**2+myTemp**2)**0.5)
            lenNTemp=(nTemp**2+mxTemp**2+myTemp**2)**.5   
            lenNNormal=lenNTemp*cosa
            kLen=lenNNormal/lenN
            
            nmxmyNormal=[n*kLen, mx*kLen, my*kLen]
            e0rxryTemp=self.nmxmy2e0rxry(nmxmyNormal,nn, crit)
            k1=self.kk(e0rxry[0:3])
            if k1==0:
                return 'error'
            
            e0rxryTemp=[e0rxry[0]/k1, e0rxry[1]/k1, e0rxry[2]/k1]
            
            if abs(k1-1)<nn:
                return k1, e0rxryTemp, n
            


    def kk(self,e0rxry):
        '''определяем коэффициент исопльзования по всем нормам 
        - самое простое - переслать в материалы список emax и emin
        1. сначала вычисляем  расположение критических точек'''
        e0, rx,ry=e0rxry
        lstCritPoint=self.critPoint(e0, rx,ry)      
        '''ищем максимальное число материалов'''
        nMat=self.lstMat.len()
        nlst=[]
        for i in range(nMat):
            nlst.append([False, False])

        '''вычисляем e для всех критических точек'''
                    
        for i in lstCritPoint:
            x,y,mat,e0t,rxt,ryt=i
            e= e0t+x*rxt+y*ryt
            if nlst[mat][0]==False:
                nlst[mat][0]=e
            else:
                if nlst[mat][0]>e:
                    nlst[mat][0]=e

            if nlst[mat][1]==False:
                nlst[mat][1]=e
            else:
                if nlst[mat][1]<e:
                    nlst[mat][1]=e
        
        '''вычисляем k для каждого материала'''
        kk=[]
        for i in range(nMat):
            kk.append(self.lstMat.kk(nlst[i]))
        
        k=kk.max()
            
            
                        
            
        return k

    
if __name__ == "__main__":
    lstForm=[
    ['Rectangle',[[0.,0.],[50.,50.]],[30.,30.],0,1,[0,0,0]],
    ['Circle',[5,5,2],[],1,1,[0,0,0]],
    ['Circle',[45,45,2],[],1,1,[0,0,0]],
    ['Circle',[45,5,2],[],1,1,[0,0,0]],
    ['Circle',[5,45,2],[],1,1,[0,0,0]]
    ]    
    
    sol=Solves()
    sol.loadForm(lstForm)
    lst=sol.elemMatr
    a=lst[2].sum()
#    print a

    conc=rcMaterial.Concrete()
    conc.norme=52
    conc.b=25
    conc.initProperties()
    conc.functDia(typDia=3, typPS=1,typTime='short', typR=0, typRT=2)
    
    rein=rcMaterial.Reinforced()
    rein.norme=52
    rein.typ='A'
    rein.a=400
    rein.initProperties()
    rein.functDia(typPS=1)
    
    lstMat=[conc, rein]

    sol.loadMat(lstMat)

    xmatr=sol.xmatr
#    print xmatr

    ymatr=sol.ymatr
#    print ymatr
    kymatr=sol.kymatr
    yEvmatr=sol.yEvmatr
    kyEvmatr=sol.kyEvmatr

    
    nmxmy=[-10000,0,1000000]
    out=sol.nmxmy2e0rxry(nmxmy, 5000, 0.000001)
#    print out

    e0rxry=[out[0],out[1],out[2]]
    print e0rxry
    out=sol.e0rxry2nmxmy(e0rxry)
    
    e=np.reshape(out[4][0:100], (10, 10))
    sigma=np.reshape(out[3][0:100], (10, 10))
    print out[0:3]

    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter
    import matplotlib.pyplot as plt
    from matplotlib.mlab import griddata    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = sol.elemMatr[0][0:900]
    Y = sol.elemMatr[1][0:900]
    Z=out[3][0:900]
#    surf = ax.plot_surface(X, Y, Z)
    surf=ax.plot_trisurf(X, Y, Z, cmap=cm.terrain, linewidth=0.1)
#    Xtr=np.reshape(X, (30, 30))
#    Ytr=np.reshape(Y, (30, 30))
#    Ztr=np.reshape(Z, (30, 30))
#
#    surf = ax.plot_surface(Xtr, Ytr, Ztr, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
#    ax.set_zlim(-200, 200)
    
    ax.zaxis.set_major_locator(LinearLocator(20))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    
    fig.colorbar(surf)
#    CS = plt.contour(X, Y, Z, 15, linewidths=0.5, colors='k')
#    
    plt.show()    
    

    import matplotlib.tri as tri
    triang = tri.Triangulation(X, Y)
    plt.figure()
    plt.gca().set_aspect('equal')
    plt.tripcolor(triang, Z, shading='flat', cmap=plt.cm.rainbow)
    plt.colorbar()
    plt.title('tripcolor of Delaunay triangulation, flat shading')    
    plt.show()
#    for i in range(10000):
#    
#        
#        nmxmy=[-1,0,0]
#        
#        sol.nmxmy2e0rxry(nmxmy,100,0.001)
#       
#    nmxmy=[-2,0,0]
#    
#    print sol.nmxmy2e0rxry(nmxmy,100,0.001)
print 'ok'