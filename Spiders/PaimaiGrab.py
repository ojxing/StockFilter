# -*- coding: utf-8 -*-

'产权交易中心列表抓取'

__author__ = 'ojxing'
__time__ = '2015-12-22'

import re
import requests
import sys
import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')

class PMSpider():
    def __init__(self):
        print('开始抓取数据')
    def getAllPage(self,url):
        links = []
        for each in range(1,9):
            link = re.sub('page=\d+','page=%s'%each,url)
            links.append(link)
        return links
    def getSource(self,url):
        html = requests.get(url)
        return html.content.decode('gbk').encode('utf-8')
    def getEachPage(self,html):
        soup = BeautifulSoup.BeautifulStoneSoup(html)
        paimai = soup.findChildren(bgcolor="#ffffff")
        return paimai
    def getPaiMaiInfo(self,eachList):
        info = {}
        info['Name'] = eachList.contents[2].contents[0].contents[0].string[:-6]
        info['Type'] = eachList.contents[3].contents[0].contents[0]
        info['Date'] = eachList.contents[4].contents[0].contents[0].string[:-6]
        return info
    def Save(self,paimai_info):
        f = open('files/paimai_list.txt','a')
        for each in paimai_info:
            f.writelines('日期：' + each['Date'] + ' 类型：' + each['Type'] +' 名称：' + each['Name'] + '\n')
        f.close()
url = 'http://www.gemas.com.cn/Project/defaultnew.asp?page=1&gopz=asset'
paimai_info =[]
pmspider = PMSpider()
links = pmspider.getAllPage(url)
for each in links:
    print '正在抓取' + each
    html = pmspider.getSource(each)
    eachList = pmspider.getEachPage(html)
    for each in eachList:
        paimai = pmspider.getPaiMaiInfo(each)
        paimai_info.append(paimai)
print('抓取成功！正在保存数据到本地文件...')
pmspider.Save(paimai_info)
print('保存文件成功！')


