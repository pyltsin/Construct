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

    def output_data(self, i, inp):
        for label in self.dict_sort:
            if i==QtCore.QString(label):
                x=self.dict_sort[label]
        if x==0:
            pr=profiles.dvut(inp[0],inp[1],inp[2],inp[3],inp[4],inp[5],inp[6])
        elif x==1:
            pr=profiles.shvel(inp[0],inp[1],inp[2],inp[3],inp[4],inp[5],inp[6],inp[7])
        elif x==2:
            pr=profiles.ugol(inp[0],inp[1],inp[2],inp[3],inp[4],inp[5])
        elif x==3:
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
