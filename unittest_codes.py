# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 10:52:37 2013

@author: puma
"""
import unittest

from profiles2 import *
from table import *
pi=3.14159265358979


from  PyQt4 import QtCore
from steel import *

from codes import * 

import basa_sort          

class Test_mat(unittest.TestCase):
    def test_mat_steel_new1(self):
        el=dvut(h=400., b=130., t=11., s=9.5, r1=14., r2=6., a1=atan(12./100))
        s=steel_snip20107n('C245',el)
        self.assertLess(abs(s.ry()-2446.5)/2446.5,0.00002)          
        self.assertLess(abs(s.ryn()-2497.45)/2497.45,0.00002)
        self.assertLess(abs(s.ru()-3669.72)/3669.72,0.00002)          
        self.assertLess(abs(s.run()-3771.66)/3771.66,0.00002) 
        self.assertLess(abs(s.rs()-1418.97)/1418.97,0.00002) 
        self.assertLess(abs(s.rth()-1834.86)/1834.86,0.00002)
        self.assertLess(abs(s.rthf()-1223.25)/1223.25,0.00002) 
        self.assertLess(abs(s.mu()-0.3)/0.3,0.00002) 
        self.assertLess(abs(s.e()-2.0999*10**6)/(2.0999*10**6),0.00002)  
        print 1   

    def test_mat_steel_new2(self):
        el=dvut(h=400., b=130., t=2.5, s=9.5, r1=14., r2=6., a1=atan(12./100))
        s=steel_snip20107n('C245',el, dim=1)
        ryn=235*100/9.81
        ry=230*100/9.81
        run=370*100/9.81
        ru=360*100/9.81

        self.assertLess(abs(s.ry()-ry)/ry,0.00002)          
        self.assertLess(abs(s.ryn()-ryn)/ryn,0.00002)
        self.assertLess(abs(s.ru()-ru)/ru,0.00002)          
        self.assertLess(abs(s.run()-run)/run,0.00002) 
        self.assertLess(abs(s.mu()-0.3)/0.3,0.00002) 
        self.assertLess(abs(s.e()-2.0999*10**6)/(2.0999*10**6),0.00002)  
        print 2  

    def test_mat_steel_old1(self):
        el=dvut(h=400., b=130., t=11., s=9.5, r1=14., r2=6., a1=atan(12./100))
        s=steel_snip1987('C235',el)

        ryn=235*100/9.81
        ry=230*100/9.81
        run=360*100/9.81
        ru=350*100/9.81
        rs=0.58*ry
        rth=0.5*ru
        rthf=0.5*ry     
        
        self.assertLess(abs(s.ry()-ry)/ry,0.00002)          
        self.assertLess(abs(s.ryn()-ryn)/ryn,0.00002)
        self.assertLess(abs(s.ru()-ru)/ru,0.00002)          
        self.assertLess(abs(s.run()-run)/run,0.00002) 
        self.assertLess(abs(s.rs()-rs)/rs,0.00002) 
        self.assertLess(abs(s.rth()-rth)/rth,0.00002)
        self.assertLess(abs(s.rthf()-rthf)/rthf,0.00002) 
        self.assertLess(abs(s.mu()-0.3)/0.3,0.00002) 
        self.assertLess(abs(s.e()-2.0999*10**6)/(2.0999*10**6),0.00002)  
        print 3   

    def test_mat_steel_old2(self):
        el=dvut(h=400., b=130., t=4.1, s=9.5, r1=14., r2=6., a1=atan(12./100))
        s=steel_snip1987('C235',el, dim=1, typ_steel='list')
        
        ryn=215*100/9.81
        ry=210*100/9.81
        run=360*100/9.81
        ru=350*100/9.81

        self.assertLess(abs(s.ry()-ry)/ry,0.00002)          
        self.assertLess(abs(s.ryn()-ryn)/ryn,0.00002)
        self.assertLess(abs(s.ru()-ru)/ru,0.00002)          
        self.assertLess(abs(s.run()-run)/run,0.00002) 
        self.assertLess(abs(s.mu()-0.3)/0.3,0.00002) 
        self.assertLess(abs(s.e()-2.0999*10**6)/(2.0999*10**6),0.00002)  
        print 4  
    def test_mat_steel_old3(self):

        ryn=235*100/9.81
        ry=230*100/9.81
        run=360*100/9.81
        ru=350*100/9.81
        rs=0.58*ry
        rth=0.5*ru
        rthf=0.5*ry  
        s=steel_general(230,235,350,360)
        self.assertLess(abs(s.ry()-ry)/ry,0.00002)          
        self.assertLess(abs(s.ryn()-ryn)/ryn,0.00002)
        self.assertLess(abs(s.ru()-ru)/ru,0.00002)          
        self.assertLess(abs(s.run()-run)/run,0.00002) 
        self.assertLess(abs(s.rs()-rs)/rs,0.00002) 
        self.assertLess(abs(s.rth()-rth)/rth,0.00002)
        self.assertLess(abs(s.rthf()-rthf)/rthf,0.00002) 
        self.assertLess(abs(s.mu()-0.3)/0.3,0.00002) 
        self.assertLess(abs(s.e()-2.0999*10**6)/(2.0999*10**6),0.00002)  
        print 5   

    def test_mat_steel_old4(self):

        el=dvut(h=400., b=130., t=11., s=9.5, r1=14., r2=6., a1=atan(12./100))
        s=steel_snip1987('C245',el)
        self.assertLess(abs(s.ry()-2446.5)/2446.5,0.00002)          
        self.assertLess(abs(s.ryn()-2497.45)/2497.45,0.00002)
        self.assertLess(abs(s.ru()-3669.72)/3669.72,0.00002)          
        self.assertLess(abs(s.run()-3771.66)/3771.66,0.00002) 
        self.assertLess(abs(s.rs()-1418.97)/1418.97,0.00002) 
        self.assertLess(abs(s.rth()-1834.86)/1834.86,0.00002)
        self.assertLess(abs(s.rthf()-1223.25)/1223.25,0.00002) 
        self.assertLess(abs(s.mu()-0.3)/0.3,0.00002) 
        self.assertLess(abs(s.e()-2.0999*10**6)/(2.0999*10**6),0.00002)  

        s=steel_snip1987('C345',el)
        self.assertLess(abs(s.ry()-315/9.81*100)/2446.5,0.00002)          
        self.assertLess(abs(s.ryn()-325/9.81*100)/2497.45,0.00002)
        self.assertLess(abs(s.ru()-460/9.81*100)/3669.72,0.00002)          
        self.assertLess(abs(s.run()-470/9.81*100)/3771.66,0.00002) 

        self.assertLess(abs(s.mu()-0.3)/0.3,0.00002) 
        self.assertLess(abs(s.e()-2.0999*10**6)/(2.0999*10**6),0.00002)

        el=dvut(h=400., b=130., t=61., s=9.5, r1=14., r2=6., a1=atan(12./100))
        s=steel_snip1987('C345',el, typ_steel='list')
        self.assertLess(abs(s.ry()-270/9.81*100)/2446.5,0.00002)          
        self.assertLess(abs(s.ryn()-275/9.81*100)/2497.45,0.00002)
        self.assertLess(abs(s.ru()-430/9.81*100)/3669.72,0.00002)          
        self.assertLess(abs(s.run()-440/9.81*100)/3771.66,0.00002) 

        self.assertLess(abs(s.mu()-0.3)/0.3,0.00002) 
        self.assertLess(abs(s.e()-2.0999*10**6)/(2.0999*10**6),0.00002)
        print 6   
        

class Test_code(unittest.TestCase):
    def test_elements(self):    
        pr=dvut(h=600, b=190, t=17.8, s=12., r1=20., r2=08., a1=atan(12./100))
        s=steel_snip20107n('C245',pr)
        el=elements(s, pr, mux=100, muy=200, mub=300, lfact=10, br=1, hr=2) 
        
        self.assertEqual(el.lx(),1000)
        self.assertEqual(el.ly(),2000)
        self.assertEqual(el.lb(),3000)
        self.assertEqual(el.lfact(),10)
        self.assertEqual(el.br(),1)
        self.assertEqual(el.hr(),2)
#        print el.profile.ix()

        self.assertLess(abs(el.lambdax()-4.23170259)/4.23170259,0.00002) 
        self.assertLess(abs(el.lambday()-56.4765)/56.4765,0.00002) 
#        print (el.lambdax_())
        self.assertLess(abs(el.lambdax_()-0.14454)/0.14454,0.001) 
        self.assertLess(abs(el.lambday_()-1.9291)/1.9291,0.001)
        print 7       
    def test_force(self):
        forc=force(n=10, mx=20, my=30, w=40, qx=50, qy=60, t=70, sr=80, floc=90)
        self.assertEqual(forc.n,10)
        self.assertEqual(forc.mx,20)
        self.assertEqual(forc.my,30)
        self.assertEqual(forc.w,40)
        self.assertEqual(forc.qx,50)
        self.assertEqual(forc.qy,60)
        self.assertEqual(forc.t,70)
        self.assertEqual(forc.sr,80)
        self.assertEqual(forc.floc,90)  
        print 8   

class Test_code_ferma(unittest.TestCase):
    def test_yc(self):
        pr=dvut(h=420, b=400, t=20, s=9, r1=0, r2=0, a1=0)
        s=steel_snip20107n('C245',pr)
        el=elements(s, pr) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.yc()

        self.assertEqual(test,1) 

        sol=snipn(el,forc,[1, 0.95], 0.8)

        self.assertEqual(sol.yc1(),1) 
        self.assertEqual(sol.yc2(),0.95) 
        self.assertEqual(sol.ycb(),0.8) 


        print 9   
        
    def test_yu(self):
        pr=dvut(h=420, b=400, t=20, s=9, r1=0, r2=0, a1=0)
        s=steel_snip20107n('C245',pr)
        el=elements(s, pr) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.yu()
        
        self.assertEqual(test,1.3) 
        print 10   

    def test_phi_n1(self):
#двутавры        
        pr1=dvut(h=40, b=40, t=2, s=2, r1=0, r2=0, a1=0)
        s=steel_snip20107n('C255',pr1)
        el=elements(s, pr1, mux=1, muy=1, mub=1, lfact=500) 
        forc=force(n=800*1000/9.81, mx=435*1000/9.81*100, my=435*1000/9.81*100)        
        sol=snipn(el,forc,1)

        self.assertLess(abs(sol.phix()[0]-0.946)/0.946,0.001) 
        self.assertLess(abs(sol.phiy()[0]-0.8579)/0.8579,0.001)

        pr=dvut(h=420, b=400, t=20, s=9, r1=0, r2=0, a1=0)
        s=steel_snip20107n('C245',pr)
        el=elements(s, pr, mux=1, muy=1, mub=1,  lfact=7000) 
        forc=force()        
        sol=snipn(el,forc,1)

        self.assertLess(abs(sol.phiy()[0]-0.781)/0.781,0.0001)  
        self.assertLess(abs(sol.phi()-0.781)/0.781,0.0001)
   
        self.assertLess(abs(sol.phix()[0]-0.919)/0.919,0.0001)                  

        pr1=dvut(h=520, b=400, t=20, s=9, r1=0, r2=0, a1=0)
        s=steel_snip20107n('C245',pr1)
        el=elements(s, pr1, mux=35000./3000, muy=7000./3000,mub=1, lfact=3000) 
        forc=force()        
        sol=snipn(el,forc,1)

        self.assertLess(abs(sol.phi()-0.28394)/0.28394,0.0001)


        pr1=dvut(h=520, b=400, t=20, s=9, r1=0, r2=0, a1=0)
        s=steel_snip20107n('C245',pr1)
        el=elements(s, pr1, mux=7000, muy=700,mub=1, lfact=1) 
        forc=force()        
        sol=snipn(el,forc,1)
        self.assertLess(abs(sol.phi()-0.9654)/0.9654,0.0001)

        print 11   

    def test_phi_n2(self):
#короб
        pr1=truba_pryam(h=500, b=400, t=20, r1=0, r2=0)
        s=steel_snip20107n('C245',pr1)
        el=elements(s, pr1, mux=35000./3000, muy=7000./3000,mub=1, lfact=3000) 
        forc=force()        
        sol=snipn(el,forc,1)

        self.assertLess(abs(sol.phi_n(4.)[0]-0.475)/0.475,0.0001)
        
        self.assertLess(abs(sol.phi_n(5.)[0]-0.304)/0.304,0.0001)

        self.assertLess(abs(sol.phi_n(3.)[0]-0.704)/0.704,0.001)

#ugol_tavr_st_up
        pr1=sost_ugol_tavr_st_up(h=500, b=400, t=20, r1=0, r2=0)
        s=steel_snip20107n('C245',pr1)
        el=elements(s, pr1, mux=35000./3000, muy=7000./3000,mub=1, lfact=3000) 
        forc=force()        
        sol=snipn(el,forc,1)
        
        self.assertLess(abs(sol.phi_n(4.)[0]-0.4016)/0.4016,0.001)
        
        self.assertLess(abs(sol.phi_n(5.)[0]-0.289)/0.289,0.001)

        self.assertLess(abs(sol.phi_n(3.)[0]-0.562)/0.562,0.001)

#ugol_tavr_st_right

        pr1=sost_ugol_tavr_st_right(h=500, b=400, t=20, r1=0, r2=0)
        s=steel_snip20107n('C245',pr1)
        el=elements(s, pr1, mux=35000./3000, muy=7000./3000,mub=1, lfact=3000) 
        forc=force()        
        sol=snipn(el,forc,1)
        
        self.assertLess(abs(sol.phi_n(4.)[0]-0.4016)/0.4016,0.001)
        
        self.assertLess(abs(sol.phi_n(5.)[0]-0.289)/0.289,0.001)

        self.assertLess(abs(sol.phi_n(3.)[0]-0.562)/0.562,0.001)

#ugol_tavr_st_krest

        pr1=sost_ugol_tavr_st_krest(h=500, b=400, t=20, r1=0, r2=0)
        s=steel_snip20107n('C245',pr1)
        el=elements(s, pr1, mux=35000./3000, muy=7000./3000,mub=1, lfact=3000) 
        forc=force()        
        sol=snipn(el,forc,1)

        
        self.assertLess(abs(sol.phi_n(4.)[0]-0.453)/0.453,0.001)
        
        self.assertLess(abs(sol.phi_n(5.)[0]-0.304)/0.304,0.001)

        self.assertLess(abs(sol.phi_n(3.)[0]-0.643)/0.643,0.001)



        print 12
        
    def test_phi_n_old1(self):
        pr1=truba_pryam(h=500, b=400, t=5, r1=0, r2=0)
        s=steel_snip20107n('C245',pr1)
        el=elements(s, pr1, mux=35000./3000, muy=7000./3000,mub=1, lfact=3000) 
        forc=force()        
        sol=snipn(el,forc,1)

        self.assertLess(abs(sol.phi_n_old(2.)-0.812)/0.812,0.001)

        self.assertLess(abs(sol.phi_n_old(4.)-0.435)/0.435,0.001)
        
        self.assertLess(abs(sol.phi_n_old(5.)-0.2887)/0.2887,0.001)

        print 13

    def test_phi_n_old2(self):
        pr1=truba_pryam(h=10, b=6, t=0.6, r1=0.6, r2=1.2)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=0.7, muy=1,mub=1, lfact=300) 
        forc=force()        
        sol=snipn(el,forc,1)

        self.assertLess(abs(sol.phix_old()-0.81)/0.81,0.001)

        self.assertLess(abs(sol.phiy_old()-0.385)/0.385,0.0013)
        
        self.assertLess(abs(sol.phi_old()-0.385)/0.385,0.0013)

        print 14

    def test_q_fic(self):
        pr1=truba_pryam(h=10, b=6, t=0.6, r1=0.6, r2=1.2)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=0.7, muy=1,mub=1, lfact=300) 
        forc=force()        
        sol=snipn(el,forc,1)

        self.assertLess(abs(sol.q_fic(500., 0.5)-10.25)/10.25,0.001)
        self.assertLess(abs(sol.q_fic_old(500., 0.5)-10.25)/10.25,0.001)


        print 15

    def test_local_buckle_h1(self):
#двутавр
        pr=dvut(h=420, b=400, t=20, s=9, r1=0, r2=0, a1=0)
        s=steel_snip20107n('C245',pr)
        el=elements(s, pr, mux=1, muy=1, lfact=7000) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_h_n()
    
        self.assertLess(abs(test[0]-1.44/1.9979)/(1.44/1.9979),0.001)  
        self.assertLess(abs(test[1]-1.997905)/1.997905,0.0001)        
        self.assertLess(abs(test[2]-1.44116298)/1.44116298,0.0001)   

        el2=elements(s, pr,  mux=210000, muy=7000, lfact=1)  
        sol2=snipn(el2,forc,1)      
        test=sol2.local_buckl_h_n()
        self.assertLess(abs(test[1]-2.3)/2.3,0.0001)        


        el2=elements(s, pr, mux=7000, muy=5000, lfact=1)  
        sol2=snipn(el2,forc,1)      
        test=sol2.local_buckl_h_n()
        self.assertLess(abs(test[1]-1.6975)/1.6975,0.0001) 

        print 16        


    def test_local_buckle_h2(self):
#короб
        pr1=truba_pryam(h=10, b=6, t=0.6, r1=0.6, r2=1.2)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=1, muy=1, lfact=300) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_h_n()
#        print test
        self.assertLess(abs(test[0]-0.2645)/(0.2645),0.001)  
        self.assertLess(abs(test[1]-1.6)/1.6,0.0001)        
        self.assertLess(abs(test[2]-0.4232)/0.4232,0.001)   

        el2=elements(s, pr1, mux=1, muy=1, lfact=100) 
        sol2=snipn(el2,forc,1)      
        test=sol2.local_buckl_h_n()
        self.assertLess(abs(test[1]-1.287)/1.287,0.0001)        


        el3=elements(s, pr1, mux=1, muy=1, lfact=30) 
        sol2=snipn(el3,forc,1)      
        test=sol2.local_buckl_h_n()
        self.assertLess(abs(test[1]-1.2)/1.2,0.0001) 

        print 17        

    def test_local_buckle_h3(self):
#все, что сделано из уголков
        pr1=sost_ugol_tavr_st_up(h=20, b=10, t=1, r1=0, r2=0, r3=0, dx=1)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=1, muy=1, lfact=300) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_h_n()
#        print test
        self.assertLess(abs(test[0]-1.08)/(1.08),0.001)  
        self.assertLess(abs(test[1]-0.58744)/0.58744,0.0001)        
        self.assertLess(abs(test[2]-0.635)/0.635,0.001)   

        el2=elements(s, pr1, mux=1, muy=1, lfact=3000) 
        sol=snipn(el2,forc,1)
        test=sol.local_buckl_h_n()
        self.assertLess(abs(test[1]-0.68)/0.68,0.0001)        


        el3=elements(s, pr1, mux=1, muy=1, lfact=30) 
        sol=snipn(el3,forc,1)
        test=sol.local_buckl_h_n()
        self.assertLess(abs(test[1]-0.456)/0.456,0.0001)        

        pr1=sost_ugol_tavr_st_right(h=20, b=10, t=1, r1=0, r2=0, r3=0, dx=1)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=1, muy=1, lfact=300) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_h_n()
#        print test

        self.assertLess(abs(test[1]-0.656)/0.656,0.001)        

        pr1=sost_ugol_tavr_st_krest(h=10, b=10, t=1, r1=0, r2=0, r3=0, dx=1, dy=1)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=1, muy=1, lfact=300) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_h_n()
        self.assertLess(abs(test[1]-0.554)/0.554,0.001)        


        print 18   
        
    def test_local_buckle_h_old1(self):
#двутавр
        pr=dvut(h=420, b=400, t=20, s=9, r1=0, r2=0, a1=0)
        s=steel_snip20107n('C245',pr)
        el=elements(s, pr, mux=1, muy=1, lfact=7000) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_h_n_old()
    
        self.assertLess(abs(test[0]-1.44/1.9979)/(1.44/1.9979),0.001)  
        self.assertLess(abs(test[1]-1.997905)/1.997905,0.0001)        
        self.assertLess(abs(test[2]-1.44116298)/1.44116298,0.0001)   

        el2=elements(s, pr,  mux=210000, muy=7000, lfact=1)  
        sol2=snipn(el2,forc,1)      
        test=sol2.local_buckl_h_n_old()
        self.assertLess(abs(test[1]-2.3)/2.3,0.0001)        


        el2=elements(s, pr, mux=7000, muy=5000, lfact=1)  
        sol2=snipn(el2,forc,1)      
        test=sol2.local_buckl_h_n_old()
        self.assertLess(abs(test[1]-1.6975)/1.6975,0.0001) 

        print 19        


    def test_local_buckle_h_old2(self):
#короб
        pr1=truba_pryam(h=10, b=6, t=0.6, r1=0.6, r2=1.2)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=1, muy=1, lfact=300) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_h_n_old()
#        print test
        self.assertLess(abs(test[0]-0.2645)/(0.2645),0.001)  
        self.assertLess(abs(test[1]-1.6)/1.6,0.0001)        
        self.assertLess(abs(test[2]-0.4232)/0.4232,0.001)   

        el2=elements(s, pr1, mux=1, muy=1, lfact=100) 
        sol2=snipn(el2,forc,1)      
        test=sol2.local_buckl_h_n_old()
        self.assertLess(abs(test[1]-1.287)/1.287,0.0001)        


        el3=elements(s, pr1, mux=1, muy=1, lfact=30) 
        sol2=snipn(el3,forc,1)      
        test=sol2.local_buckl_h_n_old()
        self.assertLess(abs(test[1]-1.2)/1.2,0.0001) 

        s=steel_snip20107n('C345',pr1, 1)
        el=elements(s, pr1, mux=5000, muy=300, lfact=1) 
        forc=force(n=200*1000/9.81, mx=100*1000/9.81*100, my=000*1000/9.81*100, qx=500*1000/9.81)        
        sol=snipn(el,forc,1)
        
        self.assertLess(abs(sol.local_buckl_h_n_old()[1]-1.6)/1.6,0.001)    

#        print sol.local_buckl_h_n()[2]     


        print 20        

    def test_local_buckl_h_old3(self):
#все, что сделано из уголков
        pr1=sost_ugol_tavr_st_up(h=20, b=10, t=1, r1=0, r2=0, r3=0, dx=1)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=1, muy=1, lfact=300) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_h_n_old()
#        print test
        self.assertLess(abs(test[0]-1.08)/(1.08),0.001)  
        self.assertLess(abs(test[1]-0.58744)/0.58744,0.0001)        
        self.assertLess(abs(test[2]-0.635)/0.635,0.001)   

        el2=elements(s, pr1, mux=1, muy=1, lfact=3000) 
        sol=snipn(el2,forc,1)
        test=sol.local_buckl_h_n_old()
        self.assertLess(abs(test[1]-0.68)/0.68,0.0001)        


        el3=elements(s, pr1, mux=1, muy=1, lfact=30) 
        sol=snipn(el3,forc,1)
        test=sol.local_buckl_h_n_old()
        self.assertLess(abs(test[1]-0.456)/0.456,0.0001)        

        pr1=sost_ugol_tavr_st_right(h=20, b=10, t=1, r1=0, r2=0, r3=0, dx=1)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=1, muy=1, lfact=300) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_h_n_old()
#        print test

        self.assertLess(abs(test[1]-0.656)/0.656,0.001)        

        pr1=sost_ugol_tavr_st_krest(h=10, b=10, t=1, r1=0, r2=0, r3=0, dx=1, dy=1)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=1, muy=1, lfact=300) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_h_n_old()
        self.assertLess(abs(test[1]-0.554)/0.554,0.001)        


        print 21   

    def test_local_buckl_b1(self):
#двутавр
        pr=dvut(h=420, b=400, t=20, s=9, r1=0, r2=0, a1=0)
        s=steel_snip20107n('C245',pr)
        el=elements(s, pr, mux=7000, muy=7000, lfact=1) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_b_n()

        self.assertLess(abs(test[1]-0.5879)/0.5879,0.0001)        
        self.assertLess(abs(test[2]-0.333615248)/0.333615248,0.0001)        


        pr1=dvut(h=42.0, b=40.0, t=0.4, s=.9, r1=0, r2=0, a1=0)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=1000, muy=1000, lfact=1) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_b_n()
        self.assertLess(abs(test[2]-1.63)/1.63,0.002)        

        self.assertLess(abs(test[1]-0.76)/0.76,0.001)        
        self.assertLess(abs(test[0]-2.1488)/2.1488,0.001)        

        pr1=dvut(h=42.0, b=40.0, t=4.0, s=.9, r1=0, r2=0, a1=0)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=1, muy=1, lfact=1) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_b_n()
        self.assertLess(abs(test[1]-0.44)/0.44,0.001)        


        pr1=dvut(h=42.0, b=40.0, t=0.4, s=.9, r1=0, r2=0, a1=0)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=300, muy=300, lfact=1) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_b_n()
#        print test
        self.assertLess(abs(test[1]-0.4875)/0.4875,0.001)        



        print 22   


    def test_local_buckl_b2(self):
#короб        
        pr1=truba_pryam(h=8,b=12,t=0.6, r2=1.2, r1=0.6)

        s=steel_snip20107n('C345',pr1, 1)
        el=elements(s, pr1, mux=300, muy=5000, lfact=1) 
        forc=force(n=200*1000/9.81, mx=100*1000/9.81*100, my=000*1000/9.81*100, qx=500*1000/9.81)        
        sol=snipn(el,forc,1)
        
        self.assertLess(abs(sol.local_buckl_b_n()[1]-1.6)/1.6,0.001)    

#        print sol.local_buckl_h_n()[2]     
        self.assertLess(abs(sol.local_buckl_b_n()[2]-0.6306)/0.6306,0.001) 

        s=steel_snip20107n('C345',pr1, 1)
        el=elements(s, pr1, mux=3, muy=50, lfact=1) 
        forc=force(n=200*1000/9.81, mx=100*1000/9.81*100, my=000*1000/9.81*100, qx=500*1000/9.81)        
        sol=snipn(el,forc,1)

        self.assertLess(abs(sol.local_buckl_b_n()[1]-1.2)/1.2,0.001)    

#        print sol.local_buckl_h_n()[2]     
        self.assertLess(abs(sol.local_buckl_b_n()[2]-0.6306)/0.6306,0.001)

        pr1=truba_pryam(h=12,b=10,t=1, r2=0, r1=0)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=300, muy=300, lfact=1) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_b_n()

        self.assertLess(abs(test[1]-1.456)/1.456,0.001)        
        self.assertLess(abs(test[2]-0.2673)/0.2673,0.001)        


        pr1=truba_pryam(h=12,b=10,t=1, r2=0, r1=0)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=3000, muy=3000, lfact=1) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_b_n()

        self.assertLess(abs(test[1]-1.6)/1.6,0.001)        


        pr1=truba_pryam(h=12,b=10,t=1, r2=0, r1=0)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=30, muy=30, lfact=1) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_b_n()

        self.assertLess(abs(test[1]-1.2)/1.2,0.001)        



        print 23   

    def test_local_buckle_b3(self):
#все, что сделано из уголков
        pr1=sost_ugol_tavr_st_up(h=20, b=10, t=1, r1=0, r2=0, r3=0, dx=1)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=1, muy=1, lfact=300) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_b_n()
#        print test
        self.assertLess(abs(test[0]-0.511)/(0.511),0.002)  
        self.assertLess(abs(test[1]-0.58744)/0.58744,0.0001)        
        self.assertLess(abs(test[2]-0.3)/0.3,0.003)   

        el2=elements(s, pr1, mux=1, muy=1, lfact=3000) 
        sol=snipn(el2,forc,1)
        test=sol.local_buckl_b_n()
        self.assertLess(abs(test[1]-0.68)/0.68,0.0001)        


        el3=elements(s, pr1, mux=1, muy=1, lfact=30) 
        sol=snipn(el3,forc,1)
        test=sol.local_buckl_b_n()
        self.assertLess(abs(test[1]-0.456)/0.456,0.0001)        

        pr1=sost_ugol_tavr_st_right(h=20, b=10, t=1, r1=0, r2=0, r3=0, dx=1)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=1, muy=1, lfact=300) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_b_n()
#        print test

        self.assertLess(abs(test[1]-0.656)/0.656,0.001)        

        pr1=sost_ugol_tavr_st_krest(h=10, b=10, t=1, r1=0, r2=0, r3=0, dx=1, dy=1)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=1, muy=1, lfact=300) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_b_n()
        self.assertLess(abs(test[1]-0.554)/0.554,0.001)        


        print 24   

    def test_local_buckl_b_old1(self):
#двутавр
        pr=dvut(h=420, b=400, t=20, s=9, r1=0, r2=0, a1=0)
        s=steel_snip20107n('C245',pr)
        el=elements(s, pr, mux=7000, muy=7000, lfact=1) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_b_n_old()

        self.assertLess(abs(test[1]-0.5879)/0.5879,0.0001)        
        self.assertLess(abs(test[2]-0.333615248)/0.333615248,0.0001)        


        pr1=dvut(h=42.0, b=40.0, t=0.4, s=.9, r1=0, r2=0, a1=0)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=1000, muy=1000, lfact=1) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_b_n_old()
        self.assertLess(abs(test[2]-1.63)/1.63,0.002)        

        self.assertLess(abs(test[1]-0.76)/0.76,0.001)        
        self.assertLess(abs(test[0]-2.1488)/2.1488,0.001)        

        pr1=dvut(h=42.0, b=40.0, t=4.0, s=.9, r1=0, r2=0, a1=0)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=1, muy=1, lfact=1) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_b_n_old()
        self.assertLess(abs(test[1]-0.44)/0.44,0.001)        


        pr1=dvut(h=42.0, b=40.0, t=0.4, s=.9, r1=0, r2=0, a1=0)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=300, muy=300, lfact=1) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_b_n_old()
#        print test
        self.assertLess(abs(test[1]-0.4875)/0.4875,0.001)        



        print 25   


    def test_local_buckl_b_old2(self):
#короб        
        pr1=truba_pryam(h=8,b=12,t=0.6, r2=1.2, r1=0.6)

        s=steel_snip20107n('C345',pr1, 1)
        el=elements(s, pr1, mux=300, muy=5000, lfact=1) 
        forc=force(n=200*1000/9.81, mx=100*1000/9.81*100, my=000*1000/9.81*100, qx=500*1000/9.81)        
        sol=snipn(el,forc,1)
        
        self.assertLess(abs(sol.local_buckl_b_n_old()[1]-1.6)/1.6,0.001)    

#        print sol.local_buckl_h_n()[2]     
        self.assertLess(abs(sol.local_buckl_b_n_old()[2]-0.6306)/0.6306,0.001) 

        s=steel_snip20107n('C345',pr1, 1)
        el=elements(s, pr1, mux=3, muy=50, lfact=1) 
        forc=force(n=200*1000/9.81, mx=100*1000/9.81*100, my=000*1000/9.81*100, qx=500*1000/9.81)        
        sol=snipn(el,forc,1)

        self.assertLess(abs(sol.local_buckl_b_n_old()[1]-1.2)/1.2,0.001)    

#        print sol.local_buckl_h_n()[2]     
        self.assertLess(abs(sol.local_buckl_b_n_old()[2]-0.6306)/0.6306,0.001)

        pr1=truba_pryam(h=12,b=10,t=1, r2=0, r1=0)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=300, muy=300, lfact=1) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_b_n_old()

        self.assertLess(abs(test[1]-1.456)/1.456,0.001)        
        self.assertLess(abs(test[2]-0.2673)/0.2673,0.001)        


        pr1=truba_pryam(h=12,b=10,t=1, r2=0, r1=0)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=3000, muy=3000, lfact=1) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_b_n_old()

        self.assertLess(abs(test[1]-1.6)/1.6,0.001)        


        pr1=truba_pryam(h=12,b=10,t=1, r2=0, r1=0)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=30, muy=30, lfact=1) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_b_n_old()

        self.assertLess(abs(test[1]-1.2)/1.2,0.001)        



        print 26   

    def test_local_buckle_b_old3(self):
#все, что сделано из уголков
        pr1=sost_ugol_tavr_st_up(h=20, b=10, t=1, r1=0, r2=0, r3=0, dx=1)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=1, muy=1, lfact=300) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_b_n_old()
#        print test
        self.assertLess(abs(test[0]-0.511)/(0.511),0.002)  
        self.assertLess(abs(test[1]-0.58744)/0.58744,0.0001)        
        self.assertLess(abs(test[2]-0.3)/0.3,0.003)   

        el2=elements(s, pr1, mux=1, muy=1, lfact=3000) 
        sol=snipn(el2,forc,1)
        test=sol.local_buckl_b_n()
        self.assertLess(abs(test[1]-0.68)/0.68,0.0001)        


        el3=elements(s, pr1, mux=1, muy=1, lfact=30) 
        sol=snipn(el3,forc,1)
        test=sol.local_buckl_b_n_old()
        self.assertLess(abs(test[1]-0.456)/0.456,0.0001)        

        pr1=sost_ugol_tavr_st_right(h=20, b=10, t=1, r1=0, r2=0, r3=0, dx=1)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=1, muy=1, lfact=300) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_b_n_old()
#        print test

        self.assertLess(abs(test[1]-0.656)/0.656,0.001)        

        pr1=sost_ugol_tavr_st_krest(h=10, b=10, t=1, r1=0, r2=0, r3=0, dx=1, dy=1)
        s=steel_snip1987('C235',pr1, dim=1)
        el=elements(s, pr1, mux=1, muy=1, lfact=300) 
        forc=force()        
        sol=snipn(el,forc,1)
        test=sol.local_buckl_b_n_old()
        self.assertLess(abs(test[1]-0.554)/0.554,0.001)        

        print 27   
        
    def test_basasort_output_simple_ferm(self):
        
        basa=basa_sort.BasaSort()

        code=QtCore.QString(u'СНиП II-23-81*')
        type_element=QtCore.QString(u'Ферма')
        typ_sec=QtCore.QString(u'Двутавр')
        gost=QtCore.QString(u"СТО АСЧМ 20-93 (К) Двутавры с параллельными полками")
        num_sect=QtCore.QString(u'40 К1')
        stl=QtCore.QString(u'C345')
        inp=[1,1,300,3,2]        
        check=basa.output_simple(code, type_element, typ_sec, gost, num_sect, stl, inp) 

        ry=315*100/9.81
        a=186.8
        phix=0.813
        phiy=0.77
        ru=460*100/9.81
        e=2.1*10**6
#дальше подряд все 24 штуки - проверка по старому снип
        un=check[0][0]
        res=phiy*ry*a
        self.assertLess(abs(un-res)/res,0.001)        


        un=check[1][0]
        res=ry*a
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[2][0]
        res=0.554
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[3][0]
        res=phix
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[4][0]
        res=phiy
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[5][0]
        res=ry*a
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[6][0]
        res=ru*a/1.3
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[7][0]
        res=14093.9/9.81*1000
        self.assertLess(abs(un-res)/res,0.002)        

        un=check[8][0]
        res=10685/9.81*1000
        self.assertLess(abs(un-res)/res,0.001)        


        un=check[9][0]
        res=phiy*ry*a/phix*7.15*10**(-6)*(2330-e/ry)
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[10][0]
        res=phiy*ry*a/phiy*7.15*10**(-6)*(2330-e/ry)
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[11][0]
        res=u'-'
        self.assertEqual(un, res)        

        un=check[12][0]
        res=u'-'
        self.assertEqual(un, res)        

        un=check[13][0]
        res=1.3
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[14][0]
        res=ry
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[15][0]
        res=186.8
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[16][0]
        res=(56150/186.8)**0.5
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[17][0]
        res=(18920/186.8)**0.5
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[18][0]
        res=51.9
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[19][0]
        res=59.6
        self.assertLess(abs(un-res)/res,0.001)        


        un=check[20][0]
        res=0.554
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[21][0]
        res=2.02
        self.assertLess(abs(un-res)/res,0.0021)        

        un=check[22][0]
        res=1.12
        self.assertLess(abs(un-res)/res,0.004)        

        un=check[23][0]
        res=0.628
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[24][0]
        res=0.59
        self.assertLess(abs(un-res)/res,0.006)        

        un=check[25][0]
        res=0.37
        self.assertLess(abs(un-res)/res,0.007)        

        
        code=QtCore.QString(u'СП16.13330.2011')
        type_element=QtCore.QString(u'Ферма')
        typ_sec=QtCore.QString(u'Двутавр')
        gost=QtCore.QString(u"ГОСТ 26020-83 (Б) Двутавры с параллельными полками")
        num_sect=QtCore.QString(u'10Б1')
        stl=QtCore.QString(u'C255')
        inp=[1,2,100,2,1]        
        check=basa.output_simple(code, type_element, typ_sec, gost, num_sect, stl, inp) 

        ry=240*100/9.81
        a=10.32
        phix=0.871
        phiy=0.694
        ru=360*100/9.81
        e=2.1*10**6


        un=check[0][0]
        res=phiy*ry*a*2
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[1][0]
        res=ry*a
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[2][0]
        res=0.287
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[3][0]
        res=phix
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[4][0]
        res=phiy
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[5][0]
        res='b'
        self.assertEqual(un, res)        

        un=check[6][0]
        res='b'
        self.assertEqual(un, res)        

        un=check[7][0]
        res=ry*a
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[8][0]
        res=ru*a/1.3
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[9][0]
        res=869.3/9.81*1000
        self.assertLess(abs(un-res)/res,0.002)        

        un=check[10][0]
        res=323.7/9.81*1000
        self.assertLess(abs(un-res)/res,0.002)        


        un=check[11][0]
        res=phiy*ry*2*a/phix*7.15*10**(-6)*(2330-e/ry)
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[12][0]
        res='-'
        self.assertEqual(un, res)        

        un=check[13][0]
        res='-'
        self.assertEqual(un, res)        

        un=check[14][0]
        res='-'
        self.assertEqual(un, res)        

        un=check[15][0]
        res=1.3
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[16][0]
        res=ry
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[17][0]
        res=a
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[18][0]
        res=(171/10.32)**0.5
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[19][0]
        res=(16/10.32)**0.5
        self.assertLess(abs(un-res)/res,0.003)        


        un=check[20][0]
        res=49.1
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[21][0]
        res=80.5
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[22][0]
        res=0.287
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[23][0]
        res=2.16
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[24][0]
        res=0.62
        self.assertLess(abs(un-res)/res,0.002)        

        un=check[25][0]
        res=0.174
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[26][0]
        res=0.6348
        self.assertLess(abs(un-res)/res,0.001)        

        un=check[27][0]
        res=0.1105
        self.assertLess(abs(un-res)/res,0.001)        

        
        print 28        




        
if __name__ == "__main__":
    unittest.main()