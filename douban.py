#__author__ = 'seyren'
# -*- coding:utf8 -*-

from bs4 import BeautifulSoup
import os, urllib2

path = os.getcwd()
new_path = os.path.join(path,'read')

#判断是否有这个目录，没有就新建
if not os.path.isdir(new_path):
    os.mkdir(new_path)

url = 'http://book.douban.com/subject/25747921/'
urlList = []

print '解析观后感列表'

soup = BeautifulSoup(urllib2.urlopen(url).read())
bname = soup.find('h1').get_text().encode('utf-8')

for divs in soup.find_all("div", {"class":"rr"})[:6]:
    urlList.append(divs.a.get("href"))
print urlList


fileHandle = open(new_path +'/' + bname + '.txt','a')


for Rurl in urlList:
    temp = BeautifulSoup(urllib2.urlopen(Rurl).read())
    title = temp.find("h1").get_text().encode('utf-8')
    fileHandle.write(title + '\n\n\n')
    content = temp.find("span",{"property":"v:description"}).get_text().encode('utf-8','ignore')
    fileHandle.write(content + '\n\n\n')
    fileHandle.write('————————分割线————————————\n\n\n')
