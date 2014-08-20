# -*- coding: utf-8 -*-
"""
Created on Fri Aug 08 21:48:07 2014

@author: Pyltsin
"""
import profiles2 as profiles
from  PyQt4 import QtCore, QtGui, uic
import table

class BasaSort(object):
    def __init__(self):
        self.__list_code=[u'СНиП II-23-81*', u'СП16.13330.2012']
        self.list_sort=[u'Прямоугольник',u'Двутавр', u'Швеллер',u'Уголок', u'Прямоугольная труба',
                        u'Труба', u'Уголки в тавр (длинные стор. - вверх)'
                        , u'Уголки в тавр (длинные стор. - в бок)'
                        ,u'Уголки в крест']
        self.dict_sostav_sort={5:2, 6:2, 7:2}
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

        self.__add_data_sostav={5:[u'dx, см'],6:[u'dx, см'],7:[u'dx, см', u'dy, см']}
        self.__list_elements=[[u'Ферма',0],[u'Балка',1],[u'Колонна',2]]
        self.__list4elements=[[0,3,5,6,7],[0,1,3],[1,3]]
        
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
    def list_code(self):
        return self.__list_code
    def add_data_sostav(self, name):
        
        for x in self.dict_sort:
            if QtCore.QString(x)==name:
                number=self.dict_sort[x]
                break
        if number in self.dict_sostav_sort:
            return self.__add_data_sostav[number]
        else:
            return []
    def output_list_sect_num(self, sortament, name):
        if sortament!="" and name!="":
            for x in self.dict_sort:
                if name==QtCore.QString(x):
                    number=self.dict_sort[x]
                    break
            if number in self.dict_sostav_sort:
                number=self.dict_sostav_sort[number]

            for x in self.__list4sortament[number+1]:
                if QtCore.QString(x[0])==sortament:
                    fil=x[1]
            
            table_sect=table.tables_csv(fil,'float')
            list_sect=table_sect.get_title_column()
            return list_sect
        else:
            return ['']
    def output_list_sortament(self, name):
        if name!="":
            for x in self.dict_sort:
                if name==QtCore.QString(x):
                    number=self.dict_sort[x]
                    break
            if number in self.dict_sostav_sort:
                number=self.dict_sostav_sort[number]
            for x in self.__list4sortament[0]:
                if x[1]==number:
                    number_sort=x[1]
                    break
            lst=[]
            for x in self.__list4sortament[number_sort+1]:
                lst.append(x[0])
            list_sortament=lst
            return list_sortament
        else:
            return ['']
    def output_list_section(self, type_section):
        lst=[]
        for x in self.output_list_elements():
            if QtCore.QString(type_section)==QtCore.QString(x[0]):
                numbers_element=self.output_list4elements()[x[1]]
                break
#        print numbers_element
        for y in self.key_sortament():
#            print y
            if self.output_dict_sort()[y] in numbers_element:
                lst.append(y)
        return lst
    def output_list_elements(self):
        return self.__list_elements
    def output_list4elements(self):
        return self.__list4elements
    def output_dict_sort(self):
        return self.dict_sort
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
#        print i
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
