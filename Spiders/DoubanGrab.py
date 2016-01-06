# -*- coding: utf-8 -*-

'豆瓣电影TOP250抓取'

__author__ = 'ojxing'
__time__ = '2015-12-21'

import re
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class DbSpider():
    def __init__(self):
        print '开始抓取网页...'
    def getAllPage(self,url):
        links = []
        for i in range(0,226,25):  #201
            link = re.sub('start=\d+','start=%d'%i,url)
            links.append(link)
        return links
    def getSource(self,url):
        html = requests.get(url);
        return html.text
    def getSingleMovie(self,eachPageSource):
        movie = re.findall('<div class="item">(.*?)<p class="quote">',eachPageSource,re.S)
        return movie
    def getMovieInfo(self,movie):
        info = {}
        info['title'] = re.search('<span class="title">(.*?)</span>',movie,re.S).group(1)
        info['rating'] = re.search('<span class="rating_num" property="v:average">(.*?)</span>',movie,re.S).group(1)
        info['ratingNum'] = re.search('<span>(.*?)</span>',movie,re.S).group(1)
        return info
    def save(self,movie_infos):
        f = open('movie_list.txt','a')
        for each in movie_infos:
            f.writelines('评分：' + each['rating'] + '   评分人数：' + each['ratingNum'] +' 电影：' +each['title'] +'\n')
        f.close()
movie_infos = []
url = 'http://movie.douban.com/top250?start=0&filter='
dbspider = DbSpider()
all_links = dbspider.getAllPage(url)
for eachPage in all_links:
    print '正在抓取 ' + eachPage
    html = dbspider.getSource(eachPage)
    SingleMovie = dbspider.getSingleMovie(html)
    for each in SingleMovie:
        info = dbspider.getMovieInfo(each)
        movie_infos.append(info)
print '完成抓取！正在保存数据！'
dbspider.save(movie_infos)
