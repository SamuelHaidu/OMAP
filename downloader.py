from threading import Thread
import pafy
import os
from mechanize import Browser
from time import sleep, time
from urllib2 import urlopen
from os.path import abspath, dirname
scriptfolder = dirname(abspath(__file__))
dowloadpath = '/mnt/sdcard/OMAP/Download/'

class Downloader(Thread):
    def __init__(self, url, tp='ogg',callback=None):
        Thread.__init__(self)
        self.url = url
        if callback: self.callback = callback
        else: self.callback = self._callback
        self.tp = tp
        self.video = pafy.new(self.url)
    
    def run(self):
        if self.callback and self.tp == 'ogg':
            self.video.getbestaudio(preftype='webm').download(callback=self.callback,
                                               filepath=dowloadpath+self.video.title+'.ogg', 
                                               quiet=True)
            
        elif self.callback and self.tp == 'm4a':
            self.video.getbestaudio(preftype='m4a').download(callback=self.callback,
                                                   filepath=dowloadpath+self.video.title+'.m4a', 
                                                   quiet=True)
            
        elif self.callback and self.tp == 'mp3':
            self.mp3_downloader(self.video.videoid)
            
        else: 
            self.video.getbestaudio(preftype='webm').download(filepath=dowloadpath+self.video.title+'.ogg',
                                               quiet=False)
                                               
    def mp3_downloader(self, video_id):
        self.br = Browser()
        self.link = 'http://www.flvto.biz/downloads/mp3/yt_%s/' % video_id
        self.br.open(self.link)
        self.br.select_form(nr=1)
        self.br.submit()
        sleep(6)
        self.resp = self.br.open('http://www.flvto.biz/download/direct/mp3/yt_%s/' % video_id)
        self.mp3url = self.resp.geturl()
        # Download Now
        self.u = urlopen(self.mp3url)
        self.f = open(dowloadpath+self.video.title+'.mp3', 'wb')
        self.meta = self.u.info()
        self.total = int(self.meta['Content-Length'])
        self.recvd = 0
        self.block_sz = 1048576/4 #Block of 256KB
        while True:
            self.tm = time()
            self.buf = self.u.read(self.block_sz)
            if not self.buf:
                break
            self.etm = time() - self.tm #etm is elipsed time
            self.rate = (float(self.block_sz)/self.etm)
            self.recvd += len(self.buf)
            self.f.write(self.buf) 
            self.ratio = float(self.recvd)/float(self.total)
            self.eta = self.total/self.rate
            self.callback(self.total, self.recvd, self.ratio, self.rate/1024, self.eta)
    
    def _callback(self, total, recvd, ratio, rate, eta):
        print total/1024,'KB', recvd/1024,'KB', int(ratio*100),'%', int(eta), 's'

if __name__ == '__main__':
    Downloader('wbAfu1C8XM0', tp='mp3').start()