#coding=UTF-8
import urllib2
from bs4 import BeautifulSoup
import os
num=1
#伪造浏览器标识
header={
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:8.0.1) Gecko/20100101 Firefox/8.0.1'}  
#定义一个抓取函数，这个可以用于网页、图片的内容读取
def getsite(url):
    req=urllib2.Request(url,None,header) 
    site=urllib2.urlopen(req)
    return site.read()


#s = raw_input('请输入要下载的分区内容1 2 3')
#循环，这个是页码范围，手工得到的
for i in xrange(1,24):
    print i
    try:
        first_url="http://tu.acfun.tv/picture/index.aspx?channelId=2&pageNo=%d" % i
        data=getsite(first_url)
        soup=BeautifulSoup(data)
        #print soup

#用bs4解析
        result=soup.find_all('img')

        #for s in range(len(result)):
         #   print 'result[%d]' % s
          #  print result[s]
        for q in result:

#图片网址在src属性里
                if q.get('src')!=None:
                    #筛选
                    if q['src'].find('http')>=0:
                        picpath=q['src']
                        print picpath
                        b = '.'
                        ok = picpath[picpath.rfind(b):]
                        print ok
                        if ok != ".com/": 
                            picname = " result/%d%s" % (num,ok)
                            pic=open(picname,'wb')
                            pic.write(getsite(picpath))
                            pic.close()
                               #如果图片大小小于10kb就删除
                            if os.path.getsize(picname)<10240:
                                os.remove(picname)
                            else:
                                num+=1
    except KeyError,e:
        print "Key not find:%s"%e 