# -*- coding: utf-8 -*-

'韩剧抓取'

__author__ = 'ojxing'
__time__ = '2015-12-25'

import re
import requests
import sys
import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')

class HJSpider():
    def __init__(self):
        print('开始抓取数据')
    def getAllPage(self,url):
        links = []
        for each in range(1,8):
            link = re.sub('chart/\d+','chart/%s'%each,url)
            links.append(link)
        return links
    def getSource(self,url):
        html = requests.get(url)
        return html.content.decode('gbk').encode('utf-8')
    def getEachPage(self,html):
        soup = BeautifulSoup.BeautifulStoneSoup(html)
        paimai = soup.findAll('img',{"class":"vipicbg"})
        titles = []
        hrefs = []
        for each in paimai:
            title = each.get('alt')
            href = each.get('src')
            titles.append(title)
            hrefs.append(href)
        timess = soup.findAll('div',{"class":"img"})
        times = []
        for each in timess:
            time = each.nextSibling.nextSibling
            time = time.string
            times.append(time)
        return titles,times,hrefs
    def getPaiMaiInfo(self,eachList,hanju_info):
        length = len(eachList[0])
        for i in range(length):
            info = {}
            info['Title'] = eachList[0][i]
            info['Date'] = eachList[1][i]
            info['Href'] = eachList[2][i]
            hanju_info.append(info)
        return hanju_info
    def Save(self,hanju_info):
        f = open('files/hanjv_list.txt','a')
        for each in hanju_info:
            f.writelines('日期：' + each['Date'] + ' 名称：' + each['Title'] + ' 链接：' +each['Href'] + '\n')
        f.close()
url = 'http://www.loldytt.com/Zuixinhanju/chart/1.html'
hanju_info =[]
pmspider = HJSpider()
links = pmspider.getAllPage(url)
for each in links:
    print '正在抓取' + each
    html = pmspider.getSource(each)
    eachList = pmspider.getEachPage(html)

    hanju_info = pmspider.getPaiMaiInfo(eachList,hanju_info)
i = 0
for each in hanju_info:
    print 'now downloading:' + each['Date']
    e = each['Href']
    pic = requests.get(e)
    fp = open('pic\\'+ str(i) + '.jpg','wb')
    fp.write(pic.content)
    fp.close()
    i+=1

print('抓取成功！正在保存数据到本地文件...')
pmspider.Save(hanju_info)
print('保存文件成功！')


