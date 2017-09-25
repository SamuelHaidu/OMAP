from threading import Thread
import pafy
import os
sdcard = '/mnt/sdcard/'
class Downloader(Thread):
    def __init__(self, url, tp='ogg', callback=None):
        Thread.__init__(self)
        self.url = url
        self.tp = tp
        self.callback = callback
    
    def run(self):
        self.video = pafy.new(self.url)
        if self.callback and self.tp == 'ogg':
            self.video.getbestaudio(preftype='webm').download(callback=self.callback,
                                               filepath=sdcard+'OMAP/Download'+self.video.title+'.ogg', 
                                               quiet=True)
            print 'Downloaded in ' +self.tp
        elif self.callback and self.tp == 'm4a':
            self.video.getbestaudio(preftype='m4a').download(callback=self.callback,
                                                   filepath=sdcard+'OMAP/Download'+self.video.title+'.m4a', 
                                                   quiet=True)
            print 'Downloaded in ' +self.tp      
        else: 
            self.video.getbestaudio(preftype='webm').download(filepath=sdcard+'OMAP/Download'+self.video.title+'.ogg',
                                               quiet=False)
