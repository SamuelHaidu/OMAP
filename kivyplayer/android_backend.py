from jnius import autoclass
MediaPlayer = autoclass('android.media.MediaPlayer')

class MPlayer():
    def __init__(self):
        self.mPlayer = MediaPlayer()
        self.length = 0
        self.state = 'stop'
    
    def load(self, audio):
        self.mPlayer.setDataSource(audio)
        self.mPlayer.prepare()
        self.length = self.mPlayer.getDuration()/1000

    def play(self):
        self.mPlayer.start()
        self.state = 'play'
    def stop(self):
        self.mPlayer.stop()
        self.state = 'stop'
    def pause(self):
        self.mPlayer.pause()
        self.state = 'stop'
    def seek(self,position):
        self.mPlayer.seekTo(int(position*1000))
        
    def get_pos(self):
        return self.mPlayer.getCurrentPosition()/1000
    
    def set_mute(self):
        self.mPlayer.setVolume(0.0, 0.0)
    
    def set_unmute(self):
        self.mPlayer.setVolume(1.0, 1.0)
    
    def set_volume(self, volume):
        self.mPlayer.setVolume(volume/100, volume/100)