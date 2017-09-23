from threading import Thread
import pafy
import os
sdcard = '/mnt/sdcard/'
class Downloader(Thread):
    def __init__(self, url, callback=None):
        Thread.__init__(self)
        self.url = url
        self.callback = callback
    
    def run(self):
        self.video = pafy.new(self.url)
        if self.callback:
            self.video.getbestaudio().download(callback=self.callback,
                                               filepath=sdcard+'OMAP/Download'+self.video.title+'.ogg', 
                                               quiet=True)
        else: 
            self.video.getbestaudio().download(filepath=sdcard+'OMAP/Download'+self.video.title+'.ogg',
                                               quiet=False)