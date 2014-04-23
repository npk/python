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

global reqDict
reqDict = {}
reqDict['reqCount'] = 0
reqDict['maxRes'] = 0
reqDict['minRes'] = 0
reqDict['resCount'] = 0
reqDict['avgRes'] = 0
reqDict['QPS'] = 0
reqDict['BRDR'] = 0
reqDict['data'] = 0
reqDict['t'] = 0


class ThreadReq(threading.Thread):


    def __init__(self, queue, args):
        threading.Thread.__init__(self)
        self.queue = queue
        self.args = args

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
        print self.getName(), time.time(), '========>start'
        requestUrl = ''.join(['http://', serverIp, ':', serverPort, '/vsearchtech/api_v1.0/imgsim/', fileName, '?uid=1&catid=1&format=xml&minscore=0.4'])
        req = urllib2.Request(requestUrl)
        pStartTime = time.time()
        reqDict['reqCount'] += 1
        failReq = 0
        while True:
            try:
                if failReq > 3:
                    data = 0
                    break
                data = urllib2.urlopen(req, timeout=8).read()
            except:
                failReq += 1
            else:
                reqDict['resCount'] += 1
                tResTime = time.time() - pStartTime
                if reqDict['resCount'] == 1:
                    reqDict['minRes'] = reqDict['maxRes'] = tResTime
                if tResTime > reqDict['maxRes']:
                    reqDict['maxRes'] = tResTime
                elif tResTime < reqDict['minRes']:
                    reqDict['minRes'] = tResTime
                reqDict['avgRes'] = (tResTime + reqDict['avgRes'] * (reqDict['resCount'] - 1)) / reqDict['resCount']
                reqDict['data'] += len(data)
                print time.time(), start, time.time() - start
                reqDict['QPS'] = reqDict['reqCount'] / (time.time() - start)
                reqDict['t'] = tResTime
                reqDict['BRDR'] = reqDict['data'] / (time.time() - start)
                break

    def run(self):
        while True:
            imgName = self.queue.get()
            self.sendRequest(self.args[1], self.args[2], imgName)
            print reqDict
            self.queue.task_done()


class PrintThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            print self.queue.get()
            self.queue.task_done






queue1 = Queue.Queue()

def main():
    args = sys.argv
    print args
    if len(args) is not 6:
        ThreadReq.print_help_info()
        return 0
    else:
        f = open(args[4])
        for i in xrange(int(args[3])):
            t = ThreadReq(queue1, args)
            t.setDaemon(True)
            t.start()
            if args[5] == '0':
                for line in f:
                    queue1.put(line.strip('\n'))
            elif args[5] == '1':
                while True:
                    for line in f:
                        queue1.put(line.strip('\n'))
        queue1.join()


if __name__ == "__main__":
    start = time.time()
    main()
    print "cost:%s" % (time.time() - start)



