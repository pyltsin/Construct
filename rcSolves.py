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
#        self.formGen()

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
        
    def formGenSC(self):
        '''Создает матрицу элементов
        type0 - флаг если начальные искривления
        Проверено, тесты не сделаны'''
        lst=self.formLst
        matrS=False
        firstS=False
        
        matrC=False
        firstC=False
        for i in lst:
            if self.lstMat[i.mat].title()=='Reinforced':
#                print 'tut'
                if firstS==False:
                    matrS=np.array(i.mesh())
                    firstS=True
                else:
                    matrS=np.concatenate((matrS,i.mesh()) ,axis=1)
            else:
                if firstC==False:
                    matrC=np.array(i.mesh())
                    firstC=True
                else:
                    matrC=np.concatenate((matrC,i.mesh()) ,axis=1)
        
        self.elemMatrC=matrC
        self.elemMatrS=matrS
        
        x,y=self.centerMass()
        
#        print self.elemMatrS[0]
        
        self.elemMatrS[0]-=x
    
        self.elemMatrS[1]-=y

        self.elemMatrC[0]-=x
        self.elemMatrC[1]-=y

        print len(matrC), len(matrS)
        self.elemMatr=np.concatenate((matrC,matrS) ,axis=1)

        
    def formGen(self):
        '''Создает матрицу элементов
        type0 - флаг если начальные искривления
        Проверено, тесты не сделаны'''
        self.formGenSC()        
        
#        print 'elemMatr', self.elemMatr
        matr=self.elemMatr
        
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
#        import time
#        startTime=time.time()
        xmatr=self.xmatr.copy()
        ymatr=self.ymatr.copy()
        kymatr=self.kymatr.copy()
#        print 'time1', (time.time()-startTime)*100000
#        startTime=time.time()
       
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

#        print 'time2', (time.time()-startTime)*100000
#        startTime=time.time()
        
        
        ymatr*=boolmatr
        ymatr=np.sum(ymatr, axis=0)
        
        kymatr*=boolmatr[:-1]
        kymatr=np.sum(kymatr, axis=0)
        
        xmatr*=boolmatr
        xmatr=np.sum(xmatr, axis=0)
        sigma=kymatr*(e-xmatr)+ymatr
#        print sigma
#        print 'time3', (time.time()-startTime)*100000

        return sigma
        
    def e2ev4(self, e):
        '''e - матрица e'''
        ebool=(e==0)
        ebool=ebool.astype(float)
        dev=self.dxmatr*ebool
        
        eTotal=e+ebool

#сигма
        xmatr=self.xmatr.copy()
        ymatr=self.ymatr.copy()
        kymatr=self.kymatr.copy()
        
        boolmatr=(e>xmatr)
        one=np.zeros(boolmatr.shape[1])
        
        boolmatrInvert=np.vstack((boolmatr[1:],one))
        boolmatrInvert=(boolmatrInvert==False)
        boolmatr=(boolmatr==boolmatrInvert)

        
        ymatr*=boolmatr
        ymatr=np.sum(ymatr, axis=0)
        
        kymatr*=boolmatr[:-1]
        kymatr=np.sum(kymatr, axis=0)
        
        xmatr*=boolmatr
        xmatr=np.sum(xmatr, axis=0)
        sigma=kymatr*(e-xmatr)+ymatr
#сигма
        ev=sigma/eTotal+dev
        return ev
        


    


    def e0rxry2nmxmy(self,e0rxry):
        '''возвращает значение усилий по дополнительным деформациям
        проверено - тестов нет'''
#        print e0rxry
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
        if d_11*(d_22*d_33-d_23**2)-d_12*(d_12*d_33-d_13*d_23)+d_13*(d_12*d_23-d_13*d_22)!=0 and (d_11*(d_23**2-d_22*d_33)+d_12**2*d_33-2*d_12*d_13*d_23+d_13**2*d_22)!=0:
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
#            print 'ee',ee
            dd=self.e2d(ee)
#            print 'dd0',dd[0]
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
            if error==1:
                return [False, False, False, 'Matr',n, []]
            else:
                if abs(e0f)<10**(-20):
                    tolE=abs(e0f-e0)
                else:
                    tolE=abs((e0f-e0)/e0f)

                if abs(rxf)<10**(-20):
                    tolRx=abs(rxf-rx)
                else:
                    tolRx=abs((rxf-rx)/rxf)

                if abs(ryf)<10**(-20):
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
                
        
    def loadLstMat(self, lstMat):
        self.lstMat=lstMat
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
        for i in self.formLst:
            lstCritPoint+=i.critPoint(e0,rx,ry)
        self.lstCritPoint=lstCritPoint
#        print 'lst', lstCritPoint

        x,y=self.centerMass()

        
        for i in self.lstCritPoint:
#            print 'i', i
            i[0]-=x
            i[1]-=y
#        print 'lstCritPoint', lstCritPoint
        return lstCritPoint
            
    def findKult6(self, nmxmy, nn, crit, typ='crit'):
        '''расчет в лоб.
        ограничение - <1000 и >1000'''
        
        nFact,mxFact,myFact=nmxmy
        nTemp,mxTemp,myTemp=nmxmy     
        nn3=20 #количество итераци на предвариловке
        crit3=crit*5
        n=0 #счетчик
        kDel=10.
#нашли работающую точку        
        while True:
            n+=1
            iterTemp=self.nmxmy2e0rxry([nTemp,mxTemp,myTemp], nn3, crit3)
            if type(iterTemp[3])!=type('error'):
                klst=self.kk(iterTemp[0:3], typ)
                k1=klst[0]
            if type(iterTemp[3])==type('error') or k1>1:
                nTemp,mxTemp,myTemp=nTemp/kDel,mxTemp/kDel,myTemp/kDel
                if n>3:
                    return 'error >1000'
                else:
                    continue
            else:
                break
#потом двоичный поиск

        n=0
        kDelCur=nTemp/nFact*10.
        kDel1=nTemp/nFact
        kDel2=kDelCur
        flagSearch=False
        while True:
            n+=1
            print'tt', kDelCur, kDel1, kDel2, nTemp

            if abs((kDelCur-kDel1)/kDelCur)<crit:
                nTemp,mxTemp,myTemp=nFact*kDel1,mxFact*kDel1,myTemp*kDel1

                kLen=nTemp/nFact
                e0rxryTemp=self.nmxmy2e0rxry([nTemp,mxTemp,myTemp], nn3, crit3)
#                print 'e0rxry', e0rxryTemp
                ee=self.e0rxry2e(e0rxryTemp[0],e0rxryTemp[1],e0rxryTemp[2]) #     
                dd=self.e2d(ee)[0]
                
                e0,rx,ry=0,0,0#устанавливаем начальные деофрмации
                ee=self.e0rxry2e(e0,rx,ry) #расчитываем матрицу деформаций
        
                ddel=self.e2d(ee) #определяем начальные dd
  

                dddel=[dd[0]/ddel[0][0],dd[3]/ddel[0][3],dd[5]/ddel[0][5]]
                return nmxmy, kLen,n, e0rxryTemp[0:3],  [nTemp,mxTemp,myTemp], dd,dddel, klst[1]

            if n>nn:
                return 'error n'
                
            nTemp,mxTemp,myTemp=nFact*kDelCur,mxFact*kDelCur,myTemp*kDelCur
            iterTemp=self.nmxmy2e0rxry([nTemp,mxTemp,myTemp], nn3, crit3)
            
            
            if type(iterTemp[3])!=type('error'):
                klst=self.kk(iterTemp[0:3], typ)
                k1=klst[0]
                
                
            if type(iterTemp[3])==type('error'):
                kDelCur=(kDelCur+kDel1)/2.
                kDel2=kDelCur
                flagSearch=True

                continue
            
            elif type(iterTemp[3])!=type('error') and k1>1:
                kDel2=kDelCur
                kDelCur=(kDel2+kDel1)/2.
                flagSearch=True
                continue                
            else:
                if flagSearch==True:
                    kDel1=kDelCur    
                    kDelCur=(kDel2+kDel1)/2. 
                else:
                    kDel1=kDelCur
                    kDelCur=kDel1*10.
                    kDel2=kDelCur
                continue
                            
    def findKult9(self, nmxmy, nn, crit, typ='crit'):
        '''поиск через DD'''
        nFact,mxFact,myFact=nmxmy #фиксируем усилия
        if nFact==0 and mxFact==0 and myFact==0:
            return nmxmy, 0, 0, [0,0,0],  [0,0,0], [0,0,0,0,0,0], [0,0,0], [[0,0,0,0],[0,0,0,0]]
            

        e0,rx,ry=0,0,0#устанавливаем начальные деофрмации
        ee=self.e0rxry2e(e0,rx,ry) #расчитываем матрицу деформаций

        ddel=self.e2d(ee) #определяем начальные dd

        e0rxry=self.matrSolve(nmxmy,ddel[0]) #определяем упругие деформации

        klst=self.kk(e0rxry[0:3], typ)
        k1=klst[0]#получаем коэффициент k - насколько надо разделить деформации, чтобы получить предельные 
#        print 'k111', k1
#        print 'klst', klst

        if k1==0:
            return 'error 1'
            
        e0rxryTemp=[e0rxry[0]/(k1/1.), e0rxry[1]/(k1/1.), e0rxry[2]/(k1/1.)] #получаем предельные дформации
        e0rxryTemp1=e0rxryTemp
        n=0
        while True:
            n+=1
#            print n
            if n>nn:
                return self.findKult7(nmxmy, nn, crit, typ='crit')
            ee=self.e0rxry2e(e0rxryTemp[0],e0rxryTemp[1],e0rxryTemp[2])
            dd=self.e2d(ee)
            e0rxry=self.matrSolve(nmxmy,dd[0])
            klst=self.kk(e0rxry[0:3], typ)
            k1=klst[0]#получаем коэффициент k - насколько надо разделить деформации, чтобы получить предельные 
    #        print 'k111', k1
    #        print 'klst', klst
    
            if k1==0:
                return 'error 2'
            e0rxryTemp=[e0rxry[0]/(k1/1.), e0rxry[1]/(k1/1.), e0rxry[2]/(k1/1.)] #получаем предельные дформации
            
            kk=[]
            for i in range(3):
                if e0rxryTemp1[i]!=0:
                    kk.append(abs((e0rxryTemp1[i]-e0rxryTemp[i])/e0rxryTemp1[i]))
                else:
                    kk.append(abs((e0rxryTemp1[i]-e0rxryTemp[i])))
            kCrit=max(kk)
#            print kCrit
            if kCrit<crit:
                
                '''возвращаем
                1 - усилия
                2- коэффициент
                3 - сколько итераций было
                4 - e0rxry для предельного состочняи
                5 - предельные усилия
                6 - d
                7 - d/de
                8 - klst - список макс e/emax'''
                nmxmyTemp=self.e0rxry2nmxmy(e0rxryTemp[0:3])
                nTemp, mxTemp, myTemp=nmxmyTemp[0:3]
#                e0rxry=self.nmxmy2e0rxry(nmxmyTemp[0:3],nn, crit)
#                print 'e0rxry', e0rxry
                klst=self.kk(e0rxryTemp[0:3], typ)
                k1=klst[0]#получаем коэффициент k - насколько надо разделить деформации, чтобы получить предельные 
                if k1==0:
                    return 'error 3'
                
                ee=self.e0rxry2e(e0rxryTemp[0]*0.8,e0rxryTemp[1]*0.8,e0rxryTemp[2]*0.8)
                dd1=self.e2d(ee)[0]
                
                print 'dd1', dd1
#                print e0rxryTemp[0:3]
#                print nmxmyTemp[0:3]
                
                dd=self.nmxmy2e0rxry([nmxmyTemp[0],nmxmyTemp[1],nmxmyTemp[2]], nn*20, crit)[5]
                print 'dd2', dd
#                print self.nmxmy2e0rxry([nmxmyTemp[0],nmxmyTemp[1],nmxmyTemp[2]], nn*20, crit)
#                print 'dd2', dd2[5]
#                print dd2[0:3]
#                print self.e0rxry2nmxmy(dd2[0:3])[0:3]   
#                
#                print 'del', ddel[0]
                e0,rx,ry=0,0,0#устанавливаем начальные деофрмации
                ee=self.e0rxry2e(e0,rx,ry) #расчитываем матрицу деформаций
        
                ddel=self.e2d(ee) #определяем начальные dd
  
#                print ddel[0], dd
                dddel=[dd[0]/ddel[0][0],dd[3]/ddel[0][3],dd[5]/ddel[0][5]]
                
                kLenN='-'
                kLenMx='-'
                kLenMy='-'
                
                kList=[]
                if nFact!=0:
                    kLenN=nTemp/nFact
                    kList.append(kLenN)
                if mxFact!=0:
                    kLenMx=mxTemp/mxFact
                    kList.append(kLenMx)

                if myFact!=0:
                    kLenMy=myTemp/myFact
                    kList.append(kLenMy)
                
                kS=sum(kList)/(len(kList)*1.)
                kSmin=min(kList)
#                print kS, kList
                for i in range(len(kList)):
                    if abs((kS-kList[i])/kS)>0.06:
#                        print abs((kS-kList[i])/kS),crit
                        return 'error 4'
                if abs(k1-1)>crit:
                    return 'error 5'
                if k1<0.8:
                    return 'error 6'
                return nmxmy, kSmin,n, e0rxryTemp[0:3],  [nTemp,mxTemp,myTemp], dd,dddel, klst[1]

            e0rxryTemp1=e0rxryTemp
                
            
    def findKult7(self, nmxmy, nn, crit, typ='crit'):
        
        nFact,mxFact,myFact=nmxmy
        nTemp,mxTemp,myTemp=nmxmy     
        nn3=20 #количество итераци на предвариловке
        crit3=crit*5
        n=0 #счетчик
        kDel=10.
#нашли работающую точку        
        while True:
            n+=1
            iterTemp=self.nmxmy2e0rxry([nTemp,mxTemp,myTemp], nn3, crit3)
            if type(iterTemp[3])!=type('error'):
                klst=self.kk(iterTemp[0:3], typ)
                k1=klst[0]
            if type(iterTemp[3])==type('error') or k1>1:
                nTemp,mxTemp,myTemp=nTemp/kDel,mxTemp/kDel,myTemp/kDel
                if n>3:
                    return 'error >1000'
                else:
                    continue
            else:
                break


        nTemp1,mxTemp1,myTemp1=nTemp,mxTemp,myTemp
        
#        print 'nTemp1,mxTemp1,myTemp1', nTemp1,mxTemp1,myTemp1, k1
    #пытаемся определисть iter2
        kn2=3.
        knlast=1.
        n=0
        nm=0
#            print 'n0', nTemp
        flagNM=False
        
        while True:
            nTemp,mxTemp,myTemp=nTemp1*kn2,mxTemp1*kn2,myTemp1*kn2
#            print 'nTemp', nTemp
            iterTemp=self.nmxmy2e0rxry([nTemp,mxTemp,myTemp], nn, crit)
#            print 'iterTemp', iterTemp[0:3]
            if type(iterTemp[3])!=type('error'):
                klst=self.kk(iterTemp[0:3], typ)
                k2=klst[0]
            
            if type(iterTemp[3])==type('error') or k2>1:
#                print 'nm',nm
                kn2=(kn2+knlast)/2.
                flagNM=True
                if nm>10:
                    return 'error 11'
                else:
                    nm+=1
                    continue
            n+=1
#            print 'n2', n

            nm=0
#                print 'iterTemp[0:3]', iterTemp[0:3]
#            print 'k2', klst
#            print 'kn2', kn2, knlast
            if k2==0:
                return 'error 12'
            if abs((kn2-knlast)/kn2)<crit:
                '''возвращаем
                1 - усилия
                2- коэффициент
                3 - сколько итераций было
                4 - e0rxry для предельного состочняи
                5 - предельные усилия
                6 - d
                7 - d/de
                8 - klst - список макс e/emax'''
                if nFact!=0:
                    kLen=nTemp/nFact
                elif mxFact!=0:
                    kLen=mxTemp/mxFact
                elif myFact!=0:
                    kLen=myTemp/myFact

                e0rxryTemp=self.nmxmy2e0rxry([nTemp,mxTemp,myTemp], nn, crit)
#                print 'e0rxry', e0rxryTemp
                ee=self.e0rxry2e(e0rxryTemp[0],e0rxryTemp[1],e0rxryTemp[2]) #     
                dd=self.e2d(ee)[0]
                
                e0,rx,ry=0,0,0#устанавливаем начальные деофрмации
                ee=self.e0rxry2e(e0,rx,ry) #расчитываем матрицу деформаций
        
                ddel=self.e2d(ee) #определяем начальные dd
  

                dddel=[dd[0]/ddel[0][0],dd[3]/ddel[0][3],dd[5]/ddel[0][5]]
                return nmxmy, kLen,n, e0rxryTemp[0:3],  [nTemp,mxTemp,myTemp], dd,dddel, klst[1]
                
            if flagNM==False:
                knlast=kn2
                kn2=kn2*3.
            else:
                knTemp=knlast
                knlast=kn2
                kn2=kn2*kn2/knTemp                       
            if n>nn:
                return 'error 13'
            else:
                continue




    def kk(self,e0rxry, typ='crit'):
        '''определяем коэффициент исопльзования по всем нормам 
        - самое простое - переслать в материалы список emax и emin
        1. сначала вычисляем  расположение критических точек
        typ=crit - расчет критической силы, если crc - расчет трещин'''
#        print 'e0rxry', e0rxry
        e0, rx,ry=e0rxry
#        print 'e0rxry', e0rxry
        lstCritPoint=self.critPoint(e0, rx,ry)      
        '''ищем максимальное число материалов'''
        nMat=len(self.lstMat)
        nlst=[]
        for i in range(nMat):
            nlst.append([False, False])
#        print 'nlst', nlst

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
                    
#        print 'nlst', nlst
                    
#        print 'nlst2', nlst
        '''вычисляем k для каждого материала'''
        kk=[]
        klst=[]
        if typ=='crit':
            for i in range(nMat):
                item=self.lstMat[i].kk(nlst[i])
                kk.append(item[0])
                klst.append(item)
        elif typ=='crc':
            for i in range(nMat):
                item=self.lstMat[i].kcrc(nlst[i])
                kk.append(item[0])
                klst.append(item)
            
            
#        print 'kk', kk
        k=max(kk)
            
        return k, klst 
        
    def EJ(self):
        ln=len(self.elemMatr[0])
        matrBolS=np.zeros(ln)
        matrBolB=np.zeros(ln)

        for i in range(len(self.lstMat)):
            if self.lstMat[i].title()=='Concrete':
                matrBolTemp=(self.elemMatr[3]==i)
                matrBolB+=matrBolTemp*self.lstMat[i].e()
            else:
                matrBolTemp=(self.elemMatr[3]==i)
                matrBolS+=matrBolTemp*self.lstMat[i].e()
                
        matrEbJx=self.elemMatr[0]*self.elemMatr[0]*self.elemMatr[2]*matrBolB
        EbJx=matrEbJx.sum()

        matrEbJy=self.elemMatr[1]*self.elemMatr[1]*self.elemMatr[2]*matrBolB
        EbJy=matrEbJy.sum()

        matrEsJx=self.elemMatr[0]*self.elemMatr[0]*self.elemMatr[2]*matrBolS
        EsJx=matrEsJx.sum()

        matrEsJy=self.elemMatr[1]*self.elemMatr[1]*self.elemMatr[2]*matrBolS
        EsJy=matrEsJy.sum()
        
        return EbJx, EbJy, EsJx, EsJy
        
    def nuD(self, lstNMxMy, typStat, lx, ly, l, typD):
        '''расчет внецентреного сжатия'''
#        сначала определяем e0 в см
        e01=0.01
        e02=l/600.
        
#дальше определяем e для оси х
        x1=False
        x2=False
        lstTempCritPointX=self.critPoint(0,1,0)
        for i in lstTempCritPointX:
            if x1==False and x2==False:
                x1=i[0]
                x2=i[0]
            elif x1>i[0]:
                x1=i[0]
            elif x2<i[0]:
                x2=i[0]
        b=(x2-x1)/100.
        
        e03x=b/30.
        
#дальше определяем e для оси y
        y1=False
        y2=False
        lstTempCritPointY=self.critPoint(0,0,1)
        for i in lstTempCritPointY:
            if y1==False and y2==False:
                y1=i[1]
                y2=i[1]
            elif y1>i[1]:
                y1=i[1]
            elif y2<i[1]:
                y2=i[1]
        h=(y2-y1)/100.
        e03y=h/30.
        eax=max([e01, e02, e03x])
        eay=max([e01, e02, e03y])
        
        EbJx, EbJy, EsJx, EsJy=self.EJ()
        
        
        
        error=True
        out=[]
#закольцовываем расчет
        for nmxmy in lstNMxMy:
#            print 'nmxmy', nmxmy
            n,mx,my, nl, mxl, myl =nmxmy
#определяем усилие при N:
            if n>=0 or typD==False:
                ex=0
                ey=0
                NcrNx=0
                NcrNy=0
                nux=1
                nuy=1
                MxNux=mx
                Mx=mx
                MyNuy=my
                My=my
                phiLx=''
                phiLy=''
                deltaEx=''
                deltaEy=''
                Dx=''
                Dy=''
                Ncrx=''
                Ncry=''
            else:
                ex=mx/n
                ey=my/n
                
                if nl!=0:
                    exl=mxl/nl
                    eyl=myl/nl
                else:
                    exl=0
                    eyl=0
#уточняем усилие по e                
                if typStat==False:
                    if abs(ex)<abs(eax):
                        if ex>=0:
                            ex=abs(eax)
                        else:
                            ex=-abs(eax)
                    if abs(ey)<abs(eay):
                        if ey>=0:
                            ey=abs(eay)
                        else:
                            ey=-abs(eay)
                            
                    if abs(exl)<abs(eax):
                        if exl>=0:
                            exl=abs(eax)
                        else:
                            exl=-abs(eax)
                    if abs(eyl)<abs(eay):
                        if eyl>=0:
                            eyl=abs(eay)
                        else:
                            eyl=-abs(eay)

                else:
                    if ex>=0:
                        ex+=eax
                    else:
                        ex-=eax
                    if ey>=0:
                        ey+=eay
                    else:
                        ey-=eay

                    if exl>=0:
                        exl+=eax
                    else:
                        exl-=eax
                    if eyl>=0:
                        eyl+=eay
                    else:
                        eyl-=eay

                
                Mx=n*ex
                My=n*ey
                
                if nl!=0:
                    Mxl=nl*exl
                    Myl=nl*eyl
                else:
                    Mxl=mxl
                    Myl=myl
#определеяем phiL
                if n==0 and Mx==0:
                    phiLx=1
                else:
                    lstmxT=[]
                    lstmxlT=[]
                    matrS=np.transpose(self.elemMatrS)
                    for i in matrS:
                        lstmxT.append(Mx+n*i[0]/100.)
                        lstmxlT.append(Mxl+nl*i[0]/100.)
                    phiLx=max(lstmxlT)/max(lstmxT)+1.
    
                if n==0 and My==0:
                    phiLy=1
                else:
                    lstmyT=[]
                    lstmylT=[]
                    matrS=np.transpose(self.elemMatrS)
                    for i in matrS:
                        lstmyT.append(My+n*i[1]/100.)
                        lstmylT.append(Myl+nl*i[1]/100.)
                    phiLy=max(lstmylT)/max(lstmyT)+1.
                    
                        
                if phiLx>2:
                    phiLx=2
                if phiLx<1:
                    phiLx=1
                    
                if phiLy>2:
                    phiLy=2
                if phiLy<1:
                    phiLy=1
    #определяем deltaE
    
                deltaEx=abs(ex/b)
                deltaEy=abs(ey/h)
                
                deltaEx=max(deltaEx, 0.15)
                deltaEy=max(deltaEy, 0.15)
                
                kbx=0.15/(phiLx*(0.3+deltaEx))
                kby=0.15/(phiLy*(0.3+deltaEy))
                
                Dx=(kbx*EbJx+0.7*EsJx)/1000./100./100.
                Dy=(kby*EbJy+0.7*EsJy)/1000./100./100.
                
                if lx==0:
                    Ncrx=''
                    NcrNx=0
                    MxNux=Mx
                    nux=1
                else:
                    Ncrx=3.14*3.14*Dx/lx**2
                    NcrNx=abs(n/Ncrx)
                    if NcrNx>=1:
                        error=False
                        nux='Error'
                        MxNux='Error'
                    else:
                        nux=1/(1-NcrNx)
                        MxNux=nux*Mx
                        
                if ly==0:
                    Ncry=''
                    NcrNy=0
                    MyNuy=My
                    nuy=1
                else:
                    Ncry=3.14*3.14*Dy/ly**2
                    NcrNy=abs(n/Ncry)
                    if NcrNy>=1:
                        error=False
                        nuy='Error'
                        MyNuy='Error'
                        
                    else:
                        nuy=1/(1-NcrNy)
                        MyNuy=nuy*My
        
            outitem=[n, MxNux, MyNuy, NcrNx, NcrNy, nux, nuy, Mx, My, ex, ey, phiLx, phiLy, deltaEx, deltaEy, Dx, Dy, Ncrx, Ncry]
            out.append(outitem)    

        return [out, error]

                    
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
#    print a

    conc=rcMaterial.Concrete()
    conc.norme=52
    conc.b=25
    conc.initProperties()
    conc.functDia(typDia=3, typPS=1,typTime='short', typR=3, typRT=2)
#    print conc.x,conc.y 
    rein=rcMaterial.Reinforced()
    rein.norme=52
    rein.typ='A'
    rein.a=400
    rein.initProperties()
    rein.functDia(typPS=1)
#    print rein.x, rein.y
    lstMat=[conc, rein]

    sol.loadMat(lstMat)

    sol.formGen()
    lst=sol.elemMatr
    a=lst[2].sum()


    xmatr=sol.xmatr
#    print xmatr

    ymatr=sol.ymatr
#    print ymatr
    kymatr=sol.kymatr
    yEvmatr=sol.yEvmatr
    kyEvmatr=sol.kyEvmatr
#    print 'tt1', sol.e0rxry2nmxmy([-0.00034524213289891469, 2.1031719114007239e-05, 0.00010515859557003618])
#    print 'tt2', sol.e0rxry2nmxmy([-1.525417962731393e-05, 2.3231638802484486e-05, 0.00011615819401242296])

#    nmxmy=[-100000,0.0,0.0]
#    nmxmy=[-200000.,600000.,1000000.] #- [-200000,600000,1000000] - граничное ошибка 
    nmxmy=[0,0,2]
    
#    nmxmy=[-22305*2,1110*2,223000*2]
#    nmxmy=[-100,500,2500]
#    nmxmy=[-200000,1000000,40000400]

#    out=sol.nmxmy2e0rxry(nmxmy, 100, 0.00001)
##    print 'out', out
#
#    e0rxry=[out[0],out[1],out[2]]
##    print 'e0rxry11', e0rxry
#    out=sol.e0rxry2nmxmy(e0rxry)
#    
#    e=np.reshape(out[4][0:100], (10, 10))
#    sigma=np.reshape(out[3][0:100], (10, 10))
#    print out[0:3]
#    e0rxry=sol.nmxmy2e0rxry(nmxmy,1000,0.0001)
#    print 'e0rxry', e0rxry[0:3]
#    print 'kk' , sol.kk(e0rxry[0:3])
#    for i in range(100):
    kk1=sol.findKult9(nmxmy, 100,0.001)
#        kk2=sol.findKult7(nmxmy, 100,0.001)

# пока рабочее - 7 вариант    
#    
    print 'kult', kk1
#    print 'kult', kk2
    e0rxry=kk1[3]
    out=sol.e0rxry2nmxmy(e0rxry)
#    print out[0], out[1] , out[2]   
#
#    '''проверка скорости ключевой функции'''
#    
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
##    ax.set_zlim(-200, 200)
#    
#    ax.zaxis.set_major_locator(LinearLocator(20))
#    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
#    
#    fig.colorbar(surf)
##    CS = plt.contour(X, Y, Z, 15, linewidths=0.5, colors='k')
##    
    plt.show()    
##    
##
##    import matplotlib.tri as tri
##    triang = tri.Triangulation(X, Y)
##    plt.figure()
##    plt.gca().set_aspect('equal')
##    plt.tripcolor(triang, Z, shading='flat', cmap=plt.cm.rainbow)
##    plt.colorbar()
##    plt.title('tripcolor of Delaunay triangulation, flat shading')    
##    plt.show()
###    for i in range(10000):
###    
###        
###        nmxmy=[-1,0,0]
###        
###        sol.nmxmy2e0rxry(nmxmy,100,0.001)
###       
###    nmxmy=[-2,0,0]
###    
###    print sol.nmxmy2e0rxry(nmxmy,100,0.001)
##print 'ok'