# -*- coding: utf-8 -*-
"""
Created on Fri Nov 07 17:49:22 2014

@author: admin
"""
from table import tables_csv
import numpy as np
from scipy import interpolate

class Reinforced(object):
    '''Класс для работы с арматурой и всем что с ней связано'''
    def __init__(self):
        
        self.norme=False 
        self.approxSP=False
        self.typ=False
        self.rn=False
        self.ys=False
        self.ysi=1
        self.ysni=1
    
    def initProperties(self):
        '''расчет и запись исходных значений для отображения, возвращает список;
        если approx=True - по аппроксимации, по а и ys
        eсли norme=52: то по списку по a
        eсли norme=63: то по списку по a'''
        if self.approxSP==True:
            return self.propertiesApproxSP()
        else:
            if self.norme==52:
                return self.propertiesSP52()
            elif self.norme==63:
                return self.propertiesSP63()
                
    def setA(self, txt):
        '''назначить typm rn'''
        self.typ=txt[0]
        self.rn=int(txt[1:])
        
    def propertiesApproxSP(self):
        '''аппроксимирующие функции определния характеристик бетона с A240'''
        a=self.rn
        ys=self.ys
        rsn=a*100/9.81
        rs=rsn/ys
        
        rs/=self.ysi

        if self.typ==u'K':
            es=1.95*10**5*100/9.81
        else:        
            es=2.0*10**5*100/9.81
            
        if a>=600:
            es0=rs/es+0.002
            es2=0.015
        else:
            es0=rs/es
            es2=0.025
    
            
        rsw=rs*0.8
        if rsw>=300*100/9.81:
            rsw=300*100/9.81
        
        self.rsn, self.rs, self.rsw, self.es, self.es0, self.es2=rsn,rs,rsw, es, es0, es2
        return rsn,rs,rsw, es, es0, es2

    def functDiaLst(self, lst):
        '''Возвращает функцию по интерполяции по списку'''
        x=lst[0]
        y=lst[1]
        x=np.array(x)
    
        y=np.array(y)        
    
        
        funSigma=interpolate.interp1d(x,y, kind='linear')
        ev=[]
        for i in range(len(x)):
            if x[i]!=0:
                ev.append(y[i]/x[i])
            else:
                if i+1>len(x):
                    ev.append(y[i-1]/x[i-1])
                else:
                    ev.append(y[i+1]/x[i+1])
        funEv=interpolate.interp1d(x,ev, kind='linear')
        
        return [funSigma, funEv]

    def functDia(self, typPS):
        '''возвращает функцию по интерполяции по графику (общему)
        typPS - тип предельного состояния'''
        
        if typPS==1:
            r=self.rs
        else:
            r=self.rsn
        
        if self.rn<600:
            x=[-self.es2,-self.es0,0,self.es0,self.es2]
            y=[-r,-r,0,r,r]
        else:
            es1=0.9*r/self.es
            sigmas1=0.9*r
            sigmas2=1.1*r
            e3=(self.es2-es1)/1.1+es1
            x=[-self.es2,-es1,-e3,0,e3, es1,self.es2]
            y=[-sigmas2,-sigmas2,-sigmas1,0,sigmas1,sigmas2]
            
        x.append(x[-1]*1000000.)
        y.append(y[-1])
    
        x.insert(0,x[0]*1000000.)
        y.insert(0,y[0])

    
        x=np.array(x)
    
        y=np.array(y)        
    
        
        funSigma=interpolate.interp1d(x,y, kind='linear')
        ev=[]
        for i in range(len(x)):
            if x[i]!=0:
                ev.append(y[i]/x[i])
            else:
                if i+1>len(x):
                    ev.append(y[i-1]/x[i-1])
                else:
                    ev.append(y[i+1]/x[i+1])
        funEv=interpolate.interp1d(x,ev, kind='linear')
        
        return [funSigma, funEv]

        
    def listSP52(self):
        '''возвращает список доступных классов по СП52'''
        fil=tables_csv(filename='MaterialData\\reinfSP52.csv', typ='none')
        return fil.get_title_column()
    def listSP63(self):
        '''возвращает список доступных классов по СП63'''
        fil=tables_csv(filename='MaterialData\\reinfSP63.csv', typ='none')
        return fil.get_title_column()
    
    
    def propertiesSP52(self):
        name=self.typ+str(self.rn)
        fil=tables_csv(filename='MaterialData\\reinfSP52.csv', typ='float')
        table=fil.get_table()
        index=False
        for i in table[1:]:
#            print name, i[0]
            if name==i[0]:
                index=i
        if index!=False:
            self.rsn, self.rs, self.rsw, self.es, self.es0, self.es2, self.ys=index[1:]
            self.rs/=self.ysi
            self.rsw/=self.ysi
            
            self.rsn*=(100/9.81)
            self.rs*=(100/9.81)
            self.rsw*=(100/9.81)
            self.es*=(100/9.81)
            
            return self.rsn, self.rs, self.rsw, self.es, self.es0, self.es2
            
    def propertiesSP63(self):
        name=self.typ+str(self.rn)
        fil=tables_csv(filename='MaterialData\\reinfSP63.csv', typ='float')
        table=fil.get_table()
        index=False
        for i in table[1:]:
            if name==i[0]:
                index=i
        if index!=False:
            self.rsn, self.rs, self.rsw, self.es, self.es0, self.es2, self.ys=index[1:]
            self.rs/=self.ysi
            self.rsw/=self.ysi

            self.rsn*=(100/9.81)
            self.rs*=(100/9.81)
            self.rsw*=(100/9.81)
            self.es*=(100/9.81)


            return self.rsn, self.rs, self.rsw, self.es, self.es0, self.es2
    
    

    def title(self):
        return 'Reinforced'
        
class Concrete(object):
    '''Класс для работы с бетоном и всем что с ней связано'''

    def __init__(self):
        self.norme=False 
        self.approxSP=False
        self.phi=75
        self.b=False
        self.yb=1
        self.c1=False
        self.c2=False

    def initProperties(self):
        '''расчет и запись исходных значений для отображения, возвращает список;
        если approx=True - по аппроксимации, по а и ys
        eсли norme=52: то по списку по a
        eсли norme=63: то по списку по a'''
        if self.approxSP==True:
            return self.propertiesApproxSP()
        else:
            if self.norme==52:
                return self.propertiesSP52()
            elif self.norme==63:
                return self.propertiesSP63()

        
    def propertiesSP52(self):
        self.ephi()
        name=unicode(self.b)
        fil=tables_csv(filename='MaterialData\\concreteSP52.csv', typ='float')
        table=fil.get_table()
        index=False
        for i in table[1:]:
            if name==i[0]:
                index=i
        if index!=False:
            self.rbn, self.rbtn, self.rb, self.rbt, self.eb=index[1:]
            self.rbn*=(100/9.81)
            self.rbtn*=(100/9.81)
            self.rb*=(100/9.81/self.yb)
            self.rbt*=(100/9.81/self.yb)
            self.eb*=(100/9.81)

            return self.rbn, self.rb, self.rbtn, self.rbt, self.eb, self.eb0, self.eb2, self.eb1red, self.ebt0, self.ebt2, self.ebt1red, self.ebl0, self.ebl2, self.ebl1red, self.eblt0, self.eblt2, self.eblt1red, self.phi_crc

    def propertiesSP63(self):
        self.ephi()
        name=unicode(self.b)
        fil=tables_csv(filename='MaterialData\\concreteSP63.csv', typ='float')
        table=fil.get_table()
        index=False
        for i in table[1:]:
            if name==i[0]:
                index=i
        if index!=False:
            self.rbn, self.rbtn, self.rb, self.rbt, self.eb=index[1:]

            self.rbn*=(100/9.81)
            self.rbtn*=(100/9.81)
            self.rb*=(100/9.8/self.yb)
            self.rbt*=(100/9.81/self.yb)
            self.eb*=(100/9.81)


            return self.rbn, self.rb, self.rbtn, self.rbt, self.eb, self.eb0, self.eb2, self.eb1red, self.ebt0, self.ebt2, self.ebt1red, self.ebl0, self.ebl2, self.ebl1red, self.eblt0, self.eblt2, self.eblt1red, self.phi_crc

    
    def listSP52(self):
        '''возвращает список доступных классов по СП52'''
        fil=tables_csv(filename='MaterialData\\concreteSP52.csv', typ='none')
        return fil.get_title_column()
    def listSP63(self):
        '''возвращает список доступных классов по СП63'''
        fil=tables_csv(filename='MaterialData\\concreteSP63.csv', typ='none')
        return fil.get_title_column()

    def functDiaLst(self, lst):
        '''Возвращает функцию по интерполяции по списку'''
        x=lst[0]
        y=lst[1]
        x=np.array(x)
    
        y=np.array(y)        
    
        
        funSigma=interpolate.interp1d(x,y, kind='linear')
        ev=[]
        for i in range(len(x)):
            if x[i]!=0:
                ev.append(y[i]/x[i])
            else:
                if i+1>len(x):
                    ev.append(y[i-1]/x[i-1])
                else:
                    ev.append(y[i+1]/x[i+1])
        funEv=interpolate.interp1d(x,ev, kind='linear')
        
        return [funSigma, funEv]
        
    def title(self):
        return 'Concrete'
#    
#    def functDia2(self,x):
#        lstx=self.x
#        lsty=self.y
#        lstyEv=self.yEv
#        lstky=self.ky
#        lstkyEv=self.kyEv
##        print lstx, lsty
##        i3=len(lstx)-1
##        i2=len(lstx)//2
##        i1=0
###        print 'i', i1,i2,i3
###        print 'lst',lstx, x
##        if lstx[0]<=x and lstx[-1]>=x:
##            while i1!=i2:
###                print 'i', i1, i2, i3
##                if lstx[i1]<=x and lstx[i2]>=x:
##                    if i2-i1==1:
##                        y1=lstky[i2-1]*x+lsty[i2]
##                        y2=lstkyEv[i2-1]*x+lstyEv[i2]
###                        print '11'                        
##                        return [y1, y2]
##
##                    else:
##                        i3=i2
##                        i2=(i2-i1)//2+i1
##                        
##                else:
##                    i1=i2
##                    i2=(i3-i2)//2+i2
#                    
#        for i in range(len(self.x)-1):
##            print lstx[i], lstx[i+1], x
##            print lstx[i]<=x and lstx[i+1]<=x
#            if lstx[i]<=x<=lstx[i+1]:
#                y1=lstky[i]*x+lsty[i+1]
#                y2=lstkyEv[i]*x+lstyEv[i+1]
##                print y1, y2 , 'y1'
#                return [y1, y2]
            
    def functDia(self, typDia, typPS, typTime, typR, typRT):
        '''Отдача функции расчета sigma по e или v по e
        typDia - тип диаграммы для бетонна, 
        typPS - тип предельного состояния, 
        typTime - long или short для бетона, 
        typR - для бетона, если 1 - просто режется все -, если 2 - после последнего значения - до 0, другое - продлеваем до max, 
        typRT - для бетона, если 1 - просто режется все +, если 2 - после последнего значения - до 0, другое - продлеваем до max'''

        rbn,rb,rbtn,rbt,eb= self.rbn, self.rb, self.rbtn, self.rbt, self.eb
        eb0, eb2, eb1red, ebt0, ebt2, ebt1red= self.eb0, self.eb2, self.eb1red, self.ebt0, self.ebt2, self.ebt1red
        ebl0, ebl2, ebl1red, eblt0, eblt2, eblt1red=self.ebl0, self.ebl2, self.ebl1red, self.eblt0, self.eblt2, self.eblt1red 
        phi_crc=self.phi_crc
        
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
            eb=eb/(1+phi_crc)

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
    
        if typR==1:
            n=0
            for i in x:
               if i<0:
                   y[n]=0
               n+=1
        elif typR==2:
            x.insert(0,x[0]*1.001)
            y.insert(0,0)
               
        if typRT==1:
            n=0
            for i in x:
               if i>0:
                   y[n]=0
               n+=1
        elif typRT==2:
            x.append(x[-1]*1.001)
            y.append(0)
        
        x.append(x[-1]*1000000.)
        y.append(y[-1])
    
        x.insert(0,x[0]*1000000.)
        y.insert(0,y[0])
    
        
        x=np.array(x)
        y=np.array(y)        
    
        
        funSigma=interpolate.interp1d(x,y, kind='linear')
        ev=[]
        for i in range(len(x)):
            if x[i]!=0:
                ev.append(y[i]/x[i])
            else:
                if i+1>len(x):
                    ev.append(y[i-1]/x[i-1])
                else:
                    ev.append(y[i+1]/x[i+1])
                
        funEv=interpolate.interp1d(x,ev, kind='linear')
        
        self.x=np.array(x)
        self.y=np.array(y)
        self.yEv=np.array(ev)
        self.ky=[]
        self.kyEv=[]
        for i in range(len(x)-1):
            self.ky.append((self.y[i+1]-self.y[i])/(self.x[i+1]-self.x[i]))
            self.kyEv.append((self.yEv[i+1]-self.yEv[i])/(self.x[i+1]-self.x[i]))
        self.ky=np.array(self.ky)
        self.kyEv=np.array(self.kyEv)
        
        return [funSigma, funEv]

    def propertiesApproxSP(self):
        '''аппроксимирующие функции определния характеристик бетона с В10'''
        b=self.b

        if b>10 and b<60:
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
            
                    
            rbn*=(100./9.81)
            rb*=(100./9.81)
            rbtn*=(100./9.81/self.yb)
            rbt*=(100./9.81/self.yb)
            eb*=10000.
            
            self.rbn,self.rb,self.rbtn,self.rbt,eb=rbn,rb,rbtn,rbt,eb
            
            self.ephi()
            return self.rbn, self.rb, self.rbtn, self.rbt, self.eb, self.eb0, self.eb2, self.eb1red, self.ebt0, self.ebt2, self.ebt1red, self.ebl0, self.ebl2, self.ebl1red, self.eblt0, self.eblt2, self.eblt1red, self.phi_crc

    def ephi(self):
        b=self.b
        phi=self.phi
        
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
        
        linMatrB=np.array([10,15,20,25,30,35,40,45,50,55,60,100])
        linMatr75=np.array([2.8,2.4,2.,1.8,1.6,1.5,1.4,1.3,1.2,1.1,1.,1.])    
        linMatr4075=np.array([3.9,3.4,2.8,2.5,2.3,2.1,1.9,1.8,1.6,1.5,1.4,1.4])    
        linMatr40=np.array([5.6,4.8,4.0,3.6,3.2,3.,2.8,2.6,2.4,2.2,2.,2.])   
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
        
        self.eb0, self.eb2, self.eb1red, self.ebt0, self.ebt2, self.ebt1red=eb0, eb2, eb1red, ebt0, ebt2, ebt1red
        self.ebl0, self.ebl2, self.ebl1red, self.eblt0, self.eblt2, self.eblt1red=ebl0, ebl2, ebl1red, eblt0, eblt2, eblt1red
        self.phi_crc=phi_crc


if __name__ == "__main__": 



    rc=Reinforced()
    rc.rn=400
    rc.typ='A'
    print rc.propertiesSP52()
    print rc.propertiesSP63()
    print rc.listSP52()
    print rc.listSP63()
    print rc.propertiesApproxSP()
    
    con=Concrete()
    con.b=25
    print con.propertiesSP52()
    print con.propertiesSP63()
    print con.listSP52()
    print con.listSP63()
    print con.propertiesApproxSP()

