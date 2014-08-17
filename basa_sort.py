# -*- coding: utf-8 -*-
"""
Created on Fri Aug 08 21:48:07 2014

@author: Pyltsin
"""
import profiles2 as profiles
from  PyQt4 import QtCore, QtGui, uic


class BasaSort(object):
    def __init__(self):
        self.list_sort=[u'Прямоугольник',u'Двутавр', u'Швеллер',u'Уголок', u'Прямоугольная труба',
                        u'Труба', u'Уголки в тавр (длинные стор. - вверх)'
                        , u'Уголки в тавр (длинные стор. - в бок)'
                        ,u'Уголки в крест']
        self.dict_sort={u'Двутавр':0, u'Швеллер':1,u'Уголок':2, u'Прямоугольная труба':3,
                        u'Труба':4, u'Уголки в тавр (длинные стор. - вверх)':5
                        , u'Уголки в тавр (длинные стор. - в бок)':6
                        ,u'Уголки в крест':7, u'Прямоугольник':8}
        self.list_input={0:profiles.dvut(1,1,1,1,1,1,0).input_data()
        ,1: profiles.shvel(h=1, b=1, s=1, t=1, r1=1, r2=1, a1=0, r3=1).input_data()
        ,2:profiles.ugol(h=1, b=1, t=0.1, r1=0, r2=0, r3=0).input_data()
        ,3:profiles.truba_pryam(h=1, b=1, t=0.1, r1=0, r2=0).input_data()
        ,4:profiles.ring(r=1, r1=0).input_data()
        ,5:profiles.sost_ugol_tavr_st_up(h=1,b=1,t=1,r1=0,r2=0,r3=0, dx=1).input_data()
        ,6:profiles.sost_ugol_tavr_st_right(h=1,b=1,t=1,r1=0,r2=0,r3=0, dx=1).input_data()
        ,7:profiles.sost_ugol_tavr_st_krest(h=1,b=1,t=1,r1=0,r2=0,r3=0, dx=1, dy=1).input_data()
        ,8:profiles.rectangle(1,1).input_data()
        }

        self.pictures_list={0:'SortamentPicture\dvut.png'
        , 1:'SortamentPicture\shvel.png'
        , 2:'SortamentPicture\ugol.png'
        , 3:'SortamentPicture\korob.png'
        , 4:'SortamentPicture/ring.png'
        , 5:'SortamentPicture\sost_ugol_tavr_st_up.png'
        , 6:'SortamentPicture\sost_ugol_tavr_st_right.png'
        , 7:'SortamentPicture\sost_ugol_tavr_st_krest.png'
        , 8:'SortamentPicture/rectangle.png'}

        self.__list4sortament=[
        [[u'Двутавры',0], [u'Швеллеры',1],[u'Уголки',2],[u'Прямоугольные трубы',3]]
            ,[[u"ГОСТ 8239-89 Двутавры с уклоном полок",u'SortamentData/GOST823989.csv'],
              [u"СТО АСЧМ 20-93 (Б) Двутавры с параллельными полками",u'SortamentData/stoaschm2093(b).csv'],
              [u"СТО АСЧМ 20-93 (Ш) Двутавры с параллельными полками",u'SortamentData/stoaschm2093(sh).csv'],
              [u"СТО АСЧМ 20-93 (К) Двутавры с параллельными полками",u'SortamentData/stoaschm2093(c).csv'],
              [u"ГОСТ 26020-83 (Б) Двутавры с параллельными полками",u'SortamentData/gost2602083(b).csv'],
              [u"ГОСТ 26020-83 (Ш) Двутавры с параллельными полками",u'SortamentData/gost2602083(sh).csv'],
              [u"ГОСТ 26020-83 (К) Двутавры с параллельными полками",u'SortamentData/gost2602083(c).csv'],
              [u"ГОСТ 26020-83 (Д) Двутавры с параллельными полками",u'SortamentData/gost2602083(d).csv'],
              [u"ГОСТ 19425-74* Двутавры специальные",u'SortamentData/gost1942574.csv']]
               
            ,[[u"ГОСТ 8240-97 (У) Швеллеры стальные горячекатанные",u'SortamentData/GOST824097(u).csv'] ,
               [u"ГОСТ 8240-97 (П) Швеллеры стальные горячекатанные",u'SortamentData/GOST824097(p).csv'],
                [u"ГОСТ 8278-83 Швеллеры гнутые (С235, С245)",u'SortamentData/GOST827883(l460).csv'],
                [u"ГОСТ 8278-83 Швеллеры гнутые (С255, С345)",u'SortamentData/GOST827883(r460).csv']]
            
            ,[[u"ГОСТ 8509-93 Уголки равнополочные",u'SortamentData/GOST850993.csv'],
              [u"ГОСТ 8510-86 Уголки неравнополочные",u'SortamentData/GOST851086.csv'],
              [u"ГОСТ 19771-93 Уголки гнутые равнополочные (Run<460 Н/мм2, C235, C245)",u'SortamentData/GOST1977193(l460).csv'],
              [u"ГОСТ 19771-93 Уголки гнутые равнополочные (Run>460 Н/мм2, C255, C345)",u'SortamentData/GOST1977193(r460).csv'],
              [u"ГОСТ 19772-93 Уголки гнутые неравнополочные (Run<460 Н/мм2, C235, C245)",u'SortamentData/GOST1977293(l460).csv'],
              [u"ГОСТ 19772-93 Уголки гнутые неравнополочные (Run>460 Н/мм2, C255, C345)",u'SortamentData/GOST1977293(r460).csv']
              ]
            
            ,[[u"ГОСТ 30245-2003 (Кв) Квадратные замкнутые сечения",u'SortamentData/gost302452003(k).csv'] ,
               [u"ГОСТ 30245-2003 (Прям) Прямоугольные замкнутые сечения",u'SortamentData/gost302452003(pr).csv'] 
               ]
        ]
    def output_data(self, i, inp):
        x=None
        for label in self.dict_sort:
            if i==QtCore.QString(label):
                x=self.dict_sort[label]
        if x==None:
            x=i
        if x==0:
#            print inp

            pr=profiles.dvut(inp[0],inp[1],inp[2],inp[3],inp[4],inp[5],inp[6])
        elif x==1:
            pr=profiles.shvel(inp[0],inp[1],inp[2],inp[3],inp[4],inp[5],inp[6],inp[7])
        elif x==2:
#            print inp
            pr=profiles.ugol(inp[0],inp[1],inp[2],inp[3],inp[4],inp[5])
        elif x==3:
#            print inp
            pr=profiles.truba_pryam(inp[0],inp[1],inp[2],inp[3],inp[4])
        elif x==4:
            pr=profiles.ring(inp[0],inp[1])
        elif x==5:
            pr=profiles.sost_ugol_tavr_st_up(inp[0],inp[1],inp[2],inp[3],inp[4],inp[5],inp[6])
        elif x==6:
            pr=profiles.sost_ugol_tavr_st_right(inp[0],inp[1],inp[2],inp[3],inp[4],inp[5],inp[6])
        elif x==7:
            pr=profiles.sost_ugol_tavr_st_krest(inp[0],inp[1],inp[2],inp[3],inp[4],inp[5],inp[6],inp[7])
        elif x==8:
            pr=profiles.rectangle(inp[0],inp[1])
        return pr
    def pict(self, i):
        
        for label in self.dict_sort:
            if i==QtCore.QString(label):
                x=self.dict_sort[label]
        return self.pictures_list[x]
    def input_data(self, i):

        for label in self.dict_sort:
#            print type(i)
#            print label
            if i==QtCore.QString(label):
                x=self.dict_sort[label]

        y=self.list_input[x]
        return y


    def key_sortament(self):
        return self.list_sort
    def list4sortament(self):
        return self.__list4sortament
    def pict4sortament(self, i):
        return self.pictures_list[i]
    def input_data4sortament(self, i):
        return self.list_input[i]