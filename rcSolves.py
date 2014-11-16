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
        matr=False
        for i in lst:
            if matr==False:
                matr=np.array(i.mesh())
            else:
                matr=np.concatenate((matr,i.mesh()) ,axis=1)
            
        self.elemMatr=matr
        x,y=self.centerMass()
        self.elemMatr[0]-=x
        self.elemMatr[1]-=y
#        print 'elemMatr', self.elemMatr
    def e0rxry2e(self,e0=0,rx=0,ry=0):
        '''создаем матрицу e'''
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
        
        return [d11Sum,d12Sum,d13Sum,d22Sum,d23Sum,d33Sum]

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
        '''e - матрица e'''
        xmatr=self.xmatr
        ymatr=self.ymatr
        kymatr=self.kymatr
#        print e.shape
#        print xmatr.shape
#        print self.elemMatr
        
        boolmatr=(e<xmatr)
#        print boolmatr
#        print e
#        print xmatr
        one=np.zeros(boolmatr.shape[1])
        
        boolmatrInvert=np.vstack((one,boolmatr[:-1]))
        boolmatrInvert=(boolmatrInvert==False)
        boolmatr=(boolmatr==boolmatrInvert)
        
#        xmatr*=boolmatr
#        xmatr=np.sum(xmatr, axis=0)
        
        ymatr*=boolmatr
        ymatr=np.sum(ymatr, axis=0)
        
        kymatr*=boolmatr[:-1]
        kymatr=np.sum(kymatr, axis=0)
        
        sigma=kymatr*e+ymatr
        
        return sigma
        
    def e2ev4(self, e):
        '''e - матрица e'''
        xmatr=self.xmatr
        ymatr=self.yEvmatr
        kymatr=self.kyEvmatr
#        print e.shape
#        print xmatr.shape
#        print self.elemMatr
        
        boolmatr=(e<xmatr)
#        print boolmatr
#        print e
#        print xmatr
        one=np.zeros(boolmatr.shape[1])
        
        boolmatrInvert=np.vstack((one,boolmatr[:-1]))
        boolmatrInvert=(boolmatrInvert==False)
        boolmatr=(boolmatr==boolmatrInvert)
        
#        xmatr*=boolmatr
#        xmatr=np.sum(xmatr, axis=0)
        
        ymatr*=boolmatr
        ymatr=np.sum(ymatr, axis=0)
        
        kymatr*=boolmatr[:-1]
        kymatr=np.sum(kymatr, axis=0)
        
        ev=kymatr*e+ymatr
        
        return ev
        


    '''Версия 3 интерполяции - через функцию здесь'''
    def e2sigma3(self, e):
        '''возвращает матрицу sigma от e'''     
#        print self.ufunE2sigma2()(e, self.elemMatr[3])
        return self.ufunE2sigma3()(e, self.elemMatr[3])


    def funE2sigma3(self, x, numMat):
        '''просто фнкция для определения e2sigma от номера материала - для перевода ее в uFun'''
#        Вытаскиваем из lst список необходимых матриц и интеполция простым перебором
        num=int(numMat)
        lstx=self.lstx[num]
        lsty=self.lsty[num]
        lstky=self.lstky[num]
        for i in xrange(len(lstx)-1):
            if lstx[i]<=x<=lstx[i+1]:
                y1=lstky[i]*x+lsty[i+1]
                return y1
        

    def ufunE2sigma3(self):
        '''возвращает функцию funE2ev для массивов'''
        return np.frompyfunc(self.funE2sigma3,2,1)



    '''Версия 3 интерполяции - через функцию здесь'''
    def e2ev3(self, e):
        '''возвращает матрицу sigma от e'''     
#        print self.ufunE2sigma2()(e, self.elemMatr[3])
        return self.ufunE2ev3()(e, self.elemMatr[3])


    def funE2ev3(self, x, numMat):
        '''просто фнкция для определения e2sigma от номера материала - для перевода ее в uFun'''
#        Вытаскиваем из lst список необходимых матриц и интеполция простым перебором
        num=int(numMat)
        lstx=self.lstx[num]
        lsty=self.lstyEv[num]
        lstky=self.lstkyEv[num]
        for i in xrange(len(lstx)-1):
            if lstx[i]<=x<=lstx[i+1]:
                y1=lstky[i]*x+lsty[i+1]
                return y1
        

    def ufunE2ev3(self):
        '''возвращает функцию funE2ev для массивов'''
        return np.frompyfunc(self.funE2ev3,2,1)

    


    def e0rxry2nmxmy(self,e0rxry):
        '''возвращает значение усилий по дополнительным деформациям'''
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
        return nSum, mxSum, mySum
        
        
    def matrSolve(self, nmxmy, dd):
        '''расчет матрицы'''
        n, m_x, m_y=nmxmy
        d_11,d_12,d_13,d_22,d_23,d_33=dd
        if d_11*(d_22*d_33-d_23**2)-d_12*(d_12*d_33-d_13*d_23)+d_13*(d_12*d_23-d_13*d_22)!=0:
            e0=(d_12*(d_33*m_y-d_23*n)+d_13*(d_22*n-d_23*m_y)+(d_23**2-d_22*d_33)*m_x)/(d_11*(d_23**2-d_22*d_33)+d_12**2*d_33-2*d_12*d_13*d_23+d_13**2*d_22)
            rx=-(d_11*(d_33*m_y-d_23*n)+d_12*d_13*n-d_13**2*m_y+(d_13*d_23-d_12*d_33)*m_x)/(d_11*(d_23**2-d_22*d_33)+d_12**2*d_33-2*d_12*d_13*d_23+d_13**2*d_22)
            ry=(d_11*(d_23*m_y-d_22*n)+d_12**2*n-d_12*d_13*m_y+(d_13*d_22-d_12*d_23)*m_x)/(d_11*(d_23**2-d_22*d_33)+d_12**2*d_33-2*d_12*d_13*d_23+d_13**2*d_22)
            error=0
        else:
            e0 = 0
            rx= 0
            ry = 0
            error = 1
        return [e0,rx,ry,error]

    def nmxmy2e0rxry(self,nmxmy, nn, crit):
        '''определение e0rxry, nn - макс кол-во итераций, criter - критерий сходимости
        Возвращает список: e0f, rxf, ryf, tol
        При ошибке tol==string'''
        e0,rx,ry=0,0,0
#        dn, dmx, dmy=self.e0rxry2nmxmy([e0,rx,ry])
#        nmxmy=[nmxmy[0]+dn,nmxmy[1]+dmx,nmxmy[2]+dmy]
        n=0
        while True:
            ee=self.e0rxry2e(e0,rx,ry)
            dd=self.e2d(ee)            
            e0f,rxf,ryf,error=self.matrSolve(nmxmy,dd)
            
            if error==1:
                return [False, False, False, 'Matr']
            else:
                if e0f==0:
                    tolE=abs(e0f-e0)
                else:
                    tolE=abs((e0f-e0)/e0f)

                if rxf==0:
                    tolRx=abs(rxf-rx)
                else:
                    tolRx=abs((rxf-rx)/rxf)

                if ryf==0:
                    tolRy=abs(ryf-ry)
                else:
                    tolRy=abs((ryf-ry)/ryf)

                    
                tol=max(tolE, tolRx, tolRy)

                if tol<crit:
                    return [e0f, rxf, ryf, tol]
                
                if n>nn:
                    return [False, False, False, 'Nmax']
                
                e0, rx,ry=e0f, rxf, ryf  
                n+=1
                
        
    
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
        
        lstx=[]
        lsty=[]
        lstky=[]
        lstyEv=[]
        lstkyEv=[]
        for i in lstMat:
            if i.title()=='Concrete':
                if typLst==False:
#                    lstFunDia2.append(i.functDia2)
                    lstx.append(i.x)
                    lsty.append(i.y)
                    lstky.append(i.ky)
                    lstyEv.append(i.yEv)
                    lstkyEv.append(i.kyEv)

                else:
                    lstFunDia.append(i.functDiaLst(lst))
            elif i.title()=='Reinforced':
                if typLst==False:
                    lstFunDia.append(i.functDia2())
                else:
                    lstFunDia.append(i.functDiaLst(lst))
                    
        self.lstFunE2ev2=lstFunDia2
        self.lstx=lstx
        self.lsty=lsty
        self.lstky=lstky
        self.lstyEv=lstyEv
        self.lstkyEv=lstkyEv

        '''теперь создаем матрицу соответствующую № массива'''
        
        xmatr=None
        
        ymatr=None
        kymatr=None

        yEvmatr=None
        kyEvmatr=None
        
        for i in self.formLst:
            ln=i.ln()
            xone=np.ones(ln)
            
            xmatrTemp= np.array(lstx[i.mat])
            xmatrTemp=np.meshgrid(xmatrTemp,xone)
            xmatrTemp=xmatrTemp[0]
            xmatrTemp=xmatrTemp.transpose()
                        
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
                ymatr=ymatrTemp
                kymatr=kymatrTemp
                yEvmatr=yEvmatrTemp
                kyEvmatr=kyEvmatrTemp
            else:
                xmatr=np.hstack((xmatr,xmatrTemp))
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
                
        
    def critPoint(self, e, rx,ry):
        lstCritPoint=[]
        for i in self.lstForm:
            lstCritPoint+=i.critPoint(e,rx,ry)
        self.lstCritPoint=lstCritPoint
        return lstCritPoint

    
if __name__ == "__main__":
    lstForm=[['Rectangle',[[1.,1.],[3.,3.]],[50.,50.],0,1,[0,0,0]]]
    
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
    
    for i in range(10000):
    
#        e0rxry=[-0.0025,0,0]
#    #    
#        sol.e0rxry2nmxmy(e0rxry)
        
        nmxmy=[-1,0,0]
        
        sol.nmxmy2e0rxry(nmxmy,100,0.001)
#        
    nmxmy=[-2,0,0]
    
    print sol.nmxmy2e0rxry(nmxmy,100,0.001)
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