#coding=utf-8
#__author__ = 'seyren'
#filname:serverTest.py
#description:
import time
import sys, os
import threading
import urllib2
import socket
import Queue
# from optparse import OptionParser


class ImgSearchClient(object):

    def __init__(self, imgName):
        """"""""
        self.imgName = imgName

    @staticmethod
    def print_help_info():
        print """
        Usage:
        imgSearchClient   [server-ip-address]  [server-port]  [# of thread]  [image-list-file] [forever-flag]
        server-ip-address:  server ip address
        erver-port: server port number
        # of thread: how many thread the program will run
        image-list-file: the input image list file generated from #2
        forever-flag:  1  -- means yes to read images from the beginning again if it reaches the end
                       0  -- means it will end after it reaches the end of the input file
        """


    def sendRequest(self, serverIp, serverPort, fileName):
        requestUrl = ''.join(['http://', serverIp, ':', serverPort, '/vsearchtech/api_v1.0/imgsim/', fileName, '?uid=1&catid=1&format=xml&minscore=0.4'])
        req = urllib2.Request(requestUrl)
        pStartTime = time.time()
        self.reqCount += 1
        try:
            urllib2.urlopen(req, timeout=8)
        except urllib2.URLError as e:
            self.faildRes += 1
            if hasattr(e, 'reason'):
                print 'failed to connect to host'
                print 'Reason:', e.reason
            elif hasattr(e, 'code'):
                print 'The server can\'t hold the request'
                print 'Error code:', e.code
            return 0
        except socket.timeout as e:
            self.faildRes += 1
            print 'timeout:', e
            return 0
        self.reqTime = time.time()
        tResTime = time.time() - pStartTime
        if self.reqCount == 1:
            self.maxRes = self.minRes = tResTime
        if tResTime > self.maxRes:
            self.maxRes = tResTime
        elif tResTime < self.minRes:
            self.minRes = tResTime
        self.lResTime = tResTime
        self.resCount += 1
        self.averRes = (tResTime + self.averRes * (self.resCount - 1)) / self.resCount

    def test(self):
        if self.foreverFlag == '0':
            for line in f:
                self.sendRequest(self.serverIp, self.serverPort, line.strip('\n'))
                sys.stdout.write("\r fail:%s starttime:%s costtime:%s reqCount:%s resCount:%s averRes:%s minRes:%s maxRes:%s" % (self.faildRes, self.startTime, self.reqTime-self.startTime, self.reqCount, self.resCount, self.averRes, self.minRes, self.maxRes))
                sys.stdout.flush()
        else:
            while True:
                for line in f:
                    self.sendRequest(self.serverIp, self.serverPort, line.strip('\n'))
                    sys.stdout.write("\r starttime:%s costtime:%s reqCount:%s resCount:%s averRes:%s minRes:%s maxRes:%s" % (self.startTime, self.reqTime-self.startTime, self.reqCount, self.resCount, self.averRes, self.minRes, self.maxRes))
                    sys.stdout.flush()
        print "============>end<============"




class ThreadReq(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            host = self.queue.get()
            self.queue.task_done()

queue = Queue.Queue()


def main():
    args = sys.argv
    f = open(args[4])
    print args
    if len(args) is not 6:
        ImgSearchClient.print_help_info()
        return 0
    else:
        for i in xrange(args[3]):
            t = ThreadReq(queue)
            t.setDaemon(True)
            t.start()
            if args[5] == '0':
                for line in f:
                    queue.put(line.strip('\n'))
            elif args[5] == '1':
                while True:
                    for line in f:
                        queue.put(line.strip('\n'))


if __name__ == "__main__":
    main()



