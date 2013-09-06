#!/bin/python
#coding=utf-8
from bs4 import BeautifulSoup
import urllib2
import os

url = "http://www.shiyebian.net/zhejiang/ningbo/"
headers = {
        "GET":url,
        "HOST":"www.shiyebian.net",
        "Referer":"http://www.baidu.com",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36",
        }
req = urllib2.Request(url)

for key in headers:
    req.add_header(key,headers[key])

data = urllib2.urlopen(req).read()
#html2 = html.decode('gb2312','ignore').encode('utf-8')
soup = BeautifulSoup(data)
html2 = soup.find("ul", {"class": "lie2"}).findAll("a")[:4]
#print html2
s = ''
for item in html2:
    s  = s + item.text + item.get("href") + ' '
print s
os.popen('echo  "%s" |mutt -s "事业单位" -- 262864590@qq.com' %s)
#os.popen(echo )
#s = [item.text for item in html2.findAll("a")]
