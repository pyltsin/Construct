# -*- coding: utf-8 -*-
"""
Created on Sat Jul 19 22:25:55 2014

@author: Pyltsin
"""

import unittest

from profiles2 import *
from table import *
pi=3.14159265358979

from profiles2 import *

class Test_profile(unittest.TestCase):
    def test_profiles_infile(self):
        el=profiles_infile(files='gost8239_89.csv',number='10', typ='dvut')
        self.assertEquals(el.h(),10.0) 
        print 4 , "test_profiles_infile"

    def test_simple_profiles(self):
        el=profiles_simple(h=20, b=30\
        , s=40, t=50, r1=60, r2=70, a1=80, a2=90, x1=100\
        , x2=110, y1=120, y2=130, r=140, r3=150)
        self.assertEquals(el.h(),20)        
        self.assertEquals(el.b(),30)   
        self.assertEquals(el.s(),40)           
        self.assertEquals(el.t(),50)           
        self.assertEquals(el.r1(),60)   
        self.assertEquals(el.r2(),70)   
        self.assertEquals(el.r3(),150)   
        self.assertEquals(el.a1(),80)   
        self.assertEquals(el.a2(),90)   
        self.assertEquals(el.x1(),100)   
        self.assertEquals(el.x2(),110)   
        self.assertEquals(el.y1(),120)   
        self.assertEquals(el.y2(),130)   
        self.assertEquals(el.r(),140)
        print 5  , "test_simple_profiles"     
        
    def test_rectangle(self):
        el=rectangle(h=20, b=30)
        self.assertEquals(el.h(),20)        
        self.assertEquals(el.b(),30)
        self.assertEquals(el.a(),20*30)
        self.assertEquals(el.jx(),20**3*30/12)
        self.assertEquals(el.jy(),30**3*20/12)
        self.assertEquals(el.s2x(),20/2*20/4*30)
        self.assertEquals(el.s2y(),30/2*30./4*20)
        self.assertEquals(el.sx(5),5.*5/2/4*30)
        self.assertEquals(el.sy(5),5.*5/2/4*20)
        self.assertEquals(el.jxy(),0)
        self.assertLess(abs(el.jxdy(5)-35000)/abs(el.jxdy(5)),0.0000001)
        self.assertLess(abs(el.jydx(5)-60000)/abs(el.jydx(5)),0.0000001) 
#        self.assertLess(abs(el.jxydxdy(5,6)-18000)/abs(el.jxydxdy(5,6)),0.0000001) 
        print 6         , "test_rectangle"           
    def test_quartercircle(self):
        el=quartercircle(r=15)
        self.assertLess(abs(el.a()-15*15*pi/4), 0.00001)
        self.assertLess(abs(el.jx()-0.05489*15**4)/abs(el.jx()),0.001)
        self.assertLess(abs(el.jy()-0.05489*15**4)/abs(el.jx()),0.001)
        self.assertLess(abs(el.xi()-4./3*15/pi),0.00001)
        self.assertLess(abs(el.yi()-4./3*15/pi),0.00001)
        self.assertLess(abs(el.jxy()+0.01646*15**4)/abs(el.jxy()),0.001)
        print 23   , "test_quartercircle"    
    def test_circleangle(self):
        el=circleangle(r=15)
        self.assertLess(abs(el.a()-48.2854)/48.2854, 0.00001)
        self.assertLess(abs(el.xi()-3.3505)/3.3505,0.00001)
        self.assertLess(abs(el.yi()-3.3505)/3.3505,0.00001)
        self.assertLess(abs(el.jx()-381.97783)/abs(el.jx()),0.001)
        self.assertLess(abs(el.jy()-381.97783)/abs(el.jx()),0.001)
        self.assertLess(abs(el.jxy()+224.7080)/abs(el.jxy()),0.001)  
        print 7  ,       "test_circleangle"    
    def test_quartercirclesolid(self):
        el=quartercirclesolid(r=15, r1=10)
        self.assertLess(abs(el.a()-98.1748)/98.1748, 0.00001)
        self.assertLess(abs(el.xi()-6.9361)/6.9361,0.00001)
        self.assertLess(abs(el.yi()-6.9361)/6.9361,0.00001)
        self.assertLess(abs(el.jx()-1592.8845)/abs(el.jx()),0.001)
        self.assertLess(abs(el.jy()-1592.8845)/abs(el.jx()),0.001)
        self.assertLess(abs(el.jxy()+1305.7566)/abs(el.jxy()),0.001)
        print 8       
    def test_anglerectangle(self):
        el=anglerectangle(b=15, h=10)
        self.assertLess(abs(el.a()-15*10/2)/abs(el.a()), 0.00001)
        self.assertLess(abs(el.xi()-5)/abs(el.xi()),0.00001)
        self.assertLess(abs(el.yi()-3.3333)/abs(el.yi()),0.00001)
        self.assertLess(abs(el.jx()-15.*10**3/36)/abs(el.jx()),0.001)
        self.assertLess(abs(el.jy()-15.**3*10/36)/abs(el.jx()),0.001)
        self.assertLess(abs(el.jxy()+15.**2*10**2/72)/abs(el.jxy()),0.001)
        print 9  ,       "test_anglerectangle"         
    def test_solid(self):
        el=solid(r=15)
        self.assertLess(abs(el.a()-15**2*pi)/abs(el.a()), 0.00001)
        self.assertLess(abs(el.xi()-15)/abs(el.xi()),0.00001)
        self.assertLess(abs(el.yi()-15)/abs(el.yi()),0.00001)
        self.assertLess(abs(el.jx()-pi*30**4/64)/abs(el.jx()),0.001)
        self.assertLess(abs(el.jy()-pi*30**4/64)/abs(el.jx()),0.001)
        self.assertEqual(el.jxy(),0)    
        print 10       ,       "test_solid"      
    def test_ring(self):
        el=ring(r=15, r1=10)
        self.assertLess(abs(el.a()-15**2*pi+10**2*pi)/abs(el.a()), 0.00001)
        self.assertLess(abs(el.xi()-15)/abs(el.xi()),0.00001)
        self.assertLess(abs(el.yi()-15)/abs(el.yi()),0.00001)
        self.assertLess(abs(el.jx()-pi*30**4/64*(1-(10./15)**4))/abs(el.jx()),0.001)
        self.assertLess(abs(el.jy()-pi*30**4/64*(1-(10./15)**4))/abs(el.jx()),0.001)
        self.assertEqual(el.jxy(),0) 
        print 11       
    def test_angle(self):
        el=angle(b=10, h=12, x1=3)
        self.assertLess(abs(el.a()-1/2.*10*12)/abs(el.a()), 0.00001)
        self.assertLess(abs(el.xi()-4.3333)/abs(el.xi()),0.00001)
        self.assertLess(abs(el.yi()-4)/abs(el.yi()),0.00001)
        self.assertLess(abs(el.jx()-480)/abs(el.jx()),0.001)
        self.assertLess(abs(el.jy()-263.333)/abs(el.jx()),0.001)
        print 12       
    def test_circleseg(self):
        el=circleseg(a1=pi/6, r=10)
        self.assertLess(abs(el.a()- 9.0586)/abs(el.a()), 0.00001)
        self.assertLess(abs(el.xi()-5)/abs(el.xi()),0.00001)
        self.assertLess(abs(el.yi()-9.1994)/abs(el.yi()),0.00001)
        self.assertLess(abs(el.jx()-1.1183)/abs(el.jx()),0.001)
        self.assertLess(abs(el.jy()-46.0432)/abs(el.jx()),0.001)
        self.assertEqual(el.jxy(),0)  
        print 13       
    def test_krug(self):
        el=krug(a1=pi/6, r=10)
        self.assertLess(abs(el.a()- 5.3751)/abs(el.a()), 0.00001)
        self.assertEqual(el.xi(),0.0000)
        self.assertLess(abs(el.yi()-1.6753)/abs(el.yi()),0.0001)
        self.assertLess(abs(el.jx()- 1.2085)/abs(el.jx()),0.001)
        self.assertLess(abs(el.jy()-14.0974)/abs(el.jx()),0.001)
        self.assertEqual(el.jxy(),0)
        
        print 14       
    def test_rotkrug(self):
        el=rotkrug(a1=pi/6, r=10)
        self.assertLess(abs(el.a()- 5.3751)/abs(el.a()), 0.00001)
        self.assertLess(abs(el.yi()- 1.0491)/abs(el.yi()), 0.0001)
        self.assertLess(abs(el.xi()-0.6057)/abs(el.xi()),0.0001)
        self.assertLess(abs(el.jy()- 10.8752)/abs(el.jy()),0.001)
        self.assertLess(abs(el.jx()-4.4307)/abs(el.jx()),0.001)
        self.assertLess(abs(el.jxy()+5.5811)/abs(el.jxy()),0.001)
        print 15       
    def test_dvut(self):
        el=dvut(h=60, b=19, t=1.78, s=1.2, r1=2, r2=0.8, a1=atan(12./100))
        self.assertLess(abs(el.a()- 137.5384332)/abs(el.a()), 0.0000001)
        self.assertLess(abs(el.jy()- 1724.838581)/abs(el.jy()),0.0000001)
        self.assertLess(abs(el.jx()-76805.76144)/abs(el.jx()),0.0000001)
        self.assertLess(abs(el.s2x()-1490.827914)/abs(el.s2x()),0.0000001)
        self.assertLess(abs(el.ix()-23.6311503)/abs(el.ix()),0.0000001)  
        self.assertLess(abs(el.iy()-3.5412957)/abs(el.iy()),0.0000001) 

        self.assertLess(abs(el.wx()-2560.19204793)/abs(el.wx()),0.0000001)
        self.assertLess(abs(el.wy()-181.56195592)/abs(el.wy()),0.0000001)

        self.assertLess(abs(el.t1()-1.246)/abs(el.t1()),0.0000001)      
        self.assertLess(abs(el.t2()-1.068)/abs(el.t2()),0.0000001) 


        self.assertEqual(el.title(),'dvut')   
        self.assertEqual(el.get_nsigma(),17)  
          
        self.assertLess(abs(el.s2y()-156.051)/abs(el.s2y()),0.00002) 
        
        self.assertLess(abs(el.sy1()-145.25)/abs(el.sy1()),0.00002)

        self.assertLess(abs(el.sx1()-695.471)/abs(el.sx1()),0.00002)

        self.assertLess(abs(el.sx1()-690)/abs(el.sx1()),0.01)
   
        self.assertLess(abs(el.sx2()-995.595417)/abs(el.sx2()),0.00002)

        self.assertLess(abs(el.sx2()-1001.057)/abs(el.sx2()),0.01)

        for i in range(1,18):
#            print i
            self.assertLess(abs((el. get_sigma(nn=i, n=10)-0.07270695))/abs(el. get_sigma(nn=i, n=10)),0.00002)
        for i in range(1, 4):
#            print i
            self.assertLess(abs((el. get_sigma(nn=i, m_x=1000)-0.390595698))/abs(el. get_sigma(nn=i, m_x=1000)),0.00002)

        for i in range(4, 8, 3):
#            print i
#            print el. get_sigma(nn=i, m_x=1000)
            self.assertLess(abs((el. get_sigma(nn=i, m_x=1000)-0.374372957))/abs(el. get_sigma(nn=i, m_x=1000)),0.00002)

        for i in range(5,7):
#            print i

            self.assertLess(abs((el. get_sigma(nn=i, m_x=1000)-0.36046775))/abs(el. get_sigma(nn=i, m_x=1000)),0.00002)


        for i in range(8, 11):
#            print i
            self.assertEqual(abs(el. get_sigma(nn=i, m_x=1000)),0.0000)

        for i in range(11, 15, 3):
#            print i
#            print el. get_sigma(nn=i, m_x=1000)
            self.assertLess(abs((el. get_sigma(nn=i, m_x=1000)+0.374372957))/abs(el. get_sigma(nn=i, m_x=1000)),0.00002)

        for i in range(12,14):
#            print i

            self.assertLess(abs((el. get_sigma(nn=i, m_x=1000)+0.36046775))/abs(el. get_sigma(nn=i, m_x=1000)),0.00002)


        for i in range(15, 18):
#            print i
            self.assertLess(abs((el. get_sigma(nn=i, m_x=1000)+0.390595698))/abs(el. get_sigma(nn=i, m_x=1000)),0.00002)

        for i in (1, 4, 11, 15):
#            print i
            self.assertLess(abs((el. get_sigma(nn=i, m_y=1000)-5.50776177))/abs(el. get_sigma(nn=i, m_y=1000)),0.00002)

        for i in (5,8,12):
#            print i
            self.assertLess(abs((el. get_sigma(nn=i, m_y=1000)-0.347858655))/abs(el. get_sigma(nn=i, m_y=1000)),0.00002)
            

        for i in (2,9,16):
#            print i
            self.assertEqual(el. get_sigma(nn=i, m_y=1000),0.0000)

        for i in (6,10,13):
#            print i
            self.assertLess(abs((el. get_sigma(nn=i, m_y=1000)+0.347858655))/abs(el. get_sigma(nn=i, m_y=1000)),0.00002)


        for i in (3,7,14,17):
#            print i
            self.assertLess(abs((el. get_sigma(nn=i, m_y=1000)+5.50776177))/abs(el. get_sigma(nn=i, m_y=1000)),0.00002)

        for i in (1,2,3,15,16,17):
            self.assertEqual(el.get_tau(nn=i, q_y=1000),0.0000)

        for i in (8,9,10):
            self.assertLess(abs((el. get_tau(nn=i, q_y=1000)-16.1753047))/abs(el. get_tau(nn=i, q_y=1000)),0.00002)

        for i in (4,7,11,14):
            self.assertLess(abs((el. get_tau(nn=i, q_y=1000)-0.476575405))/abs(el. get_tau(nn=i, q_y=1000)),0.00002)

        for i in (5,6,12,13):
            self.assertLess(abs((el. get_tau(nn=i, q_y=1000)-10.80209))/abs(el. get_tau(nn=i, q_y=1000)),0.00002)

        for i in (1,4,11,15,3,7,14,17):
            self.assertEqual(el.get_tau(nn=i, q_x=1000),0.0000)

        for i in (2,9,16):
            self.assertLess(abs((el. get_tau(nn=i, q_x=1000)-1.50788023))/abs(el. get_tau(nn=i, q_x=1000)),0.00002)

        for i in (5,8,12,6,10,13):
            self.assertLess(abs((el. get_tau(nn=i, q_x=1000)-18.1959332))/abs(el. get_tau(nn=i, q_x=1000)),0.00002)
            
        self.assertLess(abs((el.get_sigma_e(nn=i, n=1000, q_x=1000)-32.3436779))/abs(el.get_sigma_e(nn=i, n=1000, q_x=1000)),0.00002)


        self.assertLess(abs(el.wxmin()-2560.19204793)/abs(el.wx()),0.0000001)
        self.assertLess(abs(el.wymin()-181.56195592)/abs(el.wy()),0.0000001)

        self.assertLess(abs(el.hef()-51.8234)/abs(el.hef()),0.000002)
        self.assertLess(abs(el.bef()-7.1383)/abs(el.bef()),0.000002)
        

        self.assertLess(abs(el.aw()-67.73)/abs(el.aw()),0.0002)

        self.assertLess(abs(el.af()-33.82)/abs(el.af()),0.000002)

        self.assertLess(abs(el.afaw()-33.82/67.73)/abs(el.afaw()),0.0002) 
        print 24                  
    def test_dvut2(self):
        el=dvut(h=360., b=130., t=16., s=9.5, r1=14., r2=6., a1=atan(12./100))
        self.assertLess(abs(el.jx()- 15339.998*10**4)/abs(el.jx()),0.001)
#        print(el.jw()/10**6)
        self.assertLess(abs(el.jw()- 146500*10**6)/abs(el.jw()),0.001)

        self.assertLess(abs(el.w(1)- 110.63*100)/abs(el.w(1)),0.021) 
        self.assertLess(abs(el.w(1)- 112.9748*100)/abs(el.w(1)),0.000001)
        self.assertLess(abs(el.w(3)+ 112.9748*100)/abs(el.w(3)),0.000001) 
#        print(el.w(6), el.t2())
        self.assertLess(abs(el.w(5)- 808.41675)/abs(el.w(5)),0.00002) 
        self.assertLess(abs(el.w(6)+808.41675)/abs(el.w(6)),0.00002) 


        
        self.assertLess(abs((el.get_sigma(nn=1, w=10**10)-771.245))/abs(el. get_sigma(nn=1, w=10**10)),0.00002) 

        self.assertLess(abs((el.get_sigma(nn=1, w=10**10, n=100000)-771.245-100000/7380))/abs(el.get_sigma(nn=1, w=10**10, n=100000)),0.001) 


        el2=dvut(h=450, b=150, t=18, s=10.5, r1=16, r2=7, a1=atan(12./100))
#        print(el2.jw()/10**6)        
        self.assertLess(abs(el2.jw()- 398400*10**6)/abs(el2.jw()),0.001)
        


        el3=dvut(h=240, b=110, t=14, s=8.2, r1=10.5, r2=4, a1=atan(12./100))        

#        print el3.jt()
        self.assertLess(abs(el3.jt()-31.22*10**4)/abs(el3.jt()),0.005)   

        print 16                 
    def test_function(self):
        self.assertEqual(jxdx(5,6,7),299)      
        self.assertLess((jda(11.25, 31.25, 0, 45./180*pi)[0]-21.25)/21.25,0.00002)          
        self.assertLess((jda(11.25, 31.25, 0, 45./180*pi)[1]-21.25)/21.25,0.00002)
        self.assertLess((jda(11.25, 31.25, 0, 45./180*pi)[2]-10.)/10.,0.00002)
        print 17               
#         self.assertLess(abs(el.get_sigma_e()-3.5412957)/abs(el.get_sigma_e()),0.0000001)        

        
if __name__ == "__main__":
    unittest.main()
    
    