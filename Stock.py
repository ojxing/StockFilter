# -*- coding: utf-8 -*-
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
'单只股票抓取'

__author__ = 'ojxing'
__time__ = '2015-12-25'

def filefilter(reg='format',rout='str'):
    filesobj = os.walk(rout)
    for root,dir,files in filesobj:
        filess = files
    test =re.compile(reg,re.IGNORECASE)
    fileout = filter(test.search,filess)
    return fileout




def OHLC(li = 'list'):
    return float(li[4])

def closeavg3(lis = 'list'):
    sum2 = 0
    for i in lis:
        sum2 += float(i[4])
    return float(sum2/len(lis))

def postavg3(lis = 'list'):
    sum1 = 0
    for i in lis:
        sum1 += float(i[5])
    return float(sum1/len(lis))

def twinpost(li='list'):
    '倍量柱'
    if len(li) == 5:
        if float(li[-4][5]) >=float(li[-5][5])*1.9 and OHLC(li[-4]) >=OHLC(li[-5]):
            return 1
        else:
            return 0
    else:
        return -1
def goldpost(lis=[]):
    '''黄金柱'''
    if float(lis[-4][4]) > float(lis[-4][1]):
        if((closeavg3(lis)/float(lis[-4][4]))>1.0 and (postavg3(lis)<float(lis[-4][5]))):
            return 1
        else:
            return 0
    else:
        if((closeavg3(lis)/float(lis[-4][1]))>1.0 and (postavg3(lis)<float(lis[-4][5]))):
            return 1
        else:
            return 0


class SingleMapping:
    'N天内某个股票的黄金柱列表'
    def __init__(self,filename,nem='int'):
        self.name = filename
        self.nemb = nem
        self.csvfile = CsvRead(self.name)
        self.Fname = self.csvfile.FileN
    def goldPosts(self,nemb=0):
        data = self.csvfile.reading(nemb)  #获取对应日期往后5天的数据
        #return twinpost(data)
        if data!=[]:
            data2 = [data[-4][1],data[-4][4],min(data[-3][3],data[-2][3],data[-1][3])]
            data2.sort()
        else:
            return [1,[]]
        if twinpost(data) and goldpost(data):
            return [self.csvfile.DATE,data2]
        else:
            return [1,[]]

    def mapping(self):
        li= []
        for n in range(self.nemb):
            li.append(self.goldPosts(n))

        lis = []
        for m in li:
            if type(m[0]) == str:
                lis.append(m)
        return [self.Fname,lis]
class CsvRead:
    '读取某股票csv文件'
    def __init__(self,filename='strs'):
        self.filename = 'files/STOCK/'+filename
        self.DATE = ''
        self.data = []
        self.FileN = ''
        #self.read()
        self.readxml()



    def read(self):
        csv = open(self.filename,'r')
        csvdata = csv.readlines()
        csv.close()
        data1 = []
        for n in range(len(csvdata)):
            data1.append(csvdata[n].split('\n'))
        data1 = data1[4:-1]
        data2 = []
        for n in range(len(data1)):
            data2.append(data1[n][0].split(','))
        self.data = data2

    def readxml(self):
        csv = open(self.filename,'r')
        csvdata = csv.readlines()
        csv.close()
        data1 = []
        for n in range(len(csvdata)):
            data1.append(csvdata[n].split('\n'))

        self.FileN = data1[0][0].decode('GBK')[:-6]
        data1 = data1[2:-1]
        data2 = []
        for n in range(len(data1)):
            data2.append(data1[n][0].split('\t'))
        self.data = data2
    def reading(self,nem = 0):
        if nem == 0:
            if len(self.data) >=7:
                self.DATE = self.data[-4][0]
                return self.data[-5:]
            else:
                return []
        else:
            data4 = self.data[:-nem]
            if len(data4)>=7:
                self.DATE = data4[-4][0]
                return data4[-5:]
            else:
                return []

fi = filefilter('.xls',"files/STOCK")
for stock in fi:
    a = SingleMapping(stock,150)
    code,lis=a.mapping()
    if len(lis) >=8:
        print '股票代码：' + code + '黄金柱数量：' + str(len(lis))

        for each in lis:
            print(each)
        print('\n')



# b = CsvRead("000860")
# da = b.data
# for eac in da:
#     print(eac)






























